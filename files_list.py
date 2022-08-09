import os

class SourceFilesList:
    def __init__(self, path):
        self.path = path
        self.xlsx_files = []
    
    def files_selector(self):
        self.path = 'source-files'
        files = os.listdir(self.path)
        self.xlsx_files = [f for f in files if f[-4:] == 'xlsx']
        return self.xlsx_files
