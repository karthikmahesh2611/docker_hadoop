import sys
sys.path.insert(0, "../")
from python_app_configs import config
#from genric_os_modules import se_os
import docker
import os


dkr_socket = docker.from_env()


def build_images():
	for img_name in config.docker_image_dir:
		if dkr_socket.images.list(name=str(img_name)):
			print("Docker image '{}' already exists\n================\n".format(img_name))
		else:
			try:
				print("Pulling image {}:latest".format(img_name))
				print("Wait..")
				dkr_socket.images.pull(img_name,tag='latest')
			except Exception as error:
				print("Image Pull failed for '{}' due to error: {}\n================\n".format(img_name,error))
			else:
				print("Pull successful for '{}'\n================\n".format(img_name))


def del_images():
	for i in dkr_socket.images.list():
		dkr_socket.images.remove(image=i.id)


def del_all_containers():
	dkr_socket.containers.prune()

def lst_all_containers():
	for i in se_os.linux_execute('docker container ls'):
		print(i)

#Returns container objects
def get_all_containers():
	for i in dkr_socket.containers.list(all=True):
		yield(i)

def get_all_networks():
	for i in dkr_socket.networks.list():
		yield(i)

def get_all_volumes():
	for i in dkr_socket.volumes.list():
		yield(i)

def del_container(cntr_name):
	try:
		container = dkr_socket.containers.get(str(cntr_name))
		container.remove(force=True)
	except Exception as error:
		print('Cannot delete container {} due to error: {}\n'.format(cntr_name,error))
	else:
		print('Deleted container {}'.format(cntr_name))

def launch_containers_new(image_name,run_command,cntr_name,host_name,mount_objs,net_name='bridge',tty_value=True,detach_value=True,**kwargs):
	if 'port_map' in kwargs:
		dkr_socket.containers.run(image=str(image_name),command=str(run_command),name=str(cntr_name),hostname=str(host_name),network=str(net_name),mounts=mount_objs,tty=bool(tty_value),detach=bool(detach_value),ports=kwargs['port_map'])
	else:
		dkr_socket.containers.run(image=str(image_name),command=str(run_command),name=str(cntr_name),hostname=str(host_name),network=str(net_name),mounts=mount_objs,tty=bool(tty_value),detach=bool(detach_value))
	print('Container succesfully launched for {}'.format(cntr_name))

def launch_containers_grafana(image_name,cntr_name,host_name,mount_objs,net_name='bridge',tty_value=True,detach_value=True,**kwargs):
	dkr_socket.containers.run(image=str(image_name),name=str(cntr_name),hostname=str(host_name),network=str(net_name),mounts=mount_objs,tty=bool(tty_value),detach=bool(detach_value),ports=kwargs['port_map'])
	print('Container succesfully launched for {}'.format(cntr_name))

def launch_containers(image_name,run_command,cntr_name,host_name,bind_volumes,net_name='bridge',tty_value=True,detach_value=True,**kwargs):
	if 'port_map' in kwargs:
		dkr_socket.containers.run(image=str(image_name),command=str(run_command),name=str(cntr_name),hostname=str(host_name),network=str(net_name),volumes=bind_volumes,tty=bool(tty_value),detach=bool(detach_value),ports=kwargs['port_map'])
	else:
		dkr_socket.containers.run(image=str(image_name),command=str(run_command),name=str(cntr_name),hostname=str(host_name),network=str(net_name),volumes=bind_volumes,tty=bool(tty_value),detach=bool(detach_value))
	print('Container succesfully launched for {}'.format(cntr_name))

def create_volume(volume_name):
	try:
		dkr_socket.volumes.get(str(volume_name))
	except:
		dkr_socket.volumes.create(name=str(volume_name))
		print("Volume creation successfull with id '{}'".format(volume_name))
	else:
		print("Volume already exists")


def create_mounts(target,source,driver_type,read_only_bool):
	mount_obj = docker.types.Mount(target,source,type=driver_type, read_only=read_only_bool)
	return mount_obj

def del_volume(volume_name):
	try:
		volume = dkr_socket.volumes.get(str(volume_name))
		volume.remove()
	except Exception as error:
		print("Unable to delete Volume '{}' due to error: {}".format(volume_name,error))
	else:
		print("Volume '{}' deleted successfully".format(volume_name))

#Subnet example
#subnet='192.168.52.0/24'
def create_network(net_name,subnet_ip,gateway_ip):
	ipam_pool = docker.types.IPAMPool(subnet=str(subnet_ip),gateway=str(gateway_ip))
	ipam_config = docker.types.IPAMConfig(pool_configs=[ipam_pool])
	try:
		network = dkr_socket.networks.get(str(net_name))
	except:
		dkr_socket.networks.create(str(net_name),ipam=ipam_config)
		print("Network creation successfull for '{}'".format(net_name))
	else:
		if network.attrs['IPAM']['Config'][0]['Subnet'] == str(subnet_ip) and network.attrs['IPAM']['Config'][0]['Gateway'] == str(gateway_ip):
			print('Network name already exists with the same subnet and gateway ip. Nothing to do \n')
		else:
			print('Network name already in use with a different subnet or gateway ip.\nDeleting the existing docker network to recreate with new configs.')
			try:
				network.remove()
			except Exception as error:
				print("Unable to delete existing Network '{}' due to error: {}".format(net_name,error))
				print('Delete the existing network manually and rerun the script')
				print('Exiting script')
				sys.exit(1)
			else:
				print('Deleted old network. Recreating network.')
				create_network(net_name,subnet_ip,gateway_ip)


def del_network(net_name):
	try:
		network = dkr_socket.networks.get(str(net_name))
		network.remove()
	except Exception as error:
		print("Unable to delete Network '{}' due to error: {}".format(net_name,error))
	else:
		print("Network '{}' deleted successfully".format(net_name))


def disconnect_network(cntr_name,net_name='bridge'):
	try:
		network = dkr_socket.networks.get(str(net_name))
		network.disconnect(str(cntr_name))
	except Exception as error:
		print("Unable to disconnet container '{}' from network '{}' due to error: {}".format(cntr_name,net_name,error))
		
	else:
		print("Container '{}' succesfully diconnected from {}".format(cntr_name,net_name))
	
def connect_network(cntr_name,net_name,ip_addr):
	network = dkr_socket.networks.get(str(net_name))
	network.connect(str(cntr_name),ipv4_address=str(ip_addr))
	print("Container '{}' sucessfully connected to {}".format(cntr_name,net_name))
#	try:
#		network = dkr_socket.networks.get(str(net_name))
#		network.connect(str(cntr_name),ipv4_address=str(ip_addr))
#	except:
#		print("Unable to connect container '{}' to network {}".format(cntr_name,net_name))
#		
#	else:
#		print("Container '{}' sucessfully connected to {}".format(cntr_name,net_name))
#	finally:

def exec_command(cntr_name,cmd,detach_bool=False,work_dir='/',tty_bool=False):
	print("Executing command '{}' on the container '{}'".format(cmd,cntr_name))
	container = dkr_socket.containers.get(str(cntr_name))
	if detach_bool:
		container.exec_run(cmd=str(cmd),workdir=str(work_dir),detach=detach_bool,tty=tty_bool)
	else:
		out = container.exec_run(cmd=str(cmd),workdir=str(work_dir),detach=detach_bool,tty=tty_bool)
		return(out[1].decode("utf-8"))







	

