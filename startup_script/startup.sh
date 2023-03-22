#!/bin/sh
cd /home/denis/WebUI/webui
screen -dmS "DjangoServer" python manage.py runserver 0.0.0.0:8000
cd /home/denis/WebUI/nodejs_channel_server
screen -dmS "ChannelServer" node channel_server.js
cd /home/denis/WebUI/startup_script
./ros.sh start


