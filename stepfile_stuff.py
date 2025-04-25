import numpy as np

def product_definition(idx):
    # Dumb bullshit ->
    # psd_idx = input idx
    idx += 1
    s =  "#{n1} = PRODUCT_DEFINITION_SHAPE ( 'NONE', 'NONE',  #{n2} ) ;\n".format(n1 = idx, n2 = idx+1)
    s += "#{n2} = PRODUCT_DEFINITION ( 'UNKNOWN', '', #{n3}, #{n7} ) ;\n".format(n2 = idx+1, n3 = idx+2, n7 = idx+6)
    s += "#{n3} = PRODUCT_DEFINITION_FORMATION_WITH_SPECIFIED_SOURCE ( 'ANY', '', #{n4}, .NOT_KNOWN. ) ;\n".format(n3 = idx+2, n4 = idx+3)
    s += "#{n4} = PRODUCT ( 'SOLID1_AP214', 'SOLID1_AP214', '', ( #{n5} ) ) ;\n".format(n4 = idx+3, n5 = idx+4)
    s += "#{n5} = PRODUCT_CONTEXT ( 'NONE', #{n6}, 'mechanical' ) ;\n".format(n5 = idx+4, n6 = idx+5)
    s += "#{n6} = APPLICATION_CONTEXT ( 'automotive_design' ) ;\n".format(n6 = idx +5)
    s += "#{n7} = PRODUCT_DEFINITION_CONTEXT ( 'detailed design', #{n8}, 'design' ) ;\n".format(n7 = idx+6, n8 = idx+7)
    s += "#{n8} = APPLICATION_CONTEXT ( 'automotive_design' ) ;\n".format(n8 = idx + 7) # Could this simply point to n6 instead, who knows. Do I care: no.
    s += "#{n9} = APPLICATION_PROTOCOL_DEFINITION ( 'draft international standard', 'automotive_design', 1998, #{n6} ) ;\n".format(n9 = idx + 8, n6 = idx + 5)
    s += "#{n10} = APPLICATION_PROTOCOL_DEFINITION ( 'draft international standard', 'automotive_design', 1998, #{n8} ) ;\n".format(n10 = idx+9, n8 = idx + 7)
    s += "#{n11} = PRODUCT_RELATED_PRODUCT_CATEGORY ( 'part', '', ( #{n4} ) ) ;\n".format(n11 = idx +10, n4 = idx + 3)
    idx += 11 

    return s, idx

