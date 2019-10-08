""" Load DICOM files, view some metadata needed."""

import pydicom
import os
from os import walk
import numpy as np
import pandas as pd
from tqdm import tqdm
import sys
from final.config import Config, config
import altair as alt
from final.modules.utils.displayinfo import show_dcm_info


class DCMMetaExtractor():
    def __init__(self):
        self.param = Config(config)
        self.output_DF = None
        self.li_dict = None
        self.metadata = None
        self.df1 = None
        self.df2 = None
        self.df = None

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
                            'Age': np.subtract(int(self.metadata.StudyDate[0:4]),
                                               int(self.metadata.PatientBirthDate[0:4])) if "Age" in ds else None,
                            'SOURCE_FILE_PATH': file_path_dcm
                        }
                    )

        self.output_DF = pd.DataFrame(self.li_dict)

    def add_columns(self):
        """
        This fonction will allow to add some specific custom columns to a dataframe.
        :return:
        """
        self.output_DF['Age'] = self.output_DF.apply(lambda row: np.subtract(int(self.metadata.StudyDate[0:4])),
                                                                             int(self.metadata.PatientBirthDate[0:4])),
                                                    axis=1)

    def merge_patientID(self):
        """
        Fonction to merge our dataframe with our excel file in the aim to anonymize the database.
        :return:
        """
        self.df1 = self.output_DF
        self.df2 = pd.read_excel(self.param.excel_anonym)

        self.df = self.df1.merge(self.df2, on='PatientID', how='inner')

    def anonymize(self):
        """
        Fonction to anonymize the dataframe after the merge manipulation on the patientID.
        :return:
        """

    def save_DF_as_csv(self):
        """
        Fonction which after generate a dataframe will save it as a csv.
        :return:
        """
        if self.output_DF is None:
            print('Please generate your DataFrame first with <generate_dataframe> method !')
        else:
            self.output_DF.to_csv(self.param.savepath)


if __name__ == '__main__':

    mon_extractor = DCMMetaExtractor()
    mon_extractor.generate_dataframe()
    #mon_extractor.metadata
    print(mon_extractor.output_DF)
    print(mon_extractor.li_dict)
    #filter sur la valeur d'une colonne a = df[df.PatientSex == 'F']




