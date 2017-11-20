#  Gigacopy
# Allows tracking of copy progress
import os

class Gigacopy:
	"""Object responsible for tracking and reporting file copy progress"""
	def __init__(self, src, dst, chunk_size=10000, reporting=True, include_dirs=True):
		""" Initiaize object with persitency values

		Keywords:
		src -- string representing source directory
		dst -- string representing target directory
		chunk_size -- amount of data to be copied in a single write
		reporting -- If copy progress is being reported to the user
		include_dirs -- If copy is recurisve
		"""  
		
		self.source = src
		self.dest = dst
		self.chunk_size = chunk_size
		self.progress = 0
		self.reporting = reporting
		self.dirs = include_dirs
		self.directorySize = self.directory_size(self.source)


	def report_progress(self):
		"""If reporting is active, outputs an active progress report"""
		if self.reporting:
			prog = (self.progress / self.directorySize) * 100
			print(str(int(prog)), end="\r")


	def reset_progress(self):
		"""Return progress to 0"""
		self.progress = 0


	def directory_size(self, target):
		"""Returns the size of all files in subdirectories

		Kewords:
		target -- string representing the target directory to measure
		"""
		total = 0
		if self.is_available(target):
			if os.path.isdir(target) and self.dirs:
				for fps in os.listdir(target):
					#Recursively call directory_size on subcontents
					total += self.directory_size(target+"\\"+fps)
				return total
			else:
				#break recursion on files, cannot be a directory
				return os.stat(target).st_size
		return total


	def is_available(self, target):
		"""Returns binary availability of target"""
		if not os.path.exists(target):
			return False
		return True


	def is_dir(self, target):
		"""Returns binary representing if target is directory"""
		if not os.path.isdir(target):
			return False
		return True


	def duplicate_file(self, src, dst):
		"""Copy specific file to specific directory
		Note:
		Effect on existing files is undocumented

		Keywords:
		src -- String representing file to be copied
		dst -- String representing duplicate file
		"""
		file_size = os.stat(src).st_size
		amnt_copy = 0
		#print(src)
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


	def duplicate_directory(self, src=None, dst=None, dirs=True):
		"""Duplicate all files in directory

		Keywords:
		src -- String representing directory whose contents are to be copied
		dst -- String representing duplicate directory
		dirs -- Boolean if subdirectories will also be targeted
		"""
		if src == None:
			src = self.source
		if dst == None:
			dst = self.dest
		if self.is_available(src):
			if self.is_dir(src):
				if dirs:
					for fps in os.listdir(src):
						try:
							os.makedirs(dst)
						except FileExistsError as e:
							pass	#dir already exists, assume merge is expected behavior	
						self.duplicate_directory(src+"\\"+fps, dst+"\\"+fps, self.dirs)
			else:
				self.duplicate_file(src, dst)
