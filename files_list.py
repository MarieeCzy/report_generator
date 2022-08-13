import os

class SourceFilesList:
    def __init__(self, path):
        self.path = path
        self.xlsx_files = []
    
    def files_selector(self):
        files = os.listdir(os.path.expanduser(self.path))
        self.xlsx_files = [f for f in files if f[-4:] == 'xlsx']
        return self.xlsx_files

#for macos
#os.listdir(os.path.expanduser('~/Desktop'))
#for windows
#files = os.listdir(self.path)
