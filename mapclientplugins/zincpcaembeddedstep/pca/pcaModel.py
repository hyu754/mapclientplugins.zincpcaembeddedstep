from PySide import QtCore, QtGui
from pca_ui import Ui_MainWindow

from opencmiss.zinc.context import Context 
from opencmiss.zinc.field import Field
from opencmiss.zinc.fieldcache import Fieldcache
from opencmiss.zinc.region import Region
from opencmiss.zinc.node import Node,Nodetemplate,Nodeset
from opencmiss.zinc.element import Element,Elementtemplate,Elementbasis,Elementiterator
from opencmiss.zinc.spectrum import Spectrum
from opencmiss.zinc.graphics import GraphicsLines,Graphicslineattributes,Graphics
from opencmiss.zinc.field import FieldFindMeshLocation
import numpy as np

import os
class pcaView(QtGui.QMainWindow):



	# ZincViewGraphics__init__ start
	def __init__(
		self,
		_geometry_directory,
		_embedding_directory,
		_embedding_host_file,
		_embedded_geo_files,
		_embedded_geo_groupnames=None, 
		parent=None):
	    '''
	    Initialise the ZincViewGraphics first calling the QMainWindow __init__ function.
	    '''
	    QtGui.QMainWindow.__init__(self, parent)

	    # create instance of Zinc Context from which all other objects are obtained
	    self._context = Context("ZincViewGraphics");

	    # set up standard materials for colouring graphics
	    self._context.getMaterialmodule().defineStandardMaterials()
	    # set up standard glyphs, graphics to show at points e.g. spheres, arrows
	    self._context.getGlyphmodule().defineStandardGlyphs()

	    self._ui = Ui_MainWindow()
	    self._ui.setupUi(self)
	    self._ui.sceneviewerWidget.setContext(self._context)
	    self._ui.sceneviewerWidget.graphicsInitialized.connect(self._graphicsInitialized)


	    #Set default number of principle components to 2
	    self.numberOfComponents = 2
	    self._ui.numberPrincipleComponent.setText(str(self.numberOfComponents))


	    #array to store sliders and frames objects for component slider
	    self.sliderArray=[]
	    self.frameArray=[]
	    self.labelArray =[]
	    self._makeDynamicSliders()

	    
	    self.stored_surface_location = None
	    self.embeddedGeo_coordinates = None
	    self.globalNodeset = None


	    #directory of shapes for pca
	    self._geometry_directory=_geometry_directory

	    #directory of embedding geometries
	    self._embedding_directory = _embedding_directory

	    #host mesh fiel
	    self._embedding_host_file= _embedding_host_file

	    #embedded geometry filenames
	    self._embedded_geo_files = _embedded_geo_files

	    #embedded geometry group names
	    self._embedded_geo_groupnames = _embedded_geo_groupnames


	    #possible default zinc colours
	    self._colour_array = ['gold','red','cyan','blue','orange','silver']

	    #population size
	    self._population_size = 0

	    #global feature vector for pca. It will store numpy arrays.
	    self.featureVector =[]

	    #Make connections to pyside
	    self._makeConnections()



	    #Read all geometries
	    self.readAllGeometries()


	    #Perform initial pca for 2 components
	    self.performPCA(nComponent_=self.numberOfComponents)
	    #assign features to geometry
	    self.createNewShapes()

	    self.sliderChanged()

	    #show the zinc objects
	    self.showLiver()

	    
	def _graphicsInitialized(self):
		self._ui.sceneviewerWidget.getSceneviewer()
		self._ui.sceneviewerWidget.getSceneviewer().setBackgroundColourRGB([1,1,1])
	    

	def readAllGeometries(self):
		'''
		Read all geometries specified by the _geometry_directory variable.
		Currently only takes .exnode and .exelem pairs.

		TODO: add .exfile support.
		'''
		
		for root,dirs,files in os.walk(self._geometry_directory):
			for file_ in files:
				if '.exnode' in file_:
			
					READ_SUCCESS=self.readExNodeElem(root,file_)
					if(READ_SUCCESS):
						self.create_PCA_group('pca')
						self.modifyFeatureVector()
					
						self._population_size+=1

		
		
		self.embedGeometry()
		
		
	def create_PCA_group(self,name_):
		'''
		create pca group with name_ 
		'''

		region = self._context.getDefaultRegion()
		fieldmodule = region.getFieldmodule()

		globalnodeset = fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
		node_iter_ = globalnodeset.createNodeiterator()


		#Create node group
		fieldgroup_ = fieldmodule.createFieldGroup()
		fieldgroup_.setName(name_)
		fieldgroup_.setManaged(True)

		#get the nodeset group
		fieldnodegroup = fieldgroup_.createFieldNodeGroup(globalnodeset)
		nodesetgroup = fieldnodegroup.getNodesetGroup()

		#add current nodes into this group
		node_ = node_iter_.next()

		while(node_.isValid()):
			nodesetgroup.addNode(node_)
			node_  = node_iter_.next()


	def readExNodeElem(self,dir_,file_name_ ):
		'''
		Read exnode and exelem file, given the file_prefix
		returns 0, if fail, 1 if succeed
		'''

		region = self._context.getDefaultRegion()
		file_prefix = os.path.splitext(file_name_)[0]
		node_path_ = os.path.join(dir_,file_prefix+".exnode")
		element_path_ = os.path.join(dir_,file_prefix+".exelem")
		if not region.readFile(node_path_):
			print("Node file does not exist : {}".format(node_path_))
			return 0 
		if not region.readFile(element_path_):
			print("Element file does not exist : {}".format(element_path_))
			return 0

		return 1
	def saveRegion(self,name_):
		'''
		Save region to file with name_
		'''
		region = self._context.getDefaultRegion().writeFile(name_)


	def embedGeometry(self):
		region = self._context.getDefaultRegion()
		fieldmodule = region.getFieldmodule()


		


		
		embed_mesh_dir = self._embedding_directory
		host_mesh_file = self._embedding_host_file
		region.readFile(os.path.join(embed_mesh_dir,host_mesh_file+'.exnode'))
		region.readFile(os.path.join(embed_mesh_dir,host_mesh_file+'.exelem'))

		
		
		coordinates = fieldmodule.findFieldByName("coordinates")
		coordinates.setName('surface_coordinates')

		
		surface_coordinates = fieldmodule.findFieldByName("surface_coordinates")


		for embedded_file_ in self._embedded_geo_files:
			region.readFile(os.path.join(embed_mesh_dir,embedded_file_+'.exnode'))
			region.readFile(os.path.join(embed_mesh_dir,embedded_file_+'.exelem'))




		embeddedGeo_coordinates = fieldmodule.findFieldByName("coordinates")
		embeddedGeo_coordinates.setName('embeddedGeo_coordinates')


		region.readFile(os.path.join(embed_mesh_dir,host_mesh_file+'.exnode'))
		region.readFile(os.path.join(embed_mesh_dir,host_mesh_file+'.exelem'))
		

		fieldmodule.beginChange()
		
		mesh3d_ = fieldmodule.findMeshByDimension(3)
		
		find_surface_location = fieldmodule.createFieldFindMeshLocation(embeddedGeo_coordinates,surface_coordinates,mesh3d_)
		find_surface_location.setSearchMode(FieldFindMeshLocation.SEARCH_MODE_EXACT )
		find_surface_location.setName('find_surface_location')

	
		#gfx define field stored_surface_location finite_element element_xi
		stored_surface_location = fieldmodule.createFieldStoredMeshLocation(mesh3d_)



		#gfx modify nodes group portal define stored_surface_location
		globalNodeset = fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
		

		nodetemplate = globalNodeset.createNodetemplate()
		stored_surface_location.setName('stored_surface_location')

		nodetemplate.defineField(stored_surface_location)
	
		#merge
		embed_iter = globalNodeset.createNodeiterator()
		node_ = embed_iter.next()
		cache = fieldmodule.createFieldcache()
		while(node_.isValid()):
	
			node_.merge(nodetemplate)
			
			node_ = embed_iter.next()
		
		#gfx evaluate ngroup portal destination stored_surface_location source find_surface_location
		self.evaluate_ngroup(fieldmodule, find_surface_location, stored_surface_location, globalNodeset,stored_surface_location.getValueType())

		#gfx define field stored_surface_coordinates embedded element_xi stored_surface_location field surface_coordinates
		stored_surface_coordinates = fieldmodule.createFieldEmbedded(embeddedGeo_coordinates,stored_surface_location)



		#gfx evaluate ngroup portal source stored_surface_coordinates destination coordinates
		self.evaluate_ngroup(fieldmodule, stored_surface_coordinates, embeddedGeo_coordinates, globalNodeset,embeddedGeo_coordinates.getValueType())
		
		self.stored_surface_coordinates = stored_surface_coordinates
		self.embeddedGeo_coordinates = embeddedGeo_coordinates
		self.globalNodeset = globalNodeset
		self.stored_surface_location = stored_surface_location
		fieldmodule.endChange()
	def evaluate_ngroup(self,fieldmodule,source_field,target_field,nodeset,value_type):
		'''
		Wrapper for the cmgui command "gfx evaluate ngroup ..."
		value_type: 1-real, 3-meshlocation
		'''
		#gfx evaluate ngroup portal destination stored_surface_location source find_surface_location
		
		#fieldmodule.beginChange()

		nodeIterator = nodeset.createNodeiterator()
		node_ = nodeIterator.next()



		node_id_ =0
		cache = fieldmodule.createFieldcache()
		
		while(node_.isValid()):
			cache.setNode(node_)


			if(value_type==3):
				el_,xi_ = source_field.evaluateMeshLocation(cache,3)
				#print(el_.isValid())
				if(el_.isValid()):
					status_=target_field.assignMeshLocation(cache,el_,xi_)
			elif(value_type==1):
				
				status,out = source_field.evaluateReal(cache,3)
				if(status):

					target_field.assignReal(cache,out)

	
			node_ = nodeIterator.next()



	def modifyFeatureVector(self,set_ = False, set_feature_=[]):
		'''
		This function can get, or set, the opencmiss geometry.
		Input:
			set_ - determine if setting feature or getting feature
			set_feature_ - if above is true then we this variable will set 
								the nodal features
		
		'''

		region = self._context.getDefaultRegion()

		fieldmodule = region.getFieldmodule()

		#Coordinate field
		coordinates = fieldmodule.findFieldByName("coordinates")

		#get global nodeset
		globalNodeset = fieldmodule.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)

		#Create node iterator
		pca_field = fieldmodule.findFieldByName('pca')

		pca_fieldgroup = pca_field.castGroup()

		pca_node_fieldgroup = pca_fieldgroup.getFieldNodeGroup(globalNodeset)

		pca_nodeset_group =pca_node_fieldgroup.getNodesetGroup()


		nodeIterator = pca_nodeset_group.createNodeiterator()
		#nodeIterator = globalNodeset.createNodeiterator()


		cache = fieldmodule.createFieldcache()
		if(set_ == False):
			node_ = nodeIterator.next()

			geometryFeature = []

			while(node_.isValid()):
				cache.setNode(node_)
				#We have 8 values per coordinates.x,y,z 
				#k=0 is the position for x,y,z, k=1 is the first derivative and so on,
				nodeFeature=[]
				for k in range(1,8+1):

					nodeValueField = fieldmodule.createFieldNodeValue(coordinates,k,1)

					status,out = nodeValueField.evaluateReal(cache,3)
					nodeFeature.append(out)

				geometryFeature.append(nodeFeature)

					

				node_ = nodeIterator.next()

			#print("Geometry {}: \n {}".format(id,geometryFeature))

			self.featureVector.append(geometryFeature)
		else:

			scene = region.getScene()
			scene.beginChange()

			fieldmodule.beginChange()

			
			pca_field = fieldmodule.findFieldByName('pca')

			pca_fieldgroup = pca_field.castGroup()

			pca_node_fieldgroup = pca_fieldgroup.getFieldNodeGroup(globalNodeset)

			pca_nodeset_group =pca_node_fieldgroup.getNodesetGroup()


			nodeIterator = pca_nodeset_group.createNodeiterator()

			node_ = nodeIterator.next()



			node_id_ =0
			while(node_.isValid()):
				cache.setNode(node_)
				#We have 8 values per coordinates.x,y,z 
				#k=0 is the position for x,y,z, k=1 is the first derivative and so on,
				
				for k in range(1,8+1):

					nodeValueField = fieldmodule.createFieldNodeValue(coordinates,k,1)
					#print(set_feature_[node_id_,k-1,:].tolist())
					nodeValueField.assignReal(cache,set_feature_[node_id_,k-1,:].tolist())




					

				node_ = nodeIterator.next()
				node_id_+=1

			fieldmodule.endChange()

			scene.endChange()
	def performPCA(self,nComponent_=None):
		'''
		Performs PCA. Generates P matrix.
		Inputs:
			-nComponent_  : number of components to use

		'''
		#Get information on features
		featureVector = np.array(self.featureVector)
		#print(featureVector.shape)
		(numGeo,numNode,numF,dim) = featureVector.shape

		self.numNode = numNode
		self.numF = numF
		self.dim = dim

		#number of features
		featureSize = numNode*numF*dim

		#initialize mean shape feature vector
		meanShapeFeature = np.zeros((numNode,numF,dim))


		for i in range(numGeo):
			meanShapeFeature += featureVector[i,:,:,:]/numGeo

		self.meanShapeFeature = meanShapeFeature

		#find deviations of each shape from the mean dx_i = x_i - x_mean
		#and then find covariance matrix S, where S = (1/N)sum dx_i dx_i.T
		
		#initialize S
		S = np.zeros((featureSize,featureSize))
		for i in range(numGeo):
			dx_i = meanShapeFeature.flatten() - featureVector[i,:,:,:].flatten()
			dx_i = dx_i.reshape((dx_i.shape[0],1))
			S += (1.0/numGeo) *np.dot(dx_i,dx_i.T) 



		
		#Find eig-values,vectors. Note the values are in ascending order
		eigValues,eigVectors = np.linalg.eigh(S)

		#flip the eigvalues
		eigValuesSorted = np.flip((eigValues),0)
		self.eigValuesSorted = eigValuesSorted

		#indexK is the number of eigenvalues to use
		indexK =0
		eigSum_=0
		eigTot_=np.sum(eigValuesSorted) #sum of all eigenvalues
		for i_, eigVal_ in enumerate(eigValuesSorted):
			eigSum_ += eigVal_/eigTot_
			
			#if eigsum breaks them
			if(i_> nComponent_):
				break

		indexK_ = nComponent_
		self.indexK_ = indexK_
		


		pca_string_out_ = "Population size: {}\n".format(self._population_size)
		pca_string_out_ += "{}% of the variance can be explained with {} components".format(int(eigSum_*100),indexK_)
		self._ui.labelPCAInformation.setText(QtGui.QApplication.translate("MainWindow", pca_string_out_, None, QtGui.QApplication.UnicodeUTF8))
		#Create the P, matrix outlined in the paper.
		#Where P = (p_1,p_2,...,p_{indexK_})


		#Since eigvalues are flipped, we will aslo flip vectors
		eigVectorsFlipped=np.flip(eigVectors,1)
		
		#P matrix
		P = eigVectorsFlipped[:,0:indexK_]
		self.P = P

	def createNewShapes(self):
		'''
		Creates new shape, based on the equation x= x_bar + P*b
		x_bar, P , are created after running the function performPCA()
		b is a vector with length self.indexK_. 
		'''

		b = np.zeros((self.indexK_,1))

		#loop through b vector and change depending on the slider values in sliderArray[].
		for eig_index_ in range(self.numberOfComponents):
			min_b =-2*np.sqrt( self.eigValuesSorted[eig_index_])
			max_b =2*np.sqrt( self.eigValuesSorted[eig_index_])

			#Loop through range of b_k values

			b_k_value =min_b + (max_b-min_b)*(self.sliderArray[eig_index_].value()/100.0)
			#print("b_k_value :{}".format(b_k_value))
			b[eig_index_] = b_k_value


		#x= x_bar + P*b
		#TODO : make this better
		x_new = self.meanShapeFeature.flatten().reshape((self.meanShapeFeature.shape[0]*self.meanShapeFeature.shape[1]*self.meanShapeFeature.shape[2],1)) +np.dot(self.P,b)
		
		x_new_reshaped = x_new.reshape((	self.numNode,		self.numF ,		self.dim ))

		self.modifyFeatureVector(True,x_new_reshaped)
		

	def returnFeatureMatrix(self):
		'''
		Return the feature matrix
		'''
		return self.featureVector

	def findCurvature(self):

		'''
		TODO : Performs curvature analysis
		'''
		region  =  self._context.getDefaultRegion()
		fieldmodule = region.getFieldmodule()
		fieldmodule.beginChange()


		fieldmodule.endChange()

	
	def showLiver(self):

		'''
		Show surface and line of geometry.
		'''
		region  =  self._context.getDefaultRegion()
		scene = region.getScene()
		fieldmodule = region.getFieldmodule()
		
		coordinates= fieldmodule.findFieldByName("coordinates")

		radius= fieldmodule.findFieldByName("radius")
		group_fields_ =[]
		for group_name_ in self._embedded_geo_groupnames:
			group_fields_.append(fieldmodule.findFieldByName(group_name_))

		pca_field_= fieldmodule.findFieldByName("pca")
		materialmodule = self._context.getMaterialmodule()

		
		scene.beginChange()
		
	

		
		# '''
		# Add line
		# '''
		for group_field_ in group_fields_:

			graphicsline = scene.createGraphicsLines()
			graphicsline.setCoordinateField(self.embeddedGeo_coordinates)
			graphicsline.setSubgroupField(group_field_)
			group_name_ = group_field_.getName().lower()
			if('portal' in group_name_):
				color_ = materialmodule.findMaterialByName('blue')
			elif('arterial' in group_name_):
				color_ = materialmodule.findMaterialByName('red')

			elif('hepatic' in group_name_):
				color_ = materialmodule.findMaterialByName('cyan')
			else:
				color_ = materialmodule.findMaterialByName(self._colour_array[np.random.randint(len(self._colour_array))])
			graphicsline.setMaterial(color_)
			graphicsline_attribute = graphicsline.getGraphicslineattributes()
			if(radius.isValid()):
				graphicsline_attribute.setShapeType(Graphicslineattributes.SHAPE_TYPE_CIRCLE_EXTRUSION)
				graphicsline_attribute.setOrientationScaleField(radius)



		# '''
		# Add surface
		# '''
		graphicsline = scene.createGraphicsLines()
		graphicsline.setCoordinateField(coordinates)
		#graphicsline.setCoordinateField(self.embeddedGeo_coordinates)
		
		black = materialmodule.findMaterialByName('black')
		graphicsline.setMaterial(black)
		surface = scene.createGraphicsSurfaces()
		
		surface.setCoordinateField(coordinates)
		orange = materialmodule.findMaterialByName('orange')
		orange.setAttributeReal(orange.ATTRIBUTE_ALPHA,0.7)
		surface.setMaterial(orange)


		#surfaceLiver.setRenderPolygonMode(Graphics.RENDER_POLYGON_MODE_WIREFRAME)
		
		
		



		tessModule = scene.getTessellationmodule()
		tessModule.getDefaultTessellation()
		tessA = tessModule.createTessellation()
		tessA.setRefinementFactors([4,4,4])
		tessA.setMinimumDivisions([4,4,4])

		surface.setTessellation(tessA)
		graphicsline.setTessellation(tessA)

		scene.endChange()
		
 

	def _makeConnections(self):
		self._ui.numberComponentButton.clicked.connect(self.numberComponentButtonClicked)
		for i in range(0,self.numberOfComponents):
			self.sliderArray[i].valueChanged.connect(self.sliderChanged)
	def sliderChanged(self):
		self.createNewShapes()
		scene = self._context.getDefaultRegion().getScene()
		scene.beginChange()
		fieldmodule = self._context.getDefaultRegion().getFieldmodule()
		fieldmodule.beginChange()
		
	
		
		stored_surface_coordinates = fieldmodule.createFieldEmbedded(
			fieldmodule.findFieldByName("coordinates"),
			self.stored_surface_location)

		#self.saveRegion('a.exnode')
		self.evaluate_ngroup(
			fieldmodule, 
			stored_surface_coordinates,
			fieldmodule.findFieldByName("embeddedGeo_coordinates"), 
			self.globalNodeset,
			self.embeddedGeo_coordinates.getValueType()
			)
		fieldmodule.endChange()
		scene.endChange()
		
	def _makeDynamicSliders(self):
		#Add frame and slider depending on the number of components used
		
		
		for i in range(0,self.numberOfComponents):
		    frameComponent = QtGui.QFrame(self._ui.scrollAreaWidgetContents_2)
		    frameComponent.setMaximumSize(QtCore.QSize(16777215, 61))
		    frameComponent.setMinimumSize(QtCore.QSize(0, 61))
        
		    frameComponent.setFrameShape(QtGui.QFrame.StyledPanel)
		    frameComponent.setFrameShadow(QtGui.QFrame.Raised)
		    frameComponent.setObjectName("frameComponent"+str(i))
		    self.frameArray.append(frameComponent)
		    labelComponent = QtGui.QLabel(frameComponent)
		    labelComponent.setGeometry(QtCore.QRect(10, 10, 64, 16))
		    labelComponent.setObjectName("labelComponent"+str(i))
		    horizontalSliderComponent = QtGui.QSlider(frameComponent)
		    horizontalSliderComponent.setGeometry(QtCore.QRect(10, 29, 191, 22))
		    horizontalSliderComponent.setOrientation(QtCore.Qt.Horizontal)
		    horizontalSliderComponent.setObjectName("horizontalSliderComponent"+str(i))
		    horizontalSliderComponent.setMaximum(100)
		    horizontalSliderComponent.setValue(50) 
		    self._ui.verticalLayout_3.addWidget(frameComponent)   
		    self.sliderArray.append(horizontalSliderComponent)
		    labelComponent.setText(QtGui.QApplication.translate("MainWindow", "Component "+str(i+1), None, QtGui.QApplication.UnicodeUTF8))
		    self.labelArray.append(labelComponent)
		
	def _deleteComponentSliders(self):
		'''
		Remove slider widgets 
		'''

		#remove previous slider objects
		
		for i_ in range(len(self.frameArray)):
			self._ui.verticalLayout_3.removeWidget(self.sliderArray[i_])
			self.frameArray[i_].deleteLater()
			self.labelArray[i_].deleteLater()

		#reset arrays
		self.sliderArray=[]
		self.frameArray=[]
		self.labelArray=[]


	def numberComponentButtonClicked(self):
		'''
		If the number of pca components have changed.

		'''

		#change number of components and remake dynamic sliders
		self.numberOfComponents = int(self._ui.numberPrincipleComponent.text())
		self._deleteComponentSliders()
		self._makeDynamicSliders()
		self._makeConnections()
		self.performPCA(nComponent_=self.numberOfComponents)
		self.createNewShapes()



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)

    '''TEST TWO GEOMETRY TYPES'''
    w2 = pcaView('C:\\Users\\David Yu\\Documents\\mapclient\\mapclientplugins.zincPCAEmbedded\\mapclientplugins.zincpcastep\\example_geometries\\twocubes',
    	 'C:\\Users\\David Yu\\Documents\\mapclient\\mapclientplugins.zincPCAEmbedded\\mapclientplugins.zincpcastep\\example_geometries\\embedding',
    	 'surfacev2',
    	 ['portal','hepatic','arterial'],
    	 ['PORTAL','HEPATIC','ARTERIAL'])
    #w4 = pcaView('C:\\Users\\hyu754\\Documents\\mapclient\\fourcubes')
    #w.readAllGeometries()
    
    w2.showLiver()
    #w4.showLiver()

    w2.show()
    #w4.show()
    sys.exit(app.exec_())
