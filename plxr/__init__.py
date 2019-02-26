#Package initialization script for plxr package

from mpi4py import MPI
import pandas as pd
import adios2 as ad
import numpy as np




def _do_pandas_single(step):
    # Read row and column names
    row_names = step.readstring("__plxr_row_names").split('*')
    #print (row_names)
    col_names = step.readstring("__plxr_col_names").split('*')
    #print (col_names)

    # Read the frame data
    data = {}
    for col_name in col_names:
        data[col_name] = step.read(col_name)
    return pd.DataFrame(data=data, index=row_names)

# Return a pandas dataframe containing data from the specified adios1 file (or stream)
# vars must contain a list of 1d variables contained in the file; all variables must
# have the same number of elements
def adios_to_dataframe (fname, comm):
    print ("TODO: read to dataframe")
    with ad.open(fname, 'r', comm) as f:
      for step in f: # Currently assuming that we have only one step
        schema_type = step.readstring("__plxr_schema_type")
        #print ("Detected schema type %s" % schema_type)
        if schema_type == "pandas-single":
            return _do_pandas_single(step)
        else:
            print ("Missing or unknown schema type in %s!"%fname)

        break


    return None








# Write the given dataframe to the specified adios file
def dataframe_to_adios (fname, frame, comm=MPI.COMM_WORLD):
    #print ("TODO: write to adios")
    #print (frame)

    # Let's do it
    # Can we deal with both MPI and non-MPI builds of ADIOS?
    with ad.open(fname, "w", comm) as fw:
        print ('*'.join(frame.index))
        fw.write("__plxr_schema_type", "pandas-single")
        fw.write("__plxr_generated_by", "plxr-python")
        fw.write("__plxr_row_names", '*'.join(frame.index)) # string[] not currently supported by adios2
        fw.write("__plxr_col_names", '*'.join(frame.columns)) # string[] not currently supported by adios2
        for col in frame.columns:
            # Question: will column names always be unique?
            
            #print (col)
            values = frame[col].values

            shape = [len(values)]
            start = [0]
            count = [len(values)]
            fw.write(col, np.array(values), shape, start, count)
    return

