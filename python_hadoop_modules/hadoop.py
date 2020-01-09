from python_app_configs import config
from python_generic_modules import se_os
from python_generic_modules import se_docker
import re
import os
import glob
import time
import jinja2
import csv
from jinja2 import Environment
from jinja2 import FileSystemLoader


def setup_hdfs_dirs():
	print('Setting up hdfs conf bind_mount directories...\n')
	os.chdir(config.dest_dir)
	dir_glob = 'hadoop' + '*'
	dir_lst = glob.glob(dir_glob)
	for i in dir_lst:
		se_os.del_dir(str(i))

	src_dir_path = os.path.join(config.data_dir,'hadoop_conf')
	dest_path_new = os.path.join(config.dest_dir,'hadoopnode')
	se_os.copy_dir(src_dir_path,dest_path_new)
	print('bind_mount directories setup compelete\n')


def config_core_site():
	param1 = re.compile(r'(.*)(<value>hdfs://)(\$namenode\.full\.hostname)(:8020</value>)(.*)')

	dest_file = os.path.join(config.dest_dir,'hadoopnode','core-site.xml')
	src_file = os.path.join(config.data_dir,'hadoop_conf','core-site.xml')
	with open(src_file,mode='r') as file1:
		with open(dest_file,mode='w') as file2:
			for line in file1:
				if param1.search(line):
					line = param1.sub(r'\1\2{}\4\5'.format('masternode.'+config.domain_name), line)
					file2.write(line)
					continue
				else:
					file2.write(line)
	print('Configuration compelete for core-site.xml\n')


def config_hdfs_site():
	param1 = re.compile(r'(.*)(<value>)(TODO-NAMENODE-HOSTNAME)(:50070</value>)(.*)')
	param2 = re.compile(r'(.*)(<value>)(TODO-NAMENODE-HOSTNAME)(:8020</value>)(.*)')
	param3 = re.compile(r'(.*)(<value>)(TODO-NAMENODE-HOSTNAME)(:50470</value>)(.*)')
	dest_file = os.path.join(config.dest_dir,'hadoopnode','hdfs-site.xml')
	src_file = os.path.join(config.data_dir,'hadoop_conf','hdfs-site.xml')
	with open(src_file,mode='r') as file1:
		with open(dest_file,mode='w') as file2:
			for line in file1:
				if param1.search(line):
					line = param1.sub(r'\1\2{}\4\5'.format('masternode.'+config.domain_name), line)
					file2.write(line)
					continue
				elif param2.search(line):
					line = param2.sub(r'\1\2{}\4\5'.format('masternode.'+config.domain_name), line)
					file2.write(line)
					continue
				elif param3.search(line):
					line = param3.sub(r'\1\2{}\4\5'.format('masternode.'+config.domain_name), line)
					file2.write(line)
					continue
				else:
					file2.write(line)
	print('Configuration compelete for hdfs-site.xml\n')


def config_yarn_site():
	param1 = re.compile(r'{{resourcemanager_full_hostname}}')
	param2 = re.compile(r'{{yarn_nodemanager_resource_cpu_vcores}}')
	param3 = re.compile(r'{{yarn_scheduler_minimum_allocation_vcores}}')
	param4 = re.compile(r'{{yarn_scheduler_maximum_allocation_vcores}}')
	param5 = re.compile(r'{{yarn_scheduler_maximum_allocation_mb}}')
	param6 = re.compile(r'{{yarn_scheduler_minimum_allocation_mb}}')
	param7 = re.compile(r'{{yarn_nodemanager_resource_memory_mb}}')
	param8 = re.compile(r'{{yarn_nodemanager_resource_memory_mb}}')
	param9 = re.compile(r'{{yarn_nodemanager_vmem_pmem_ratio}}')
	dest_file = os.path.join(config.dest_dir,'hadoopnode','yarn-site.xml')
	src_file = os.path.join(config.data_dir,'hadoop_conf','yarn-site.xml')
	with open(src_file,mode='r') as file1:
		with open(dest_file,mode='w') as file2:
			for line in file1:
				if param1.search(line):
					line = param1.sub('masternode.'+config.domain_name, line)
					file2.write(line)
					continue
				elif param2.search(line):
					line = param2.sub(str(config.yarn_nodemanager_resource_cpu_vcores), line)
					file2.write(line)
					continue
				elif param3.search(line):
					line = param3.sub(str(config.yarn_scheduler_minimum_allocation_vcores), line)
					file2.write(line)
					continue
				elif param4.search(line):
					line = param4.sub(str(config.yarn_scheduler_maximum_allocation_vcores), line)
					file2.write(line)
					continue
				elif param5.search(line):
					line = param5.sub(str(config.yarn_scheduler_maximum_allocation_mb), line)
					file2.write(line)
					continue
				elif param6.search(line):
					line = param6.sub(str(config.yarn_scheduler_minimum_allocation_mb), line)
					file2.write(line)
					continue
				elif param7.search(line):
					line = param7.sub(str(config.yarn_nodemanager_resource_memory_mb), line)
					file2.write(line)
					continue
				elif param8.search(line):
					line = param8.sub(str(config.yarn_nodemanager_resource_memory_mb), line)
					file2.write(line)
					continue
				elif param9.search(line):
					line = param9.sub(str(config.yarn_nodemanager_vmem_pmem_ratio), line)
					file2.write(line)
					continue
				else:
					file2.write(line)
	print('Configuration compelete for yarn-site.xml\n')


