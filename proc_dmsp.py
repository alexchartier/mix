import numpy as np
import h5py
import datetime as dt

def main(
    fn = 'data/dmsp/dms_ut_20140523_16.002.hdf5',
):
    #flist = get_file_list(data_dir)
    #for fn in flist:
    raw_dmsp_data = load_data(fn)
    processed_dmsp_data = proc_data(raw_dmsp_data)

def load(fn):
    return proc_data(load_data(fn))


def load_data(fn):
    with h5py.File(fn, "r") as f:
        # Get the metadata
        parameters = f.get('Metadata')['Data Parameters'][...]
        # Get the data
        dataTable = f.get('Data').get('Table Layout')[...]

    vars = {}
    dmspData = {}
    for ind, prm in enumerate(parameters):
        str = prm[0].decode('utf-8')  # removing those annoying b' prefixes
        vars[str] = ind 
        dmspData[str] = []
    
    for entry in dataTable:
        for k, v in dmspData.items():
            v.append(entry[vars[k]])

    for k, v in dmspData.items():
        dmspData[k] = np.array(v)
    return dmspData


def proc_data(dmspData):

    # remove flagged bad data
    forQualIndex = dmspData["ION_V_FOR_FLAG"] == 1
    leftQualIndex = dmspData["ION_V_LEFT_FLAG"] == 1

    qualFlag = forQualIndex & leftQualIndex

    
    #goodInd = np.logical_and(dmspData['RPA_FLAG_UT'] < 2, dmspData['IDM_FLAG_UT'] < 2)  # NOTE: This is only for F15
    for k, v in dmspData.items():
        dmspData[k] = v[qualFlag]
    return dmspData
    

if __name__ == '__main__':
    main() 











