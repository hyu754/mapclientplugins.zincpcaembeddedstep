$object='twocube';
$off=100;
$offi=1000;
$offd=0;
$tot_itt=5;

fem def para;r;$object;example       # Declares array dimensions   
fem def coord;r;$object;example      # Defines the coordinate system
fem def nodes;r;onecube;example      # Reads in nodal information
fem def bases;r;$object;example      # Defines tri-cubic Hermite basis functions
fem def element;r;onecube;example    # Reads in element information

fem update nodes derivative 1 linear # Updates the derivatives in all three
fem update nodes derivative 2 linear # xi directions
fem update nodes derivative 3 linear #


fem export node;${object}_initial as ${object}_initial offset $offi
fem export elem;${object}_initial as ${object}_initial offset_node $offi offset_elem $offi

#fem def field;r;$object;example      # Reads in field variables
#fem def elem;r;$object;example field # Defines connectivity of field variables
#fem update field from geometry       # Updates field 

# Instead of using the above 3 lines to read in a predefined field
# the following could be used to create is automatically. The created
# field will have the same topology as the geometry.
fem update field from geometry       # Updates field 
fem def elem;d  field

#fem group faces 1,3..11 as FFFFF     # Defines face group

# The faces could also be grouped using this command which
# avoids having to know what the face numbers are.
fem group faces allfaces external as FFFFF     # Defines face group

fem def data;r;$object;example       # Reads in data information     

fem def xi;c closest_face faces FFFFF           # Projects data onto faces
                                                # only in group FFFFF. 
#fem def xi;w;twocube closest_face faces FFFFF   # Writes out xi positions
                                                # of the projections.
fem export data;${object}_initial_error error as ${object}_initial_error
								     
# Note that *.ipxi should contain DATA PT. NO., ELEM NO., LOCAL FACE NO., xi1, xi2 and xi3.

fem li data error                    # Lists initial data error

# Fitting is done iteratively. In this case three iterations. Since we do linear
# fitting, after each fit, scale factors are updated which results in change   
# in the shape of the fitted mesh. Thus, re-projection of data points onto the 
# new mesh is required prior to determining the error. Also note that for each 
# iteration, a new *.ipfit is read in. This helps to relax the Sobelov weights 
# gradually.
 
for ($fit_itt=1; $fit_itt<=$tot_itt; $fit_itt=$fit_itt+1)
  {
   fem def fit;r;onecube_${fit_itt};example geometry faces FFFFF 
   fem fit
   fem update node fit
   fem update scale_factor normalise
   fem de xi;c closest_face faces FFFFF #old
   fem li data error
   system "echo ' ================' " 
   system "echo ' ITERATION ${fit_itt} DONE' "
   system "echo ' ================' "
  }

$output_file = 'twocubes'
$output_file = 'threecubes'
$output_file = 'fourcubes'
$output_file = 'fivecubes'
$output_file = 'onecube'




fem export data;${object}_fitted_error error as ${object}_fitted_error offset $offd 
fem export nodes;$output_file  as surface offset $off
fem export elem;$output_file  as surface offset_node $off offset_elem $off
