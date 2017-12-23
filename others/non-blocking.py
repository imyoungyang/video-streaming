import subprocess
import time

p = subprocess.Popen(['sleep', '5'])

while p.poll() is None:
    print('Still sleeping')
    time.sleep(1)

print('Not sleeping any longer.  Exited with returncode %d' % p.returncode)
