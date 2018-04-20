# Morph portal back to a particular iteration in the optimisation algorithm 
# where it is more convex

#read in final geometry

$MORPH_DIRECTION = 'forward'
#$MORPH_DIRECTION = 'backward'

if($MORPH_DIRECTION eq 'backward'){
	$element_file = 'liverGeometry/ellipsoid_twocubes'
	gfx read nodes 'iteration_result/surface'
	gfx read element $element_file
	gfx modify field coordinates rename surface_coordinates


	#read in portal file
	$portal_file = 'portal_segment1_v2'
	gfx read nodes 'liverGeometry/'.$portal_file
	gfx read el 'liverGeometry/'.$portal_file

	#find embedded xi ,etc.

	gfx define field find_surface_location find_mesh_location find_exact mesh surface.mesh3d mesh_field surface_coordinates source_field coordinates
	gfx define field stored_surface_location finite_element element_xi

	gfx modify nodes group portal define stored_surface_location
	gfx evaluate ngroup portal destination stored_surface_location source find_surface_location


	gfx define field stored_surface_coordinates embedded element_xi stored_surface_location field surface_coordinates


	gfx evaluate ngroup portal source stored_surface_coordinates destination coordinates

	gfx modify g_element "/" general clear;
	gfx modify g_element "/" lines domain_mesh1d subgroup portal coordinate coordinates tessellation default LOCAL circle_extrusion line_base_size 0 line_orientation_scale radius line_scale_factors 1 select_on material default selected_material default_selected render_shaded;
	gfx modify g_element "/" surfaces domain_mesh2d coordinate surface_coordinates tessellation default LOCAL select_on material gold selected_material default_selected render_wireframe;

	gfx cr win
	gfx define tessellation default minimum_divisions "4" refinement_factors "4" circle_divisions 12;

	#Morph backwards
	if(0){
		#read in i-th iteration
		$iteration_file  = 'iteration_result/surface_temp_2_iteration_6_target'
		gfx read nodes $iteration_file
		gfx evaluate ngroup portal source stored_surface_coordinates destination coordinates


		gfx write nodes portal_segment1_v2_morphback group portal field coordinates field radius
		gfx write el portal_segment1_v2_morphback group portal field coordinates field radius
	#rea
	}
}

if($MORPH_DIRECTION eq 'forward'){
	#read in i-th iteration
	$iteration_file  = 'iteration_result/iteration_morph'
	gfx read nodes $iteration_file
	$element_file = 'liverGeometry/ellipsoid_twocubes_surface_coords'
	gfx read element $element_file



	#read in generated portal file
	$portal_file = 'vessel_grown'
	gfx read nodes 'generated_results/'.$portal_file
	gfx read el 'generated_results/'.$portal_file

	gfx define field find_surface_location find_mesh_location find_exact mesh surface.mesh3d mesh_field surface_coordinates source_field coordinates
	gfx define field stored_surface_location finite_element element_xi

	gfx modify nodes group tree3 define stored_surface_location
	gfx evaluate ngroup tree3 destination stored_surface_location source find_surface_location


	gfx define field stored_surface_coordinates embedded element_xi stored_surface_location field surface_coordinates


	gfx evaluate ngroup tree3 source stored_surface_coordinates destination coordinates



	gfx modify g_element "/" general clear;
	gfx modify g_element "/" lines domain_mesh1d subgroup tree3 coordinate coordinates tessellation default LOCAL circle_extrusion line_base_size 0 line_orientation_scale radius line_scale_factors 1000 select_on material default selected_material default_selected render_shaded;
	gfx modify g_element "/" surfaces domain_mesh2d subgroup surface coordinate surface_coordinates tessellation default LOCAL select_on material grey25 selected_material default_selected render_wireframe;
	
	gfx cr win
	gfx define tessellation default minimum_divisions "4" refinement_factors "4" circle_divisions 12;

	if(0){
		gfx read nodes iteration_result/surface_final
		gfx read el iteration_result/surface_final

		gfx evaluate ngroup tree3 source stored_surface_coordinates destination coordinates
	}

}

