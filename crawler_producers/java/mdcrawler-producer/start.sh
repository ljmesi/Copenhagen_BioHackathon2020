#!/usr/bin/bash

class=org.perpetualnetworks.mdcrawler.Application

JAVA_OPTS="-Djavax.net.ssl.sessionCacheSize=10000 -server"

# Setting Max Heap memory based on pod's available memory
JAVA_OPTS="${JAVA_OPTS} -XX:MaxRAMPercentage=80.0"

# debugging options.
#JAVA_OPTS="${JAVA_OPTS} -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=5006"

#echo ${JAVA_OPTS}

exec java ${JAVA_OPTS} \
  -cp java-app.jar:lib/* \
  ${class}
