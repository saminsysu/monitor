#!/bin/bash

set -e
set -o pipefail

agent_dir="/etc/monitor-agent/"
init_dir="/etc/init.d/"
server_url="http://172.18.215.158:5000/api/v1.0/"

# Root user detection
if [ $UID -eq 0 ]; then
    sudo_cmd=''
else
    sudo_cmd='sudo'
fi

$sudo_cmd apt-get install gcc python-dev python-pip
$sudo_cmd apt-get install python-psutil
$sudo_cmd apt-get install python-influxdb

if [ -e $agent_dir ]; then
	$sudo_cmd rm -rf $agent_dir
fi

$sudo_cmd mkdir $agent_dir

if [ -e "${init_dir}monitor-agent" ]; then
	$sudo_cmd rm "${init_dir}monitor-agent"
fi

$sudo_cmd curl -o "${agent_dir}monitor_agent.py" "${server_url}monitor_agent.py"
$sudo_cmd curl -o "${init_dir}monitor-agent" "${server_url}monitor-agent"
$sudo_cmd chmod +x "${agent_dir}monitor_agent.py"
$sudo_cmd chmod +x "${init_dir}monitor-agent"

$sudo_cmd update-rc.d "monitor-agent" defaults

$sudo_cmd /etc/init.d/monitor-agent start

echo "Your Agent is running.It will continue to run in the background and submit metrics to Influxdb.

If you ever want to stop the Agent, run:

　　sudo /etc/init.d/monitor-agent stop

And to run it again run:

　　sudo /etc/init.d/monitor-agent start

And you can also restart it with:

　　sudo /etc/init.d/monitor-agent restart"
