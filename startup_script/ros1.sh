#!/bin/bash
if [ "$1" = "stop" ] || [ "$1" = "restart" ]; then
    ps axf | grep start_robot_and_web.launch | grep -v grep | awk '{print "kill -9 $(pgrep -P " $1 ") ; kill -9 " $1}' | sh
    sleep 5
fi

if [ "$1" = "start" ] || [ "$1" = "restart" ]; then
    cd ~/WebUI/ros_launch_files/
    if [ "$2" = "silent" ]; then
      roslaunch start_robot_and_web.launch >~/WebUI/ros_launch_files/stdout 2>~/WebUI/ros_launch_files/stderr &
    else
      roslaunch start_robot_and_web.launch
    fi
fi
