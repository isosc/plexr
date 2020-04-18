#!/usr/bin/env python3



import sys

from mpi4py import MPI
import numpy as np
import adios2
import plxr

from PIL import Image

## viewer.py
usage_msg = """Usage: extract.py <bp-file-name> <image-name>

Produces a series of images from the timesteps of the named variable
"""

def main():

    step = 0

    # Single process viewer
    comm = MPI.COMM_SELF

    print (sys.argv)


    if len(sys.argv) < 3:
        print (usage_msg)
        exit(0)

    bpfilename = sys.argv[1]
    varname = sys.argv[2]


    #Open the bpfile
    with adios2.open(bpfilename, "r", comm) as fh:
#        for fh_step in fh:
#            step = fh_step.currentstep()
#
#            schema = str(fh_step.read("%s/__plxr_schema_type"%varname),encoding='ascii')
#
#            print ("Detected schema type: %s"%schema)
#
#            if schema == "__plxr:image-rgb-8":
#                #Read the image data
#                img = fh_step.read("%s/data"%varname) 
#            pimg = Image.fromarray(img)

        print (varname)
        pimg = plxr.read_image (fh, varname, step)
        pimg.save("%s_%i.png"%(varname, step) )
        step = step + 1

#            else:
#                print ("Unknown schema type detected")
#                continue







if __name__ == "__main__":
    main()
