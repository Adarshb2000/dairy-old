import os
import re
import subprocess


text = subprocess.call("ssh -R 80:192.168.29.62:5000 ssh.localhost.run")
print(str(text))