def advanced_brep_shape_rep(idx: int, adv_Faces:list, filename: str):
    # Creates ADVANCED_BREP_SHAPE_REPRESENTATION
    # from a list of advanced faces. 

    # Create axis:
    s = """#{n1} = AXIS2_PLACEMENT_3D ( 'NONE', #{n2}, #{n3}, #{n4} ) ;
#{n2} = CARTESIAN_POINT ( 'NONE',  ( 0.000000000000000000, 0.000000000000000000, 0.000000000000000000 ) ) ;
#{n3} = DIRECTION ( 'NONE',  ( 0.000000000000000000, 0.000000000000000000, 1.000000000000000000 ) ) ;
#{n4} = DIRECTION ( 'NONE',  ( 1.000000000000000000, 0.000000000000000000, 0.000000000000000000 ) ) ;
""".format(n1 = idx, n2 = idx+1, n3 = idx+2, n4 = idx+3)
    axis_idx = idx
    idx += 4

    # Create unit definition(?)
    s += """#{n1} =( GEOMETRIC_REPRESENTATION_CONTEXT ( 3 ) GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT ( ( #{n2} ) ) GLOBAL_UNIT_ASSIGNED_CONTEXT ( ( #{n3}, #{n4}, #{n5} ) ) REPRESENTATION_CONTEXT ( 'NONE', 'WORKASPACE' ) );
#{n2} = UNCERTAINTY_MEASURE_WITH_UNIT (LENGTH_MEASURE( 1.000000000000000082E-05 ), #{n3}, 'distance_accuracy_value', 'NONE');
#{n3} =( LENGTH_UNIT ( ) NAMED_UNIT ( * ) SI_UNIT ( .MILLI., .METRE. ) );
#{n4} =( NAMED_UNIT ( * ) PLANE_ANGLE_UNIT ( ) SI_UNIT ( $, .RADIAN. ) );
#{n5} =( NAMED_UNIT ( * ) SI_UNIT ( $, .STERADIAN. ) SOLID_ANGLE_UNIT ( ) );
""".format(n1 = idx, n2 = idx+1, n3 = idx+2, n4 = idx+3, n5 = idx+4)
    units_idx = idx
    idx += 5

    adv_face_idx_str = ""

    # Create manifold solid from advanced faces:
    for face in adv_Faces:
         s_face, idx = Advanced_face_stp(idx, face)
         adv_face_idx_str += " #{n},".format(n = idx-1)
         s += s_face
    
    s += "#{} = CLOSED_SHELL ( 'NONE', (".format(idx) + adv_face_idx_str[:-1] + " ) ) ;\n"
    idx += 1
    s += "#{n} = MANIFOLD_SOLID_BREP ( 'NONE', #{closed_shell} ) ;\n".format(n = idx, closed_shell = idx-1)
    idx += 1
    s += "#{n} = ADVANCED_BREP_SHAPE_REPRESENTATION ( '{name}_AP214', ( #{manifold_brep}, #{axis} ), #{unit} ) ;".format(n = idx, name = filename, manifold_brep = idx-1, axis = axis_idx, unit = units_idx)
    return s, idx

def manifold_surface_shape_rep(idx: int, adv_Faces:list, filename: str):
    # Creates manifold_surface_shape_representation
    # from a list of advanced faces. 

    # Create axis:
    s = """#{n1} = AXIS2_PLACEMENT_3D ( 'NONE', #{n2}, #{n3}, #{n4} ) ;
#{n2} = CARTESIAN_POINT ( 'NONE',  ( 0.000000000000000000, 0.000000000000000000, 0.000000000000000000 ) ) ;
#{n3} = DIRECTION ( 'NONE',  ( 0.000000000000000000, 0.000000000000000000, 1.000000000000000000 ) ) ;
#{n4} = DIRECTION ( 'NONE',  ( 1.000000000000000000, 0.000000000000000000, 0.000000000000000000 ) ) ;
""".format(n1 = idx, n2 = idx+1, n3 = idx+2, n4 = idx+3)
    axis_idx = idx
    idx += 4

    # Create unit definition(?)
    s += """#{n1} =( GEOMETRIC_REPRESENTATION_CONTEXT ( 3 ) GLOBAL_UNCERTAINTY_ASSIGNED_CONTEXT ( ( #{n2} ) ) GLOBAL_UNIT_ASSIGNED_CONTEXT ( ( #{n3}, #{n4}, #{n5} ) ) REPRESENTATION_CONTEXT ( 'NONE', 'WORKASPACE' ) );
#{n2} = UNCERTAINTY_MEASURE_WITH_UNIT (LENGTH_MEASURE( 1.000000000000000082E-05 ), #{n3}, 'distance_accuracy_value', 'NONE');
#{n3} =( LENGTH_UNIT ( ) NAMED_UNIT ( * ) SI_UNIT ( .MILLI., .METRE. ) );
#{n4} =( NAMED_UNIT ( * ) PLANE_ANGLE_UNIT ( ) SI_UNIT ( $, .RADIAN. ) );
#{n5} =( NAMED_UNIT ( * ) SI_UNIT ( $, .STERADIAN. ) SOLID_ANGLE_UNIT ( ) );
""".format(n1 = idx, n2 = idx+1, n3 = idx+2, n4 = idx+3, n5 = idx+4)
    units_idx = idx
    idx += 5

    openshell_idx_str = ""

    # Create manifold solid from advanced faces:
    for face in adv_Faces:
         s_face, idx = Advanced_face_stp(idx, face)
         s += s_face
         s += "#{n} = OPEN_SHELL ( 'NONE', ( #{adv_face} ) ) ;\n".format(n = idx, adv_face = idx-1)
         openshell_idx_str += " #{n},".format(n = idx)
         idx += 1

    s += "#{n} = SHELL_BASED_SURFACE_MODEL ( 'NONE', ( {openshells} ) );\n".format(n = idx, openshells = openshell_idx_str[:-1])
    idx += 1
    s += "#{n} = MANIFOLD_SURFACE_SHAPE_REPRESENTATION ( '{filename}', ( #{shell_based_surface_model}, #{axis} ), #{unit} ) ;\n".format(
        n = idx, filename = filename, shell_based_surface_model = idx-1, axis = axis_idx, unit = units_idx )
    
    return s, idx

