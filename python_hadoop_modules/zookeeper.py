from python_app_configs import config
from python_generic_modules import se_os
from python_generic_modules import se_docker
import re
import os
import glob
import time
import jinja2

def setup_zookeeper_dirs():
	print('Setting up zookeeper conf bind_mount directories...\n')
	os.chdir(config.dest_dir)
	dir_glob = 'zookeeper' + '*'
	dir_lst = glob.glob(dir_glob)
	for i in dir_lst:
		se_os.del_dir(str(i))

	src_dir_path = os.path.join(config.data_dir,'zookeeper_conf')
	dest_path_new = os.path.join(config.dest_dir,'zookeepernode')
	se_os.copy_dir(src_dir_path,dest_path_new)
	print('bind_mount directories setup compelete\n')


def config_zookeeper():
	dest_file_path = os.path.join(config.dest_dir,'zookeepernode','zoo.cfg')
	print('Updating Zookeeper configs inside the bind_dir\n')
	with open(dest_file_path,mode='w') as file2:
		file2.write('dataDir=/var/lib/zookeeper\n')
		file2.write('clientPort=2181\n')
		file2.write('initLimit=5\n')
		file2.write('syncLimit=2\n')
		file2.write('tickTime=2000\n')
		for i in range(0,config.zookeeper_nodes):
			file2.write('server.{}=zookeepernode{}.{}:2888:3888\n'.format(str(i+1),str(i),config.domain_name))


def launch_zookeeper():
	print('\n====Running zookeeper setup module====\n')
	setup_zookeeper_dirs()
	config_zookeeper()

	print('\n====Creating SE_Platform Network if not already created====\n')
	hadoop_net = config.hadoop_network_range + '/24'
	lst = config.hadoop_network_range.split('.')
	lst[3]='1'
	hadoop_gateway = '.'.join(lst)
	se_docker.create_network('hadoopnet',hadoop_net,hadoop_gateway)

	print('\n====Launching zookeeper containers and attaching bind mounts====\n')
	for i in range(0,config.zookeeper_nodes):
		port_num = 2181 + i
		print('Launching zookeeper node {}\n'.format(str(i)))
		se_docker.launch_containers('kmahesh2611/zookeeper','bash','zookeepernode' + str(i) + '.' + config.domain_name,'zookeepernode' + str(i) + '.' + config.domain_name,{os.path.join(config.dest_dir,'zookeepernode'):{'bind':'/etc/zookeeper/conf','mode':'ro'}},'hadoopnet',True,True,port_map={'2181/tcp': port_num})
		print('Creating myid file for the zookeeper node {}\n'.format(str(i)))
		print(se_docker.exec_command('zookeepernode' + str(i) + '.' + config.domain_name,"su -l zookeeper -c 'echo {} > /var/lib/zookeeper/myid'".format(str(i+1))))
		print('Starting Zookeeper service on the node the zookeeper node {}\n'.format(str(i)))
		print(se_docker.exec_command('zookeepernode' + str(i) + '.' + config.domain_name,"su -l zookeeper -c '/usr/hdp/current/zookeeper-client/bin/zkServer.sh start'"))
	print('Wait for 5 seconds....')
	time.sleep(5)

	print('\n====Verify if containers are running====\n')
	num = 0
	for i in se_docker.get_all_containers():
		if 'zookeepernode' in i.name:
			num = num + 1
			if 'running' in i.status:
				print('{} : {}'.format(i.name,i.status))
			else:
				print('Error: Container "{}" is in status "{}"\n'.format(i.name,i.status))
				print('Exiting script\n')
				sys.exit(1)
	if num == 0:
		print('No container found starting with name "zookeepernode"')
		print('Exiting script\n')
		sys.exit(1)


def del_zookeeper_containers():
	print('\n====Stopping and deleting Containers for zookeeper====\n')
	for i in se_docker.get_all_containers():
		if 'zookeepernode' in i.name:
			print('Stopping and deleting Container: {}\n'.format(i.name))
			i.remove(force=True)