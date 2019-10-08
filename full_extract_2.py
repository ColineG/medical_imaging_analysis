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

    def dictify(self):
        """
        Fonction which load in a dataframe all metadata needed from DICOM file, using a dictionnaire.
        :return:
        """
        output = dict()
        for root, dirs, files in walk(self.param.startpath):
            for file in files:
                file_path_dcm = os.path.join(root, file)
                if file_path_dcm.endswith(".dcm"):
                    ds = pydicom.dcmread(file_path_dcm, force=True)
                    self.metadata = ds
                    for elem in ds:
                        if elem.VR != 'SQ':
                            output[elem.tag] = elem.value
                        else:
                            output[elem.tag] = [dictify(item) for item in elem]
                    return output

if __name__ == '__main__':

    mon_extractor = DCMAllMetaExtractor()
    mon_extractor.dictify()
