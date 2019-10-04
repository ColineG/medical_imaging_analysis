import pydicom
import os
from os import walk
import numpy as np
import pandas as pd
from tqdm import tqdm
import sys
from final.config import Config, config
from final.modules.utils.displayinfo import show_dcm_info


class DCMAllMetaExtractor():
    def __init__(self):
        self.param = Config(config)
        self.full_DF = None
        self.dict_metadata = None
        self.metadata = None

    def dicom_dataset_to_dict(self):
        """
        Fonction which load all metada in a dataframe from DICOM file, using a dictionnaire.
        :return:
        """
        self.dict_metadata = []
        for root, dirs, files in walk(self.param.startpath):
            for file in files:
                file_path_dcm = os.path.join(root, file)
                if file_path_dcm.endswith(".dcm"):
                    ds = pydicom.dcmread(file_path_dcm, force=True)
                    #print(self.ds.PatientSex)
                    #print(file)
                    #print(self.ds)
                    #show_dcm_info(ds)
                    #plot_pixel_array(ds)
                    print(ds)
                    self.metadata = ds
                    for elem in ds:
                        print(elem)
                        if True:
                            self.dict_metadata.append(elem)
            return self.dict_metadata
        self.full_DF = pd.DataFrame(self.dict_metadata)

if __name__ == '__main__':

    extract = DCMAllMetaExtractor()
    extract.dicom_dataset_to_dict()
    print(extract.full_DF)

"""
    extract.dict_metadata.append({elem.value})
    return extract.dict_metadata
extract.full_DF = pd.DataFrame(extract.dict_metadata)"""