#!/bin/python
#this script will be used to setup and do 
#Load generation testing 

import ConfigParser
import os
import yum
import sys
import subprocess
from sys import argv
from decimal import *
from subprocess import *

#config_file = load.conf
#print 'config file:', config_file

config = ConfigParser.ConfigParser()
config.readfp( open( '/home/admin/Load/load.conf'))

#setting variables from config file

nos= int(config.get('Section 1', 'nos'))
logging= str(config.get('Section 1', 'logging'))
log_file= str(config.get('Section 1', 'log_file'))
load_number = int(config.get('Section 1', 'load_number'))
wpbs = Decimal(config.get('Section 1', 'wpbs'))
#open(config.get('Section 1', 'test_script'), 'w').close()
test_script = open(config.get('Section 1', 'test_script'),"w")
logginginfo= '--verbose 2 --fileloggin --logfile' +log_file 

yb = yum.YumBase()
if yb.rpmdb.searchNevra(name='vlc'):
	print "VLC installed"
else:
	print "Please install VLC before continuing"
	exit()

test_script.write('#!/bin/bash\n')


for x in range (load_number,0,-1):
	for y in range (nos,0,-1):
		y = str(y)
		try:
			if logging in ['y','Y', 'yes', 'Yes', 'YES']:
				teststring = 'nohup vlc ' + logginginfo + '--intf dummy --quiet --no-sout-display-audio --no-sout-display-video ' + config.get( 'Section 1', 'url' + (y)) +' &'  
			else:
				teststring = 'nohup vlc --intf dummy --quiet --no-sout-display-audio --no-sout-display-video ' + config.get ('Section 1', 'url' + (y)) + ' &'
			test_script.write( teststring)		
		except ConfigParser.NoOptionerror:
			print "missing url"+ (y)
			break
	test_script.write('sleep ' + str(wpbs) + '\n')

test_script.close()	

print "Running Tests"
os.chmod(config.get('Section 1', 'test_script'), 0777)
subprocess.call(config.get('Section 1', 'test_script'),shell=True)
exit()


		
