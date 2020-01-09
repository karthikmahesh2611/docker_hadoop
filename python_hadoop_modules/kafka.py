from python_app_configs import config
from python_generic_modules import se_os
from python_generic_modules import se_docker
import re
import os
import glob
import time
import jinja2

template1 = jinja2.Template("{% for i in range(0,last_num)%}zookeepernode{{ i }}.{{ domain }}:2181{% if not loop.last %},{% endif %}{% endfor %}")
zookeeper_nodes = template1.render(last_num=config.zookeeper_nodes,domain=config.domain_name)

def setup_kafka_dirs():
	print('Setting up kafka bind_mount directories...\n')
	os.chdir(config.dest_dir)
	dir_glob = 'kafka' + '*'
	dir_lst = glob.glob(dir_glob)
	for i in dir_lst:
		se_os.del_dir(str(i))
	src_dir_path = os.path.join(config.data_dir,'kafka_conf')

	for i in range(0,config.kafka_nodes):
		dest_path_new = os.path.join(config.dest_dir,'kafkanode'+str(i))
		se_os.copy_dir(src_dir_path,dest_path_new)
	print('bind_mount directories setup compelete\n')


def config_kafka(i):
	src_file_path = os.path.join(config.data_dir,'kafka_conf','server.properties')
	dest_file_path = os.path.join(config.dest_dir,'kafkanode'+str(i),'server.properties')
	param1 = re.compile(r'(.*)(broker.id)(.*)')
	param2 = re.compile(r'(.*)(num.partitions)(.*)')
	param3 = re.compile(r'(.*)(zookeeper.connect=)(.*)')


	with open(src_file_path,mode='r') as file1:
		with open(dest_file_path,mode='w') as file2:
			for line in file1:
				if param1.search(line):
					line = param1.sub(r'\1\2{}'.format('='+str(i)), line)
					file2.write(line)
					continue
				elif param2.search(line):
					line = param2.sub(r'\1\2{}'.format('='+str(str(config.kafka_default_partitions))), line)
					file2.write(line)
					continue
				elif param3.search(line):
					line = param3.sub(r'\1\2{}'.format(zookeeper_nodes), line)
					file2.write(line)
					continue
				else:
					file2.write(line)				



def launch_kafka():

	print('\n====Running kafka_setup module====\n')
	setup_kafka_dirs()
	time.sleep(3)

	print('\n====Running kafka_config module====\n')
	for i in range(0,config.kafka_nodes):
		print("Updating configs for node 'kafkanode{}'\n".format(i))
		config_kafka(i)
	time.sleep(3)
	
	print('\n====Creating SE_Platform Network if not already created====\n')
	hadoop_net = config.hadoop_network_range + '/24'
	lst = config.hadoop_network_range.split('.')
	lst[3]='1'
	hadoop_gateway = '.'.join(lst)
	se_docker.create_network('hadoopnet',hadoop_net,hadoop_gateway)


	print('\n====Launching containers and attaching bind mounts====\n')
	for i in range(0,config.kafka_nodes):
		se_docker.launch_containers('kmahesh2611/kafka','/kafka_2.11-2.1.0/bin/kafka-server-start.sh /kafka_2.11-2.1.0/config/server.properties','kafkanode' + str(i) + '.' + config.domain_name,'kafkanode' +str(i) + '.' + config.domain_name,{os.path.join(config.dest_dir,'kafkanode'+str(i)):{'bind':'/kafka_2.11-2.1.0/config','mode':'rw'}},'hadoopnet',True,True)

	print('Wait for 10 seconds....')
	time.sleep(10)

	print('\n====Verify if containers are running====\n')
	num = 0
	for i in se_docker.get_all_containers():
		if 'kafkanode' in i.name:
			num = num + 1
			if 'running' in i.status:
				print('{} : {}'.format(i.name,i.status))
			else:
				print('Error: Container "{}" is in status "{}"\n'.format(i.name,i.status))
				print('Exiting script\n')
				sys.exit(1)
	if num == 0:
		print('No container found starting with name "kafkanode"')
		print('Exiting script\n')
		sys.exit(1)
	### Creating Kafka topics ###
	print('\n====Creating Kafka Topics====\n')
	for i in config.kafka_topics:
		print(se_docker.exec_command('kafkanode0' + '.' + config.domain_name,"/kafka_2.11-2.1.0/bin/kafka-topics.sh --create --zookeeper {} --replication-factor {} --partitions  {} --topic {}".format(zookeeper_nodes,str(config.kafka_nodes),str(config.kafka_default_partitions),i)))

	print("Created topics: {}\n".format([topics for topics in config.kafka_topics]))


def del_kafka_containers():
	print('\n====Stopping and deleting Containers for kafka====\n')
	for i in se_docker.get_all_containers():
		if 'kafkanode' in i.name:
			print('Stopping and deleting Container: {}\n'.format(i.name))
			i.remove(force=True)






















	
	