def config_mapred_site():
	param1 = re.compile(r'{{mapreduce_map_memory_mb}}')
	param2 = re.compile(r'{{mapreduce_map_java_opts}}')
	param3 = re.compile(r'{{mapreduce_reduce_memory_mb}}')
	param4 = re.compile(r'{{mapreduce_reduce_java_opts}}')
	param5 = re.compile(r'{{yarn_app_mapreduce_am_resource_mb}}')
	param6 = re.compile(r'{{yarn_app_mapreduce_am_command_opts}}')
	param7 = re.compile(r'{{mapreduce_task_io_sort_mb}}')
	dest_file = os.path.join(config.dest_dir,'hadoopnode','mapred-site.xml')
	src_file = os.path.join(config.data_dir,'hadoop_conf','mapred-site.xml')
	with open(src_file,mode='r') as file1:
		with open(dest_file,mode='w') as file2:
			for line in file1:
				if param1.search(line):
					line = param1.sub(str(config.mapreduce_map_memory_mb), line)
					file2.write(line)
					continue
				elif param2.search(line):
					line = param2.sub(str(config.mapreduce_map_java_opts), line)
					file2.write(line)
					continue
				elif param3.search(line):
					line = param3.sub(str(config.mapreduce_reduce_memory_mb), line)
					file2.write(line)
					continue
				elif param4.search(line):
					line = param4.sub(str(config.mapreduce_reduce_java_opts), line)
					file2.write(line)
					continue
				elif param5.search(line):
					line = param5.sub(str(config.yarn_app_mapreduce_am_resource_mb), line)
					file2.write(line)
					continue
				elif param6.search(line):
					line = param6.sub(str(config.yarn_app_mapreduce_am_command_opts), line)
					file2.write(line)
					continue
				elif param7.search(line):
					line = param7.sub(str(config.mapreduce_task_io_sort_mb), line)
					file2.write(line)
					continue
				else:
					file2.write(line)
	print('Configuration compelete for mapred-site.xml\n')	

template1 = jinja2.Template("{% for i in range(0,last_num)%}zookeepernode{{ i }}.{{ domain }}{% if not loop.last %},{% endif %}{% endfor %}")
zookeeper_nodes = template1.render(last_num=config.zookeeper_nodes,domain=config.domain_name)


def setup_hbase_dirs():
	print('Setting up hdfs conf bind_mount directories...\n')
	os.chdir(config.dest_dir)
	dir_glob = 'hbase' + '*'
	dir_lst = glob.glob(dir_glob)
	for i in dir_lst:
		se_os.del_dir(str(i))

	src_dir_path = os.path.join(config.data_dir,'hbase_conf')
	dest_path_new = os.path.join(config.dest_dir,'hbasenode')
	se_os.copy_dir(src_dir_path,dest_path_new)
	print('bind_mount directories setup compelete\n')


