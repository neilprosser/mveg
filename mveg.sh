#!/bin/bash
#
# Use me like this:
# /path/to/me.sh | nc -w 20 {graphite_host} {graphite_port}
#

function get() {
  code=1
  while [ $code -ne 0 ]
  do
    response=`curl --silent "$1" -m 1`
    code=$?
  done
}

script=`readlink -f $0`
path=`dirname $script`
port="8080"
environment="Live"

get "http://localhost:$port/_nodes/_local/stats?all=true"
echo $response | python $path/mveg.py $environment
