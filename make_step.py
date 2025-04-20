from math_stuff import *
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( "filename", type = str, help = "Name of file that contains the points." )
    parser.add_argument( "-p", "--degree", type = int, default = 3, help = "Polynomial degree of the surface" )
    parser.add_argument( "-n", "--stpfilename", type = str, default= "")

    args = parser.parse_args()

    if args.stpfilename == "":
        stpfilename = args.filename.split(".")[0]
    else:
        stpfilename = args.stpfilename

    points = read_n_parse_Surface_txt( filename= args.filename )
    surfs = multiSurfacePart( points, p = args.degree)
    surfs.construct_step( stpfilename )

if __name__ == "__main__":
    main()