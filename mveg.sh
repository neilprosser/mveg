#!/bin/bash

[ -e /etc/sysconfig/mveg ] && . /etc/sysconfig/mveg

if [ "xx$ENVIRONMENT" = "xx" ]
then
  echo "ENVIRONMENT must be set"
  exit 1
fi

if [ "xx$APP_NAME" = "xx" ]
then
  APP_NAME="elasticsearch"
fi

if [ "xx$ES_HOST" = "xx" ]
then
  ES_HOST="localhost"
fi

if [ "xx$ES_PORT" = "xx" ]
then
  ES_PORT="9200"
fi

if [ "xx$CARBON_HOST" = "xx" ]
then
  echo "CARBON_HOST must be set"
  exit 1
fi

if [ "xx$CARBON_PORT" = "xx" ]
then
  echo "CARBON_PORT must be set"
  exit 1
fi

if [ "xx$HOSTNAME" = "xx" ]
then
  HOSTNAME=`hostname`
fi

SCRIPT_PATH="$(cd `dirname $0` && pwd)"

OUTPUT=`python $SCRIPT_PATH/mveg.py $HOSTNAME $ENVIRONMENT $APP_NAME $ES_HOST $ES_PORT`

if [ $? = 0 ]
then
  echo "${OUTPUT}" | nc -w 20 $CARBON_HOST $CARBON_PORT
fi
