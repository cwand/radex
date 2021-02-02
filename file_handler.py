import glob
import pydicom
from collections import defaultdict

class FileHandler:

    def __init__(self, fp):
        self.fp = fp
        self.filemap = defaultdict(list)

    #   Recrsively discover all dicom files (*.dcm) in the handlers directory
    def discover(self):
        for filename in glob.iglob(self.fp + '**/*.dcm', recursive=True):
            ds = pydicom.dcmread(filename)
            self.filemap[ds['SeriesDescription'].value].append(filename)

    #   Get a list of all series descriptions available
    def get_descriptions(self):
        return list(self.filemap.keys())

    def get_files_for_description(self, descr):
        if descr in self.filemap:
            return self.filemap[descr]
        return []
