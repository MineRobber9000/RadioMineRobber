import subprocess,sys
from configparser import ConfigParser
config = ConfigParser()
config.read("config.ini")
if len(sys.argv)!=2:
	print("Usage: python3 broadcaster.py <station>")
	sys.exit(1)
if sys.argv[1] not in config.sections():
	print("Error: Invalid section {!r}! (Did you forget to add a configuration section for it?)")
	sys.exit(127)
station=config[sys.argv[1]]

files = ["bumps/bump-00000.ogg","bumps/bump-00002.ogg","music/panicatthedisco-highhopes.ogg","bumps/bump-00001.ogg"]

with open("tracks.pls","w") as f:
	f.write("\n".join(files))

subprocess.run(["/usr/bin/liquidsoap",'output.icecast(%vorbis,host="{station[host]}",port={station[port]},mount="{station[mount]}",user="{station[user]}",password="{station[password]}",mksafe(playlist.once("tracks.pls")),on_stop=shutdown)'.format(station=station)])
