#!/usr/bin/env python
# encoding: utf-8
"""
learn_cuckoo.py

Created by Philipp Trinius on 2013-11-10.
Copyright (c) 2013 pi-one.net . All rights reserved.
"""
import os
import json
import sys
import re
import glob


if __name__ == '__main__':

	learn_reports = {}

	learn_reports['device'] 			= {} 
	learn_reports['filesystem'] 		= {} 
	learn_reports['hooking'] 			= {} 
	learn_reports['network'] 			= {} 
	learn_reports['process'] 			= {} 
	learn_reports['registry'] 			= {} 
	learn_reports['services'] 			= {} 
	learn_reports['synchronization'] 	= {} 
	learn_reports['system'] 			= {} 
	learn_reports['threading'] 			= {} 
	learn_reports['windows'] 			= {}

	i = 0
	for top, dirs, files in os.walk('/opt/cuckoo/storage/analyses/'):
    		for nm in files:
			if nm == "report.json":
				report = os.path.join(top, nm)      
				i += 1
				print "learn report number %i (%s)" % (i, report),

				fp = open(report, 'r')
				jo = json.load(fp)
				fp.close()

				sortCalls = {}
				procs = jo['behavior']['processes']
				counter = 0
				for proc in procs:
					calls = proc['calls']
					for call in calls:
						sortCalls[call['timestamp']] = (call['category'], call['api'], call['arguments'])
						for item in sorted(sortCalls.iterkeys()):
							try:
								l = len(learn_reports[sortCalls[item][0]][sortCalls[item][1]])
							except:
								learn_reports[sortCalls[item][0]][sortCalls[item][1]] = {}
							for arg in sortCalls[item][2]:
								print ".", #arg
								try:	
									learn_reports[sortCalls[item][0]][sortCalls[item][1]][arg['name']][arg['value']] += 1
								except:
									try:
										learn_reports[sortCalls[item][0]][sortCalls[item][1]][arg['name']][arg['value']] = 1				
									except:
										learn_reports[sortCalls[item][0]][sortCalls[item][1]][arg['name']] = {}
										learn_reports[sortCalls[item][0]][sortCalls[item][1]][arg['name']][arg['value']] = 1				
				k = i % 10
				json.dump(learn_reports, open(str(k) + "_learned_from_reports.json", 'wb'))
				print " done."


