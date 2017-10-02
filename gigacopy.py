#  Gigacopy
# Allows tracking of copy progress

import os


class Gigacopy:
	def __init__(self, src, dst, chunk_size=10000, reporting=True):
		self.source = src
		self.dest = dst
		self.chunk_size = chunk_size
		self.directorySize = self.directory_size(self.source)
		self.progress = 0
		self.reporting = reporting


	def report_progress(self):
		if self.reporting:
			prog = (self.progress / self.directorySize) * 100
			print(str(int(prog)), end="\r")


	def directory_size(self, target):
		total = 0
		if self.is_available(target):
			if os.path.isdir(target):
				for fps in os.listdir(target):
					#Recursively call directory_size on subcontents
					total += self.directory_size(target+"\\"+fps)
				return total
			else:
				#break recursion on files, cannot be a directory
				return os.stat(target).st_size
		return total


	def eradicate_directory(self, target):
		total = 0
		if self.is_available(target):
			if self.is_dir(target):
				for fps in os.listdir(target):
					total += self.eradicate_directory(target+ "\\"+ fps)
				os.rmdir(target)
				return total
			else:
				returnable = os.stat(target).st_size
				os.remove(target)
				return returnable
		return total


	def is_available(self, target):
		if not os.path.exists(target):
			return False
		return True


	def is_dir(self, target):
		if not os.path.isdir(target):
			return False
		return True


	def duplicate_file(self, src, dst):
		file_size = os.stat(src).st_size
		amnt_copy = 0
		inFP = open(src, 'rb')
		outFP = open(dst, 'wb')

		while amnt_copy < file_size:
			chunk = inFP.read(self.chunk_size)
			outFP.write(chunk)
			amnt_copy += len(chunk)
		self.progress += amnt_copy
		self.report_progress()

		inFP.close()
		outFP.close()
		return amnt_copy


	def duplicate_directory(self, src, dst):
		#total = 0
		if self.is_available(src):
			if self.is_dir(src):
				for fps in os.listdir(src):
					try:
						os.makedirs(dst)
					except FileExistsError as e:
						pass	#dir already exists, assume merge is expected behavior	
					self.duplicate_directory(src+"\\"+fps, dst+"\\"+fps)
				
			else:
				self.duplicate_file(src, dst)
