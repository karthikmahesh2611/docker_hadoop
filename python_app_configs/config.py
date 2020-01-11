import os

####################Base configs###############################

docker_image_dir=['kmahesh2611/centosbase','kmahesh2611/java','kmahesh2611/hdp2.6.5','kmahesh2611/kafka','kmahesh2611/zookeeper','kmahesh2611/hadoopclient']
hadoop_network_range = '10.0.5.0'
domain_name = 'theitnoob.com'
dest_dir = os.path.join(os.getcwd(),'bind_mounts')
data_dir = os.path.join(os.getcwd(),'Data')
docker_file_dir = os.path.join(os.getcwd(),'dockerfiles_dir')

####################hadoop_configs###############################
slavenodes = 3
kafka_nodes = 1
zookeeper_nodes = 1
yarn_nodemanager_resource_cpu_vcores = 2
yarn_scheduler_minimum_allocation_vcores = 1
yarn_scheduler_maximum_allocation_vcores = 2

yarn_scheduler_minimum_allocation_mb = 1536
yarn_scheduler_maximum_allocation_mb = 4608
yarn_nodemanager_resource_memory_mb = 4608

mapreduce_map_memory_mb = 1536
mapreduce_map_java_opts = 1228
mapreduce_reduce_memory_mb = 3072
mapreduce_reduce_java_opts = 2457
yarn_app_mapreduce_am_resource_mb = 3072
yarn_app_mapreduce_am_command_opts = 2457
mapreduce_task_io_sort_mb = 614
yarn_nodemanager_vmem_pmem_ratio = 2.1


###################kafka topics##########################################
kafka_topics = ['test1']
kafka_default_partitions = kafka_nodes