def config_hbase_site():
	param1 = re.compile(r'(.*)(<value>hdfs://)(namenode)(:8020/apps/hbase/data</value>)(.*)')
	param2 = re.compile(r'(.*)(<value>)(zookeeper)(</value>)(.*)')

	dest_file = os.path.join(config.dest_dir,'hbasenode','hbase-site.xml')
	src_file = os.path.join(config.data_dir,'hbase_conf','hbase-site.xml')
	with open(src_file,mode='r') as file1:
		with open(dest_file,mode='w') as file2:
			for line in file1:
				if param1.search(line):
					line = param1.sub(r'\1\2{}\4\5'.format('masternode.'+config.domain_name), line)
					file2.write(line)
					continue
				elif param2.search(line):
					line = param2.sub(r'\1\2{}\4\5'.format(zookeeper_nodes), line)
					file2.write(line)
					continue
				else:
					file2.write(line)
	print('Configuration compelete for hbase-site.xml\n')


def config_regionservers():
	dest_file_path=os.path.join(config.dest_dir,'hbasenode','regionservers')
	with open(dest_file_path,mode='w') as file2:
			file2.write('masternode.{}\n'.format(config.domain_name))


def setup_spark2_dirs():
	print('Setting up hdfs conf bind_mount directories...\n')
	os.chdir(config.dest_dir)
	dir_glob = 'spark' + '*'
	dir_lst = glob.glob(dir_glob)
	for i in dir_lst:
		se_os.del_dir(str(i))

	src_dir_path = os.path.join(config.data_dir,'spark_conf')
	dest_path_new = os.path.join(config.dest_dir,'sparknode')
	os.mkdir(os.path.join(config.dest_dir,'sparkclient'))
	os.mkdir(os.path.join(config.dest_dir,'sparkwatcher'))
	se_os.copy_dir(src_dir_path,dest_path_new)
	print('bind_mount directories setup compelete\n')


def setup_hadoop_dirs():

	print('\n====Setting up hadoop dirs and configs====\n')
	setup_hdfs_dirs()
	config_core_site()
	config_hdfs_site()
	config_yarn_site()
	config_mapred_site()
	setup_hbase_dirs()
	config_hbase_site()
	config_regionservers()
	setup_spark2_dirs()

	time.sleep(1)
	print('\n====Creating SE_Platform Network if not already created====\n')
	hadoop_net = config.hadoop_network_range + '/24'
	lst = config.hadoop_network_range.split('.')
	lst[3]='1'
	hadoop_gateway = '.'.join(lst)
	se_docker.create_network('hadoopnet',hadoop_net,hadoop_gateway)


