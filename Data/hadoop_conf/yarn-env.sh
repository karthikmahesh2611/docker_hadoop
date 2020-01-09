export HADOOP_YARN_HOME=/usr/hdp/2.6.5.0-292/hadoop-yarn
export YARN_LOG_DIR="/tmp"
export HADOOP_LIBEXEC_DIR=/usr/hdp/2.6.5.0-292/hadoop/libexec
JAVA=$JAVA_HOME/bin/java
# default log directory & file
if [ "$YARN_LOG_DIR" = "" ]; then
    YARN_LOG_DIR="$HADOOP_YARN_HOME/logs"
fi
if [ "$YARN_LOGFILE" = "" ]; then
    YARN_LOGFILE='yarn.log'
fi

# default policy file for service-level authorization
if [ "$YARN_POLICYFILE" = "" ]; then
   YARN_POLICYFILE="hadoop-policy.xml"
fi

# restore ordinary behaviour
unset IFS


	YARN_OPTS="$YARN_OPTS -Dhadoop.log.dir=$YARN_LOG_DIR"
	YARN_OPTS="$YARN_OPTS -Dyarn.log.dir=$YARN_LOG_DIR"
	YARN_OPTS="$YARN_OPTS -Dhadoop.log.file=$YARN_LOGFILE"
	YARN_OPTS="$YARN_OPTS -Dyarn.log.file=$YARN_LOGFILE"
	YARN_OPTS="$YARN_OPTS -Dyarn.home.dir=$YARN_COMMON_HOME"
	YARN_OPTS="$YARN_OPTS -Dyarn.id.str=$YARN_IDENT_STRING"
	YARN_OPTS="$YARN_OPTS -Dhadoop.root.logger=${YARN_ROOT_LOGGER:-DEBUG,console}"
	YARN_OPTS="$YARN_OPTS -Dyarn.root.logger=${YARN_ROOT_LOGGER:-DEBUG,console}"
if [ "x$JAVA_LIBRARY_PATH" != "x" ]; then
  YARN_OPTS="$YARN_OPTS -Djava.library.path=$JAVA_LIBRARY_PATH"
fi
  YARN_OPTS="$YARN_OPTS -Dyarn.policy.file=$YARN_POLICYFILE"

