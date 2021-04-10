#!/bin/sh
cd /home/sched-bot
python3 main.py

echo "Bot script starting"
while true; do
        cd /home/sched-bot
		python3 main.py
	sleep 6
done
