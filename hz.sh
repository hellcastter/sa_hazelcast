#!/bin/bash

start_node() {
  local port=$1
  echo "Starting Hazelcast node: $port"
  hz start -c "$PWD/hazelcast.xml" -p $port &
}

stop_nodes() {
  echo "Stopping all Hazelcast nodes..."
  pkill -f 'hazelcast'
}

case "$1" in
  start)
    start_node 5701
    start_node 5702
    start_node 5703

    sleep 6
    echo "Hazelcast nodes started"
    ;;
  stop)
    stop_nodes
    sleep 1
    echo "Hazelcast nodes stopped"
    ;;
  *)
    echo "Usage: $0 {start|stop}"
    exit 1
    ;;
esac
