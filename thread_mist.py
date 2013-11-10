#!/usr/bin/python
#-*- coding: utf-8 -*-

import sys
import os
from threading import Thread   
import subprocess
from class_mist import mistit
import gzip

class th_seq2mist(Thread):
	"""This thread converts a new sectional XML report in a MIST report"""

	def __init__(self, input_file, elements2mist, types2mist, analysis_id):
		Thread.__init__(self)
		self.input_file = input_file
		(froot, fext) = os.path.splitext(self.input_file)
		self.elements2mist = elements2mist
		self.types2mist = types2mist
		self.analysis_id = analysis_id
		self.output_file = froot + ".mist"

	def log(self, msg):
#		msg = msg.strip()
		fullmsg = "%s: %s\n" % (self.input_file, msg)
		hfile = open("log/report2mist.log", "a")
		hfile.write(fullmsg)
		hfile.close()

	def run(self):
		mist = mistit(self.input_file, self.elements2mist, self.types2mist)
		if mist.parse() and mist.convert():
			mist.write(self.output_file)
#			if len(mist.errormsg) > 0:
			self.log(mist.errormsg)
		else:
			self.log(mist.errormsg)
