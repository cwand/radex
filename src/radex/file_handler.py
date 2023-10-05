import glob
from typing import DefaultDict
import os

import pydicom
from collections import defaultdict
import configparser


class FileHandler:

	def __init__(self, data_fp: str | None = None):
		config = configparser.ConfigParser()
		config.read('config.ini')
		if data_fp is None:
			self.fp = config['dicom']['data']
		else:
			self.fp = data_fp
		self.filemap: DefaultDict[str, list[str]] = defaultdict(list)

	# Recursively discover all dicom files (*.dcm) in the handlers directory
	def discover(self):
		print(self.fp)
		for filename in glob.iglob(os.path.join(self.fp, '**', '*.dcm'), recursive=True):
			ds = pydicom.dcmread(filename)
			self.filemap[ds['SeriesDescription'].value].append(filename)

	# Get a list of all series descriptions available
	def descriptions(self) -> list[str]:
		return list(self.filemap.keys())

	def files(self, descr: str) -> list[str]:
		if descr in self.filemap:
			return self.filemap[descr]  # type: ignore
		return []
