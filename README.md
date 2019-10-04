"# medical_imaging_analysis" 

1. Create a config file with all your path store and a class to use them as follow :

"""config = {
    'startpath': r'YOUR FILE PATH',

    'excel_file': {
        'path': r'YOUR EXCEL FILE PATH',
        'sheetname': 'NAME OF SHEET USED IN YOUR MAIN SCRIPT',
    },

    'savepath': r'WRITE HERE THE PATH WHERE YOU WANT TO SAVE THE RESULT OF YOUR FONCTION'

}


class Config:
    def __init__(self, param):
        self.startpath = param['startpath']
        self.excel_file_path = param['excel_file']['path']
        self.excel_file_sheetname = param['excel_file']['sheetname']
        self.savepath = param['savepath']

    def __repr__(self):
        return 'It works! <__maing__.Config at 0xblabla |||| %s' % self.startpath
"""