import numpy as np
import re
from stepfile_stuff import *
# np.set_printoptions(precision=3)

class multiSurfacePart():
    def __init__(self, surfaces: dict, p: int):
        self.surfaces = []
        for surf in surfaces.keys():
            self.add_surface(P = surfaces[surf], p = (p, p))
        pass
    
    def add_surface(self, P, p):
        self.surfaces.append( BsplineSurface(P, p) )
 
    def construct_step(self, filename):
        print("Creating 'MANIFOLD SURFACE SHAPE REPRESENTATION', and a bunch of other intuitively named stuff...")
        idx = 1
        s_manifold, idx = manifold_surface_shape_rep(idx, self.surfaces, filename)
        s = s_manifold
        idx_manifold = idx

        print("Creating 'PRODUCT DEFINITION SHAPE' ")
        s_psd, idx = product_definition(idx)
        s += s_psd
        idx_psd = idx-11
        print("Completing step file contents")
        s1 = shape_def_rep_Step(idx, idx_psd, idx_manifold, s, filename)
        
        print("Writing stepfile")
        file = filename + ".step"
        f = open(file, "w+")
        f.write(s1)
        f.close()
        print("Done")


class BsplineSurface():
    def __init__(self, P, p, given_points = "points on surface"):
        """Initialize the surface with a grid of controlnodes, P 
        and a tuple of the degrees along i an j, p e.g. p = (3,3) for bicubic"""
        
        self.P = P
        self.Px , self.Py , self.Pz = P 
        self.POLYNOMIAL_DEGREE_i, self.POLYNOMIAL_DEGREE_j = p
        self.POLYNOMIAL_DEGREE = p[0] 

        if given_points == "points on surface":
            self.get_controlnode_locations()

        pass

    def get_controlnode_locations(self):
        ni, nj = np.shape(self.Px)
        n = ni*nj 
        A = np.zeros( (n, n) ) # Prealloker A matrix 

        Bu = B_spline( P = np.zeros( (ni,3) ), p = self.POLYNOMIAL_DEGREE_i)
        Bv = B_spline( P = np.zeros( (nj,3) ), p = self.POLYNOMIAL_DEGREE_j)
        Bu.pointOfMaxInfluence()
        Bv.pointOfMaxInfluence()
        Bu_pmi = Bu.pmi
        Bv_pmi = Bv.pmi
        
        for j in range(nj): # Konstruer A matrix til at finde kontrolpunkt placeringer ud fra punkter på overfladen. 
            Nv = Bv.basisVals(Bv_pmi[j])
            for i in range(ni):
                Nu = Bu.basisVals(Bu_pmi[i])
                N = np.outer( Nu, Nv )
                A[i + ni*j,:] = np.ravel(N)
         
        self.CONTROL_NODES = np.zeros( (n, 3) )
        for d in range(3):
            B = self.P[d,:] # B-vector is the X,Y or Z coordinate of the referencepoints, through which we want the B-surf to flow. 
            c = np.linalg.solve( A, B.flatten(order='F') )
            self.CONTROL_NODES[:,d] = c
        
        self.CONTROL_NODE_REFERENCES = np.arange(n).reshape(ni, nj)


def read_n_parse_Surface_txt(filename):
    with open(filename, "r") as file:
        text = file.read()

    surfs_dict = {}

    surfaces = re.findall(r'Surface\d+\((.*?)\)SurfaceEnd', text, re.DOTALL)
    for i, surface in enumerate(surfaces):
        # Find alle Section-blokke
        sections_raw = re.findall(r'Section\d+\((.*?)\)SectionEnd', surface, re.DOTALL)

        all_sections = []

        for section in sections_raw:
            # Find alle (x;y;z)-punkter
            points_raw = re.findall(r'\(([^)]+)\)', section)
            section_points = []

            for point_str in points_raw:
                coords = list(map(float, point_str.split(';')))
                section_points.append(coords)

            all_sections.append(section_points)

        # Konverter til NumPy-array
        P = np.array(all_sections)
        P = np.transpose(P, (2, 1, 0))

        surfs_dict[str(i)] = P

    return surfs_dict

