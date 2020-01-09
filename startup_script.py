#!/usr/bin/python3
import sys
import os
import time
import multiprocessing
import argparse
from datetime import datetime
from datetime import date
from datetime import timedelta
from python_generic_modules import se_docker
from python_hadoop_modules import kafka
from python_hadoop_modules import zookeeper
from python_hadoop_modules import hadoop
from python_app_configs import config



def launch_hadoop_containers():
	print('LAUNCHING HADOOP CONTAINERS')
	zookeeper.launch_zookeeper()
	kafka.launch_kafka()
	print('KAFKA AND ZOOKEEPER CONTAINERS ARE LAUNCHED')
	hadoop.setup_hadoop_dirs()
	hadoop.launch_containers()
	hadoop.launch_hdfs()
	hadoop.launch_yarn()
	hadoop.launch_hbase()
	print('HADOOP CONTAINERS ARE LAUNCHED')
	time.sleep(3)

		
def clear_docker_env():
	print("=====CLEANING ANY EXISTING CONTAINERS=====\n")
	kafka.del_kafka_containers()
	print('KAFKA CONTAINERS ARE DELETED')
	zookeeper.del_zookeeper_containers()
	print('ZOOKEEPER CONTAINERS ARE DELETED')
	hadoop.del_hadoop_containers()
	print('HADOOP CONTAINERS STOPPED')


	print('\n====REMOVING UNUSED VOLUMES====\n')
	for i in se_docker.get_all_volumes():
		if 'mongo' not in i.name and 'grafana' not in i.name:
			print('Removing unused volume: {}\n'.format(i.name))
			i.remove(force=True)


parser = argparse.ArgumentParser()
parser.add_argument("--start", help="Start Hadoop Containers", action="store_true")
parser.add_argument("--stop", help="Stop and Delete Hadoop Containers", action="store_true")

args = parser.parse_args()

if __name__ == "__main__":
	if (args.start):
		clear_docker_env()
		launch_hadoop_containers()	
		#os.system('clear')
		print('=====HADOOP CONTANIERS ARE LAUNCHED=====\n')
		time.sleep(4)
	elif (args.stop):
		os.system('clear')
		clear_docker_env()
	else:
		print('Invalid Argument!!')
		print('See ')