def launch_containers():
	print('\n====Launching masternode container and attaching bind mounts====\n')
	se_docker.launch_containers('kmahesh2611/hdp2.6.5','bash','masternode' + '.' + config.domain_name,'masternode' + '.' + config.domain_name,{os.path.join(config.dest_dir,'hadoopnode'):{'bind':'/etc/hadoop/conf','mode':'rw'},os.path.join(config.dest_dir,'hbasenode'):{'bind':'/etc/hbase/conf','mode':'rw'},os.path.join(config.dest_dir,'sparknode'):{'bind':'/etc/spark2/conf','mode':'rw'}},'hadoopnet',True,True,port_map={'50070/tcp': 50070,'8088/tcp': 8088, '8765/tcp': 8765, '18080/tcp': 18080, '16010/tcp': 16010})
	print('Wait for 5 seconds....')
	time.sleep(5)

	# create_proxy_dirs()
	# proxy_config()
	# create_log_dirs()
	print('\n====Launching slavenode container and attaching bind mounts====\n')
	for i in range(0,config.slavenodes):
		#se_docker.launch_containers('se_hadoop',"bash",'slavenode' + str(i) + '.' + config.domain_name,'slavenode' + str(i) + '.' + config.domain_name,{os.path.join(config.proxy_dir,'slavenode'):{'bind':'/opt/se_proxy','mode':'ro'},os.path.join(config.dest_dir,'hadoopnode'):{'bind':'/etc/hadoop/conf','mode':'rw'},os.path.join(config.dest_dir,'hbasenode'):{'bind':'/etc/hbase/conf','mode':'rw'},os.path.join(config.dest_dir,'sparknode'):{'bind':'/etc/spark2/conf','mode':'rw'}},'seplatform',True,True)
		se_docker.launch_containers('kmahesh2611/hdp2.6.5',"bash",'slavenode' + str(i) + '.' + config.domain_name,'slavenode' + str(i) + '.' + config.domain_name,{os.path.join(config.dest_dir,'hadoopnode'):{'bind':'/etc/hadoop/conf','mode':'rw'},os.path.join(config.dest_dir,'hbasenode'):{'bind':'/etc/hbase/conf','mode':'rw'},os.path.join(config.dest_dir,'sparknode'):{'bind':'/etc/spark2/conf','mode':'rw'}},'hadoopnet',True,True)
		time.sleep(3)
		print(se_docker.exec_command('slavenode' + str(i) + '.' + config.domain_name,"chmod +x /etc/hadoop/conf/health_check"))


	print('\n====Launching client container and attaching bind mounts====\n')
	se_docker.launch_containers('kmahesh2611/hadoopclient','bash','clientnode' + '.' + config.domain_name,'clientnode' + '.' + config.domain_name,{os.path.join(config.dest_dir,'hadoopnode'):{'bind':'/etc/hadoop/conf','mode':'rw'},os.path.join(config.dest_dir,'hbasenode'):{'bind':'/etc/hbase/conf','mode':'rw'},os.path.join(config.dest_dir,'sparknode'):{'bind':'/etc/spark2/conf','mode':'rw'},os.path.join(config.dest_dir,'sparkclient'):{'bind':'/opt/spark','mode':'rw'},os.path.join(config.dest_dir,'sparkwatcher'):{'bind':'/nfs','mode':'rw'}},'hadoopnet',True,True)
	print(se_docker.exec_command('clientnode' + '.' + config.domain_name,"setfacl -m u:spark:rwX /nfs"))	
	print(se_docker.exec_command('clientnode' + '.' + config.domain_name,"setfacl -d -m u:spark:rwX /nfs"))	
	print(se_docker.exec_command('clientnode' + '.' + config.domain_name,"setfacl -m u:spark:rwX /opt/spark"))
	print(se_docker.exec_command('clientnode' + '.' + config.domain_name,"setfacl -d -m u:spark:rwX /opt/spark"))
	print('Wait for 5 seconds....')
	time.sleep(5)	

	print('\n====Verify if container running====\n')
	num = 0
	for i in se_docker.get_all_containers():
		if 'masternode' in i.name or 'slavenode' in i.name:
			num = num + 1
			if 'running' in i.status:
				print('{} : {}'.format(i.name,i.status))
			else:
				print('Error: Container "{}" is in status "{}"\n'.format(i.name,i.status))
				print('Exiting script\n')
				sys.exit(1)
	if num == 0:
		print('No container found starting with name "masternode" or "slavenode"')
		print('Exiting script\n')
		sys.exit(1)


def launch_hdfs():

	print('\n====Formatting Namenode====\n')
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs namenode -format -force'"))

	print('\n====Starting Namenode====\n')
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c '/usr/hdp/current/hadoop-client/sbin/hadoop-daemon.sh start namenode'"))
	print('Wait for 5 seconds....')
	time.sleep(5)
	
	print('\n====Starting datanodes====\n')
	for i in se_docker.get_all_containers():
		if 'slavenode' in i.name:
			print(se_docker.exec_command(i.name,"su -l hdfs -c '/usr/hdp/current/hadoop-client/sbin/hadoop-daemon.sh start datanode'"))
			print('Wait for 5 seconds....')
			time.sleep(5)


