import glob
import pydicom
from collections import defaultdict
import configparser

class FileHandler:

	def __init__(self):
		config = configparser.ConfigParser()
		config.read('config.ini')
		self.fp = config['dicom']['data']
		self.filemap = defaultdict(list)

	#   Recrsively discover all dicom files (*.dcm) in the handlers directory
	def discover(self):
		for filename in glob.iglob(self.fp + '**/*.dcm', recursive=True):
			ds = pydicom.dcmread(filename)
			self.filemap[ds['SeriesDescription'].value].append(filename)

	#   Get a list of all series descriptions available
	def descriptions(self):
		return list(self.filemap.keys())

	def files(self, descr):
		if descr in self.filemap:
			return self.filemap[descr]
		return []
