

# Create a simple dataframe and write it to adios

from mpi4py import MPI
import numpy as np
import pandas as pd
import plxr as px

def main():

    df = pd.DataFrame(np.random.randn(6,4),index=list('abcdef'),columns=list('ABCD'))
    #print (df)
    px.dataframe_to_adios ("test.bp", df)    

if __name__=='__main__':
    main()