def Advanced_face_stp(idx, surface):
    """Creates all the bullshit that .step requires to construct a B_SPLINE_CURVE_WITH_KNOTS as an ADVANCED_FACE"""
    #   LOOK AT ALL THIS BULLSHIT: 
    #   ADVANCED_FACE 
    #   ├─ FACE_OUTER_BOUND
    #   │  └─ EDGE_LOOP
    #   │     └─ ORIENTED_CURVE (x4)
    #   │        └─ EDGE_CURVE
    #   │           ├─ VERTEX_POINT
    #   │           │  └─ CARTESIAN_POINT
    #   │           ├─ VERTEX_POINT
    #   │           │  └─ CARTESIAN_POINT
    #   │           └─ B_SPLINE_CURVE_WITH_KNOTS
    #   │              └─ CARTESIAN_POINTS (x?)
    #   └─ B_SPLINE_SURFACE_WITH_KNOTS
    #      └─ CARTESIAN_POINTS (x?)

    # idx = start index
    p = surface.POLYNOMIAL_DEGREE
    P = surface.CONTROL_NODES
    Cn = surface.CONTROL_NODE_REFERENCES

    edge_loop = "#{n} = EDGE_LOOP ( 'NONE', ( #{oc0}, #{oc1}, #{oc2}, #{oc3} ) ) ;\n"
    face_outer_bound = "#{n} = FACE_OUTER_BOUND ( 'NONE', #{el}, .T. ) ;\n"
    advanced_face = "#{n} = ADVANCED_FACE ( 'NONE', ( #{fob} ), #{surface}, .T. ) ;\n"

    s = ""
    # Create the face outer bound:

    # boundary = np.stack([
    #     Cn[0,:],
    #     Cn[:,-1],
    #     np.flip(Cn[-1,:]),
    #     np.flip(Cn[:,0]),
    # ])
    boundary = {
        "0": Cn[0,:],
        "1": Cn[:,-1],
        "2": np.flip(Cn[-1,:]),
        "3": np.flip(Cn[:,0])}

    ocs = [] # oriented curves

    for i in range(4):
        # Pb = P[Cn[i,:]]
        Pb = P[boundary[str(i)]]
        soc, idx = oriented_curve(idx, Pb, p)
        s += soc
        ocs.append(idx-1)

    s += edge_loop.format(n = idx, oc0 = ocs[0], oc1 = ocs[1], oc2 = ocs[2], oc3 = ocs[3] ) 
    idx += 1
    s += face_outer_bound.format(n = idx, el = idx-1)
    fob_idx = idx # face outer bound index. 
    idx += 1

    s_surf, idx = B_spline_surface_step(idx, surface)
    s += s_surf

    s+= advanced_face.format(n = idx, fob = fob_idx, surface = idx-1, )

    idx += 1

    return s, idx

