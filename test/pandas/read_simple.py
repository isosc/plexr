

# Create a simple dataframe and write it to adios

from mpi4py import MPI
import numpy as np
import pandas as pd
import plxr as px

def main():

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    df = px.adios_to_dataframe("test.bp", comm)
    print (df)



if __name__=='__main__':
    main()


