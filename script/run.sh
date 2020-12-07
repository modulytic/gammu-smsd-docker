#! /bin/bash

python3 config.py

pip3 install -r requirements.txt

# Create a new smsd for each dongle conf
for file in /app/smsdrcs/*; do
    gammu-smsd -c $file -d
done

tail -f /var/log/gammu.log