class B_spline:
    """Creates a clamped, B-spline from a list of knots: P, and a curve degree: p.
    Default knotspacing is cosine. 
    Use distribution = "uniform" for uniform knot spacing."""
    def __init__(self, P, p) -> None:
        self.P = P
        self.p = p
        ### Create Knotvector: 
        self.n = len(P)-1
        self.d = len(P[0])
        min_n_knots = 2*(p+1)
        self.m = self.n+p+1
        if self.m+1 < min_n_knots:
            raise TypeError("Cannot create knot vector, check input. NB! order must be p <= n")
        
        # create the middle knots first:
        self.U = np.linspace(0,1, self.m+1-2*p) 
        # Then pad on either side with edge multiplicities: 
        self.U = np.concatenate( (np.zeros(p), self.U, np.ones(p) ), axis = 0 )

    def zeroOrderBasisFuns(self, u):
        """Determine the 0'th order basis function values at a particular u"""
        U = self.U
        U[-1] *= (1.0+ 1e-9)
        N0 = np.zeros(self.m)
        for i in range(self.m):
            if U[i] <= u and u < U[i+1]:
                N0[i] = 1
        
        return N0

    def basisVals(self, u):
        N0 = self.zeroOrderBasisFuns(u)
        for pi in range(1, self.p+1):
            Ni = np.zeros( len(N0)-1 )
            for i in range( len(Ni) ):
                # Determine the coefficients of the previous order basis functions. 
                # Here divide by 0 error may occur, so some checks are needed beforehand.
                # Denominator might become 0 in multiplicity knots, but nowhere else.
                # The basis value of intervals between multiplicity knots is zero, so this can be used as a check
                # Contribution from north west basis value: 
                if abs( N0[i] ) < 1e-6:
                    nw = 0
                else:
                    nw = N0[i] * ( u - self.U[i] )/( self.U[i+pi] - self.U[i] )

                # Contribution from south west basis value: 
                if abs( N0[i+1] ) < 1e-6:
                    sw = 0
                else:
                    sw = N0[i+1] * ( self.U[i+pi+1] - u )/( self.U[i+pi+1] - self.U[i+1] )

                Ni[i] = nw + sw
            del N0
            N0 = Ni

        return Ni

    def solveAt_u(self, u):
        (_, d) = np.shape(self.P) # d = number of dimensions. 
        B = np.zeros(d)
        N = self.basisVals(u)
        for i in range(d):
            B[i] = np.matmul(self.P[:,i], N)

        return B

    def pointOfMaxInfluence(self):
        """Finds the points of max influence for the basisfunctions, and stores them in self.pmi, returns nothing"""
        self.pmi = np.zeros(self.n+1)
        n1 = 300
        n2 = 100
        u = np.linspace(0, 1, n1)
        for i in range(self.n+1):
            if i == 0:
                self.pmi[0] = 0
                k_last = 0
            elif i == self.n:
                self.pmi[-1] = 1
            else: 
                N_last = self.basisVals( u[k_last] )[i]
                for k in range(k_last, n1):
                    N_new = self.basisVals( u[k] )[i]
                    if N_new < N_last:
                        k_last = k-1
                        break
                    
                    N_last = N_new

                u2 = np.linspace(u[k-1], u[k], n2)
                N_last = self.basisVals( u2[0] )[i]
                for k in range(1,n2):
                    N_new = self.basisVals( u2[k] )[i]
                    if N_new < N_last:
                        break
                    
                    N_last = N_new
                self.pmi[i] = u2[k-1]

    def createWeightMatrix(self):
        if not hasattr(self, "pmi"): # Check if pointOfMaxInfluence was run already. 
            self.pointOfMaxInfluence()

        A = np.zeros( (self.n+1, self.n+1) )
        for i in range( self.n+1 ):
            A[i,:] = self.basisVals(self.pmi[i])

        return A