def shape_def_rep_Step(idx:int, pds_idx: int, msr_idx: int, s: str, filename: str):
    """
    creates the "top level" SHAPE_DEFINITION_REPRESENTATION for the step file.
    requires:
    idx -> next index to write
    PRODUCT_DEFINITION_SHAPE #pds_idx
    MANIFOLD SURFACE REPRESENTATION #msr_idx
    s -> string containing PDS and ABSR

    SHAPE_DEFINITION_REPRESENTATION
    ├─ MANIFOLD_SURFACE_SHAPE_REPRESENTATION
    └─ PRODUCT_DEFINITION_SHAPE 
    """
    
    header = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION (( 'STEP AP214' ),
    '1' );
FILE_NAME ('{name}.STEP',
    '2025-01-01T10:00:00',
    ( '!!!! NOT FOR COMMERCIAL USE !!!!' ),
    ( 'Christian von Koldskaal' ),
    'Product ENgineering with Intuitive Surfacing',
    '!!!! PENIS v0.1 !!!!',
    '' );
FILE_SCHEMA (( 'AUTOMOTIVE_DESIGN' ));
ENDSEC;

DATA;\n""".format(name = filename)

    end_of_file = """\nENDSEC;
END-ISO-10303-21;"""

    s = header + s
    s += "#{n} = SHAPE_DEFINITION_REPRESENTATION ( #{pds}, #{msr} ) ;".format(n = idx, pds = pds_idx, msr = msr_idx)
    s+= end_of_file

    return s


def oriented_curve(idx, P , p):
    vertex = "#{n} = VERTEX_POINT ( 'NONE', #{cart_idx} ) ;\n"
    edge_curve = "#{n} = EDGE_CURVE ( 'NONE', #{v1}, #{v2}, #{curve}, .T. ) ;\n"
    or_edge = "#{n} = ORIENTED_EDGE ( 'NONE', *, *, #{edge_curve}, .T. ) ;\n"
    
    # Vertex 1:
    s = cart_point(idx, P[0])
    idx += 1
    s +=  vertex.format(n = idx, cart_idx = idx-1)
    v1_idx = idx
    idx += 1

    # Vertex 2:
    s += cart_point(idx, P[-1])
    idx += 1
    s+= vertex.format(n= idx, cart_idx = idx-1)
    v2_idx = idx
    idx += 1

    s_curve, idx =  B_spline_curve_step(idx, P, p) 
    s += s_curve
    # #1 = EDGE_CURVE ( 'NONE', #53, #18, #85, .T. ) ;
    s += edge_curve.format(n = idx, v1 = v1_idx, v2 = v2_idx, curve = idx-1)
    idx += 1
    s += or_edge.format(n = idx, edge_curve = idx -1)
    idx += 1

    return s, idx

def cart_point(idx, pt):  
    cart_point = "#{n}  = CARTESIAN_POINT ( 'NONE',  ( {x:.10f}, {y:.10f}, {z:.10f} ) ) ;\n"
    s = cart_point.format(n = idx, x = pt[0], y = pt[1], z = pt[2])
    return s

def B_spline_curve_step(idx, P, p):
#     #26 = B_SPLINE_CURVE_WITH_KNOTS ( 'NONE', 3,
#  ( #65, #40, #3, #14 ),
#  .UNSPECIFIED., .F., .F.,
#  ( 4, 4 ),
#  ( 0.000000000000000000, 1.000000000000000000 ),
#  .UNSPECIFIED. ) ;
    s = ""
    cart_pts = ""

    # Create all cartesian points: 
    for pt in P:
        s += cart_point(idx, pt)
        cart_pts += "#{}, ".format(idx)
        idx += 1

    # Create the Spline itself: 
    s += "#{n} = B_SPLINE_CURVE_WITH_KNOTS ( 'NONE', {pi},\n".format(n = idx, pi = p)
    s += "( " + cart_pts[:-2] + "),\n" # [:-1] to remove the last comma
    s += ".UNSPECIFIED., .F., .F.,\n"
    s += "( "
    n_knots = len(P)-p + 1
    for i in range(n_knots):
        if i == 0:
            s += "{}, ".format(p+1)
        elif i == n_knots-1:
            s += "{} ),\n".format(p+1)
        else:
            s += "{}, ".format(1)
       
    s += "( "
    U = np.linspace(0, 1, n_knots)
    for i in range(n_knots):
        if i == n_knots-1:
            s += "{:.10f} ".format(U[i])
        else:
            s += "{:.10f}, ".format(U[i])
    s+= "), \n .UNSPECIFIED. ) ;\n"

    idx += 1

    return s, idx

def B_spline_surface_step(idx, surface):
# Example: 
# #16 = B_SPLINE_SURFACE_WITH_KNOTS ( 'NONE', 3, 3, ( 
#  ( #36, #60, #37, #74, #55 ),
#  ( #21, #31, #72, #23, #49 ),
#  ( #12, #56, #51, #32, #82 ),
#  ( #7, #25, #44, #22, #61 ) ),
#  .UNSPECIFIED., .F., .F., .F.,
#  ( 4, 4 ),
#  ( 4, 1, 4 ),
#  ( 0.000000000000000000, 1.000000000000000000 ),
#  ( 0.000000000000000000, 0.5650950645287347029, 1.000000000000000000 ),
#  .UNSPECIFIED. ) ;
    p = surface.POLYNOMIAL_DEGREE
    P = surface.CONTROL_NODES
    Cn = surface.CONTROL_NODE_REFERENCES
    # pi = face["pi"]
    # pj = face["pj"]
    # P = face["P"]
    # Cn = face["Cn"]

    cart_pts = ""
    (ni, nj) = np.shape(Cn)
    s = ""
    # Create all the cartesian points. 
    for i in range(ni):
        for j in range(nj):
            s += cart_point(idx, P[Cn[i,j]])
            if j == 0:
                cart_pts += "( #{}, ".format(idx)
            elif j == nj-1:
                if i == ni-1:
                    cart_pts += "#{} ) ),\n".format(idx) # ) ),
                else:
                    cart_pts += "#{} ),\n".format(idx)
            else:
                cart_pts += "#{}, ".format(idx)
            idx += 1

    # Create the surface: 
    s += "#{n} = B_SPLINE_SURFACE_WITH_KNOTS ( 'NONE', {p1}, {p2}, (\n".format(n = idx, p1 = p, p2 = p)
    s += cart_pts
    s += ".UNSPECIFIED., .F., .F., .F.,\n"

    # Knot vector, i:
    s += "( "
    n_knots_i = ni-p + 1
    for i in range(n_knots_i):
        if i == 0:
            s += "{}, ".format(p+1)
        elif i == n_knots_i-1:
            s += "{} ),\n".format(p+1)
        else:
            s += "{}, ".format(1)
    
    # Knot vector, j:
    s += "( "
    n_knots_j = nj-p + 1
    for j in range(n_knots_j):
        if j == 0:
            s += "{}, ".format(p+1)
        elif j == n_knots_j-1:
            s += "{} ),\n".format(p+1)
        else:
            s += "{}, ".format(1)

    # Knot locations, i: 
    s += "( "
    Ui = np.linspace(0, 1, n_knots_i)
    for i in range(n_knots_i):
        if i == n_knots_i-1:
            s += "{:.10f} ".format(Ui[i])
        else:
            s += "{:.10f}, ".format(Ui[i])
    s+= "), \n"

    # Knot locations, j: 
    s += "( "
    Uj = np.linspace(0, 1, n_knots_j)
    for i in range(n_knots_j):
        if i == n_knots_j-1:
            s += "{:.10f} ".format(Uj[i])
        else:
            s += "{:.10f}, ".format(Uj[i])
    s+= "), \n"

    # End of surface:     
    s+= ".UNSPECIFIED. ) ;\n"
    idx += 1

    return s, idx