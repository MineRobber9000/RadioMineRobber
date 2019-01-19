import shouty, time, sys
from tinytag import TinyTag
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")
if len(sys.argv)!=2:
	print("Usage: python3 broadcaster.py <station>")
	sys.exit(1)
if sys.argv[1] not in config.sections():
	print("Error: Invalid station {!r}! (Did you forget to configure it?)")
	sys.exit(127)
config = config[sys.argv[1]]
params = {}
for k in config.keys():
	params[k]=config[k]
	if k=="port":
		params[k]=int(params[k])
	elif k=="format":
		params[k]=getattr(shouty.Format,params[k].upper())

with open("playlist.txt") as f:
	files = [l.strip() for l in f if l.strip()]
metadata = [TinyTag.get(f) for f in files]

with shouty.connect(**params) as c:
	for i in range(len(files)):
		c.send_file(files[i])
		c.sync()
		print("Sent {}".format(files[i]))
		time.sleep(metadata[i].duration)
