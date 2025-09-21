#
# Manager start script using cron
# crontab -e: 30 * * * * cd /home/user1337/finbot && /usr/bin/python3 /home/user1337/finbot/manager.py
#
import sys
import subprocess

# Check if we already have been started
# Exit if there is process manager.py
raw_stdout = subprocess.check_output(["ps", "-ax"])
stdout = raw_stdout.decode()
if "finbot.py" in stdout:
    sys.exit()


# Infinite cycle
while True:
    stdout = subprocess.check_output(["python3", "finbot.py"])
