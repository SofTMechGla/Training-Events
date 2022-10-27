algebraic3d

#
# Generates a pan/pot
#

solid BiggerCylinder = cylinder ( 0, 0, 0.4; 0, 0, 0; 1.0 )
			and plane (0, 0, 0.4; 0, 0, 1) and  plane (0, 0, 0; 0, 0, -1);

solid SmallerCylinder = cylinder ( 0, 0, 0.4; 0, 0, 0.1; 0.9 ) 
			 and plane (0, 0, 0.4; 0, 0, 1) and  plane (0, 0, 0.1; 0, 0, -1);

solid Handle = orthobrick (-3,-0.08,0.17;-0.5,0.08,0.23);

solid Pan = (BiggerCylinder or Handle) and not SmallerCylinder -maxh = 0.1;

tlo Pan;
