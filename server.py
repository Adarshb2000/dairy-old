import os
import re


text = os.system("ssh -R 80:192.168.29.235:1234 ssh.localhost.run &")
print(str(text))