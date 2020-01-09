import os
import subprocess
import time
import shutil
import datetime
from python_app_configs import config
import tarfile


class linux_cmd_line():

	def __init__(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs
		if 'delay' in self.kwargs.keys():
			self.delay = int(self.kwargs['delay'])
		else:
			self.delay = 0

	def run(self):
		for index,cmd in enumerate(self.args):
			print("Running command '{}'".format(cmd))
			print("Wait...")
			p = subprocess.Popen(str(cmd), shell=True, stdout = subprocess.PIPE)
			for line in p.stdout.readlines():
				yield line.decode("utf-8")
				
			print("Command execution compelete '{}'".format(cmd))
			if index != len(self.args)-1:
				print("Waiting for delay timer to complete for next command with delay = {}".format(self.delay))
				time.sleep(self.delay)
			print('\n=======================================\n')



def linux_execute(*args, **kwargs):
	if 'delay' in kwargs.keys():
		delay = int(kwargs['delay'])
	else:
		delay = 0
	for index,cmd in enumerate(args):
		print("Running command '{}'".format(cmd))
		print("Wait...")
		p = subprocess.Popen(str(cmd), shell=True, stdout = subprocess.PIPE)
		for line in p.stdout.readlines():
			#print(line.strip())
			yield line.decode("utf-8")
			
		print("Command execution compelete '{}'".format(cmd))
		if index != len(args)-1:
			print("Waiting for delay timer to complete for next command with delay = {}".format(delay))
			time.sleep(delay)
		print('\n=======================================\n')


def del_dir(dir_name):
	for i in linux_execute('sudo rm -rf ' + str(dir_name)):
		print(i)
	#shutil.rmtree(str(dir_name))
	'''
	try:
		shutil.rmtree(str(dir_name))
	except:
		print('Unable to delete the directory {}. The directory path might not exist'.format(str(dir_name)))
	else:
		print('Directory deleted {}'.format(str(dir_name)))
	'''

def copy_dir(src_dir,dest_dir):
	cmd = 'cp -r ' + str(src_dir) + ' ' + str(dest_dir)
	print(cmd)
	for i in linux_execute(cmd):
		print(i)

def archive_logs():
	copy_dir(config.dest_logs_dir, config.backup_logs_dir)
	dateformat = str(datetime.datetime.now())
	newname = config.backup_logs_dir+'_'+dateformat
	#os.mkdir(config.backup_logs_dir)
	os.rename(config.backup_logs_dir,newname)
	print(newname)
	with tarfile.open(os.path.join(str(newname)+'.tar.gz'), "w") as archive:
			archive.add(newname)
		