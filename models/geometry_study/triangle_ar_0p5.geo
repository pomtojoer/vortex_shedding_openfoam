// Gmsh project created on Mon Feb 22 15:28:21 2021

// ********************  control  ********************
// Dimensions
diamond_thickness = 0.5;
diamond_length = 5/20;
outer_cir_rad = 1.5;
xmax = 25;
xmin = -10;
ymax = 10;
ymin = -10;
zmax = 1;

// Circle Mesh Controls
Nc = 126;
Rc = 1;

// Y-direction Mesh Controls
Ny_outer = 91;
Ry_outer = 1;

Ny_inner = 31;

// X-direction Mesh Controls
Nx_outer_right = 256;
Nx_outer_left = 91;

Nx_inner = 31;

// Z-direction Mesh Controls
Nz = 1;
// ********************************************************

// ********************  points  ********************
// Outer bounds
Point(1) = {xmin, ymax, 0, 1.0};
Point(2) = {xmax, ymax, 0, 1.0};
Point(3) = {xmax, ymin, 0, 1.0};
Point(4) = {xmin, ymin, 0, 1.0};

// Outer cicular points
Point(5) = {outer_cir_rad, outer_cir_rad, 0, 1.0};
Point(6) = {-outer_cir_rad, outer_cir_rad, 0, 1.0};
Point(7) = {outer_cir_rad, -outer_cir_rad, 0, 1.0};
Point(8) = {-outer_cir_rad, -outer_cir_rad, 0, 1.0};

// Intermediate outer bounds
Point(9) = {xmin, outer_cir_rad, 0, 1.0};
Point(10) = {xmin, -outer_cir_rad, 0, 1.0};
Point(11) = {-outer_cir_rad, ymin, 0, 1.0};
Point(12) = {-outer_cir_rad, ymax, 0, 1.0};
Point(13) = {outer_cir_rad, ymax, 0, 1.0};
Point(14) = {outer_cir_rad, ymin, 0, 1.0};
Point(15) = {xmax, outer_cir_rad, 0, 1.0};
Point(16) = {xmax, -outer_cir_rad, 0, 1.0};

// Midpoint
Point(17) = {0, 0, 0, 1.0};

//  Inner points
Point(18) = {-diamond_length, 0, 0, 1.0};
Point(19) = {diamond_length, -diamond_thickness, 0, 1.0};
Point(20) = {diamond_length, diamond_thickness, 0, 1.0};
// Point(21) = {diamond_length, -diamond_thickness, 0, 1.0};
// ********************************************************

// ********************  lines  ********************
// // Bounding box
Line(1) = {1, 9};
Line(2) = {9, 10};
Line(3) = {10, 4};
Line(4) = {4, 11};
Line(5) = {11, 14};
Line(6) = {14, 3};
Line(7) = {3, 16};
Line(8) = {16, 15};
Line(9) = {15, 2};
Line(10) = {2, 13};
Line(11) = {13, 12};
Line(12) = {12, 1};

// Cross lines
Line(13) = {9, 6};
Line(14) = {10, 8};
Line(15) = {11, 8};
Line(16) = {14, 7};
Line(17) = {16, 7};
Line(18) = {15, 5};
Line(19) = {13, 5};
Line(20) = {12, 6};

// Outer circle
Circle(21) = {6, 17, 8};
Circle(22) = {8, 17, 7};
Circle(23) = {7, 17, 5};
Circle(24) = {5, 17, 6};

// Inner lines
Line(25) = {20, 19};
Line(26) = {19, 18};
Line(27) = {18, 20};

// Line(26) = {19, 21};
// Line(27) = {21, 18};
// ********************************************************

// ********************  Surfaces  ********************
// Outer domain
Curve Loop(1) = {1, 13, -20, 12};
Plane Surface(1) = {1};
Curve Loop(2) = {11, 20, -24, -19};
Plane Surface(2) = {2};
Curve Loop(3) = {10, 19, -18, 9};
Plane Surface(3) = {3};
Curve Loop(4) = {8, 18, -23, -17};
Plane Surface(4) = {4};
Curve Loop(5) = {7, 17, -16, 6};
Plane Surface(5) = {5};
Curve Loop(6) = {5, 16, -22, -15};
Plane Surface(6) = {6};
Curve Loop(7) = {4, 15, -14, 3};
Plane Surface(7) = {7};
Curve Loop(8) = {2, 14, -21, -13};
Plane Surface(8) = {8};

// Inner domain
Curve Loop(9) = {24, 21, 22, 23};
Curve Loop(10) = {25, 26, 27};
Plane Surface(9) = {9, 10};
// ********************************************************

// ********************  Recombine  ********************
Recombine Surface {1, 2, 3, 4, 5, 6, 7, 8};
// ********************************************************

// // ********************  Setting mesh points  ********************
// Outer domain
Transfinite Curve {1, 20, 19, 9} = Ny_outer Using Progression 1;
Transfinite Curve {3, 15, 16, 7} = Ny_outer Using Progression 1;

Transfinite Curve {12, 13, 14, 4} = Nx_outer_left Using Progression 1;
Transfinite Curve {10, 18, 17, 6} = Nx_outer_right Using Progression 1;

// Cross domain
Transfinite Curve {2, 21} = Ny_inner Using Progression 1;
Transfinite Curve {8, 23} = Ny_inner Using Progression 1;

Transfinite Curve {11, 24} = Nx_inner Using Progression 1;
Transfinite Curve {5, 22} = Nx_inner Using Progression 1;

// Inner domain
Transfinite Curve {25} = Nc Using Progression 1;
Transfinite Curve {28} = Nc Using Progression 1;
Transfinite Curve {27} = Nc Using Progression 1;
Transfinite Curve {26} = Nc Using Progression 1;
// ********************************************************

// ********************  Mesh surfaces  ********************
Transfinite Surface {1};
Transfinite Surface {2};
Transfinite Surface {3};
Transfinite Surface {4};
Transfinite Surface {5};
Transfinite Surface {6};
Transfinite Surface {7};
Transfinite Surface {8};
// ********************************************************

// ********************  Make 3D  ********************
Extrude {0, 0, zmax} {
  Surface{1,2,3,4,5,6,7,8,9};
  Layers{Nz};
  Recombine;
}
// ********************************************************

// ********************  Physical planes  ********************
Physical Surface("in") = {36, 190, 180};
Physical Surface("out") = {92, 102, 124};
Physical Surface("sym2") = {168, 146, 136};
Physical Surface("sym1") = {48, 58, 80};
Physical Surface("back") = {1, 2, 3, 4, 5, 6, 7, 8, 9};
Physical Surface("front") = {49, 71, 93, 115, 137, 159, 181, 203, 240};
Physical Surface("obstacle") = {231, 235, 239};
// ********************************************************

// ********************  Physical Volume  ********************
Physical Volume("internal") = {1, 2, 3, 4, 5, 6, 7, 8, 9};
// ********************************************************