""" Load DICOM files, view some metadata and plot images."""

import pydicom
import os
from os import walk
import numpy as np
import pandas as pd
from tqdm import tqdm
import sys
from final.config import Config, config
from final.modules.utils.displayinfo import show_dcm_info


class DCMMetaExtractor():
    def __init__(self):
        self.param = Config(config)
        self.output_DF = None
        self.li_dict = None
        self.metadata = None

    def generate_dataframe(self):
        """
        Fonction which load in a dataframe all metadata needed from DICOM file, using a dictionnaire.
        :return:
        """
        self.li_dict = []
        for root, dirs, files in walk(self.param.startpath):
            for file in files:
                file_path_dcm = os.path.join(root, file)
                if file_path_dcm.endswith(".dcm"):
                    ds = pydicom.dcmread(file_path_dcm, force=True)
                    self.metadata = ds
                    #print(self.ds.PatientSex)
                    #print(file)
                    #print(self.ds)
                    #show_dcm_info(ds)
                    #plot_pixel_array(ds)

                    self.li_dict.append(
                        {
                            'PatientID': ds.PatientID if "PatientID" in ds else None,
                            'PatientBirthDate': ds.PatientBirthDate if "PatientBirthDate" in ds else None,
                            'PatientSex': ds.PatientSex,
                            'Modality': ds.Modality if "Modality" in ds else None,
                            'StudyDate': ds.StudyDate if "StudyDate" in ds else None,
                            'StudyDesc': ds.StudyDescription if "StudyDescription" in ds else None,
                            'pixel_size': ds.PixelSpacing[0] if "PixelSpacing" in ds else None,
                            'imageMin': np.min(ds.pixel_array) if "pixel_array" in ds else None,
                            'imageMax': np.max(ds.pixel_array) if "pixel_array" in ds else None,
                            'imageMean': np.mean(ds.pixel_array) if "pixel_array" in ds else None,
                            'SOURCE_FILE_PATH': file_path_dcm
                        }
                    )

        self.output_DF = pd.DataFrame(self.li_dict)

    def save_DF_as_csv(self):
        """
        Fonction which after generate a dataframe will save it as a csv.
        :return:
        """
        if self.output_DF is None:
            print('Please generate your DataFrame first with <generate_dataframe> method !')
        else:
            self.output_DF.to_csv()



if __name__ == '__main__':

    mon_extractor = DCMMetaExtractor()
    mon_extractor.generate_dataframe()
    mon_extractor.metadata
    print(mon_extractor.output_DF)
    print(mon_extractor.li_dict)
