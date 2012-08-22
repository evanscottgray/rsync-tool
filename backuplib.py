#! /usr/bin/env python

import os

class logger(object):
	def __init__(self,f1,f2):
		self.log1 = f1
		self.log2 = f2
		return
	def write(self,data):
		with open(self.log2,'a')as f:
			if type(data) == type(['a','b']):
				for line in data:
					f.write(line.strip())
					f.write('\n')
			else:
				f.write(data)

	def log(self,data):
		with open(self.log1,'a') as f:
			f.write(data)
			f.write('\n')
		self.write(data)
		self.write('\n')
		return

class clobber():
	def __init__(self,files,lock,log):
		self.files = files
		self.lockfile = lock
		self.log = log
		self.pidfil = ''
		return

	def make(self):
		self.log.log('Making marker file...')
		if not self.files: return False
		for f in self.files:
			try:
				with open(f,'w') as p:
					p.write(str(os.getpid()))
			except IOError as e:
				self.log.log('IOError: could not write lock files. {0}\n{1}'.format(e.errno,e.strerror))
			else:
				self.log.log('PID marker file created at ' + f)
				self.pidfil = f
				return
		if self.pidfil == '':
			self.log.log('Could not create pid files!')

	def exists(self):
		if self.locked():
			return False
		for f in self.files:
			if os.path.exists(f):
				with open(f) as p:
					if os.path.exists('/proc/'+p.read().strip()):
						return True
		return False

	def lock(self):
		self.log.log('Creating lock file...')
		self.unlock()
		with open(self.lockfile) as f:
			f.write(str(os.getpid()))
		self.log.log('Lock file created.')
		return

	def unlock(self):
		os.remove(self.lockfile)
		self.log.log('Removing lock file...')
		return

	def locked(self):
		return os.path.exists(str(self.lockfile))

	def get(self):
		return os.getpid()

	def remove(self):
		self.log.log('Removing marker file...')
		try: os.remove(self.pidfil)
		except OSError: self.log.log('Could not remove marker file.')
		return

class ProcessError(Exception):
	def __init__(self, cmd, returncode, output):
		self.cmd,self.returncode,self.output = cmd,returncode,output
	def __str__(self, cmd, returncode, output):
		return repr('Process ' + cmd + ' failed with code ' + returncode + '.\n' + output)