def launch_yarn():
	print('\n====Creating hdfs directories required for yarn and spark====\n')
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -mkdir -p /hdp/apps/2.6.5.0-292/mapreduce/'"))
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -put /usr/hdp/current/hadoop-client/mapreduce.tar.gz /hdp/apps/2.6.5.0-292/mapreduce/'"))
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -chown -R hdfs:hadoop /hdp && hdfs dfs -chmod -R 555 /hdp/apps/2.6.5.0-292/mapreduce && hdfs dfs -chmod 444 /hdp/apps/2.6.5.0-292/mapreduce/mapreduce.tar.gz'"))
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -mkdir -p /user/yarn && hdfs dfs -chown yarn:yarn /user/yarn && hdfs dfs -chmod -R 755 /user/yarn'"))
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -mkdir -p /mr-history/tmp && hdfs dfs -mkdir -p /mr-history/done'"))
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -chown mapred:mapred /mr-history && hdfs dfs -chown mapred:mapred /mr-history/tmp && hdfs dfs -chown mapred:mapred /mr-history/done'"))	
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -mkdir -p /app-logs && hdfs dfs -chmod 1777 /app-logs && hdfs dfs -chown yarn:hadoop /app-logs'"))
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -mkdir -p /user/spark && hdfs dfs -chown spark:spark /user/spark && hdfs dfs -chmod -R 755 /user/spark'"))
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -mkdir /spark2-history && hdfs dfs -chown -R spark:hadoop /spark2-history && hdfs dfs -chmod -R 777 /spark2-history'"))
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -mkdir -p /apps/hbase/data'"))
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -chown -R hbase:hbase /apps/hbase'"))	
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -mkdir -p /spark-clearing-input'"))
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -chown -R spark:spark /spark-clearing-input'"))	
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -mkdir -p /spark-clearing-output'"))
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hdfs -c 'hdfs dfs -chown -R spark:spark /spark-clearing-output'"))	
	print('\n====Starting Resource manager====\n')
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l yarn -c '/usr/hdp/current/hadoop-yarn-resourcemanager/sbin/yarn-daemon.sh --config $HADOOP_CONF_DIR start resourcemanager'"))
	print('Wait for 5 seconds....')
	time.sleep(5)
	print('\n====Starting Node manager====\n')
	for i in range(0,config.slavenodes):
		print(se_docker.exec_command('slavenode' + str(i) + '.' + config.domain_name,"su -l yarn -c '/usr/hdp/current/hadoop-yarn-nodemanager/sbin/yarn-daemon.sh --config $HADOOP_CONF_DIR start nodemanager'"))
		
	print('Wait for 5 seconds....')
	time.sleep(5)

	print('\n====Starting Spark History Server====\n')
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l spark -c '/usr/hdp/2.6.5.0-292/spark2/sbin/start-history-server.sh'"))
	print('Wait for 5 seconds....')


def launch_hbase():
	print('\n====Verify if Zookeeper containers are running====\n')
	num = 0
	for i in se_docker.get_all_containers():
		if 'zookeeper' in i.name:
			num = num + 1
			if 'running' in i.status:
				print('{} : {}'.format(i.name,i.status))
			else:
				print('Error: Container "{}" is in status "{}"\n'.format(i.name,i.status))
				print('Exiting script\n')
				sys.exit(1)
	if num == 0:
		print('No container found starting with name "zookeeper"')
		print('Exiting script\n')
		sys.exit(1)

	print('\n====Launch hbase master====\n')
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hbase -c '/usr/hdp/current/hbase-client/bin/hbase-daemon.sh start master'"))
	print('Wait for 10 seconds....')
	time.sleep(10)

	print('\n====Launch hbase region====\n')
	#se_docker.launch_containers('se_hbase','bash','hbaseregion' + '.' + config.domain_name,'hbaseregion' + '.' + config.domain_name,{os.path.join(config.dest_dir,'hbasenode'):{'bind':'/etc/hbase/conf','mode':'ro'}},'seplatform',True,True,port_map={'16020/tcp': 16020,'16030/tcp': 16030})
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hbase -c '/usr/hdp/current/hbase-client/bin/hbase-daemon.sh start regionserver'"))

	print('\n====Launch Phoenix query server====\n')
	#se_docker.launch_containers('se_hbase','bash','hbaseregion' + '.' + config.domain_name,'hbaseregion' + '.' + config.domain_name,{os.path.join(config.dest_dir,'hbasenode'):{'bind':'/etc/hbase/conf','mode':'ro'}},'seplatform',True,True,port_map={'16020/tcp': 16020,'16030/tcp': 16030})
	#print(se_docker.exec_command('hbasenode' + '.' + config.domain_name,"echo \"create 'hbaseTestTable','status'\" | hbase shell"))
	print(se_docker.exec_command('masternode' + '.' + config.domain_name,"su -l hbase -c '/usr/hdp/current/phoenix-server/bin/queryserver.py start'"))


def del_hadoop_containers():
	print('\n====Stopping and deleting Containers for hdfs====\n')
	for i in se_docker.get_all_containers():
		if 'masternode' in i.name or 'slavenode' in i.name or 'clientnode' in i.name:
			print('Stopping and deleting Container: {}\n'.format(i.name))
			i.remove(force=True)
