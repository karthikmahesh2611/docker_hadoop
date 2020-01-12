# Contents

1. [About the Script](#about-the-script)

2. [Usage](#usage)

3. [Hadoop Environment](#hadoop-environment)

------

### About the Script

* This is a python3 script to help developers setup a local Hadoop development docker cluster setup on their Linux workstation.
* Includes **HDFS, YARN, Spark2, HBase and Apache Phoenix** with full cluster setup having master and slave nodes.
* The folder **'bind_mounts'** is used to share code from your local workstation into the docker environment for integrated testing.
* The Hadoop setup currently uses the **Hortonworks Data Platform (HDP) verion HDP 2.6.5**
* Has been tested on Centos7 work station 

------

### Usage

1. Clone the repository on your local Centos machine.

2. Run the **initial_setup bash script** to setup your system to run the python program. This will install python3, docker-ce and other required packages if not already installed.

   ```
   #./initial_setup.sh
   ```

   <img src=".\screenshots\initial_setup_screenshot.png" style="zoom:80%;" />
   
   <img src=".\screenshots\verification_screenshots.png" style="zoom:67%;" />

3. Now the python script should be ready for use and you can see available options using the --help option.

   ```
   #python3.4 startup_script.py --help
   ```

   <img src=".\screenshots\script_options_screenshot.png" style="zoom:80%;" />

   

4. Next pull the required Docker images using the --pull option.

   ```
   #python3.4 startup_script.py --pull
   ```

   <img src=".\screenshots\image_pull_screenshot.png" style="zoom:80%;" />

5. Once the images are pulled you can start the docker containers using the --start option.

   ```
   #python3.4 startup_script.py --start
   ```

   <img src=".\screenshots\startup_screenshot.png" style="zoom: 150%;" />



------

### Hadoop Environment

Once the containers are launched you will be able to verify the Hadoop environment using the Hadoop UIs that will be accessible from you host machine as the ports have been forwarded from the docker environment.

Below are the Hadoop UI port numbers:

Hadoop Links and ports  ==>

* HDFS Namenode: http://127.0.0.1:50070
* YARN Resource manager: http://127.0.0.1:8088
* HBase web UI: http://127.0.0.1:16010
* Spark History Server: http://127.0.0.1:18080
* phoenix_query_server_port:   **8765**



##### HDFS

<img src=".\screenshots\hdfs_screenshot2.png" style="zoom:80%;" />

**Note:** *That since all the docker containers are running on the same host they falsely assume as the net availbale hard disk space as 16 GB each whereas it is overall 16 GB only. This is one side effect of simulating the hadoop docker cluster on a single host.*



##### YARN

<img src=".\screenshots\yarn_screenshot.png" style="zoom:80%;" />

##### HBASE

<img src=".\screenshots\hbase_screenshot.png" style="zoom:80%;" />

##### SPARK HISTORY SERVER

<img src=".\screenshots\spark_screenshot.png" style="zoom:80%;" />

##### APACHE PHOENIX SHELL

**Note**: To access the phoenix shell you need to first install the apache phoenix client on your host system.

* As root create the file and add the below lines to it '**/etc/yum.repos.d/hdp.repo**'

  ```
  #VERSION_NUMBER=2.6.5.0-292
  [HDP-2.6.5.0]
  name=HDP Version - HDP-2.6.5.0
  baseurl=http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.5.0
  gpgcheck=1
  gpgkey=http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.5.0/RPM-GPG-KEY/RPM-GPG-KEY-Jenkins
  enabled=1
  priority=1
  
  [HDP-UTILS-1.1.0.22]
  name=HDP-UTILS Version - HDP-UTILS-1.1.0.22
  baseurl=http://public-repo-1.hortonworks.com/HDP-UTILS-1.1.0.22/repos/centos7
  gpgcheck=1
  gpgkey=http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.6.5.0/RPM-GPG-KEY/RPM-GPG-KEY-Jenkins
  enabled=1
  priority=1
  ```

* Next install the Phoenix client using the below command

  ```
  #sudo yum install -y phoenix
  ```

* Install JAVA 1.8 if not already installed

  ```
  #sudo yum install -y java-1.8.0-openjdk
  ```

* Now you will be able to launch the phoenix shell which will connect to the phoenix server running inside the docker environment and access the phoenix/hbase tables using the below command.

  ```
  #python /usr/hdp/2.6.5.0-292/phoenix/bin/sqlline-thin.py 127.0.0.1:8765
  ```

  <img src=".\screenshots\phoenix_screenshot.png" style="zoom:150%;" />





