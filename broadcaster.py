import subprocess,sys,os,random
rng = random.SystemRandom()
from configparser import ConfigParser
config = ConfigParser()
config.read("config.ini")
if len(sys.argv)!=2:
	print("Usage: python3 broadcaster.py <station>")
	sys.exit(1)
if sys.argv[1] not in config.sections() and sys.argv[1]!="genlist":
	print("Error: Invalid section {!r}! (Did you forget to add a configuration section for it?)")
	sys.exit(127)
station=config[sys.argv[1]] if sys.argv[1]!="genlist" else {}

INTRO = "bumps/bump-00000.mp3"
OUTRO = "bumps/bump-00001.mp3"
BUMPS = ["bumps/"+x for x in os.listdir("bumps") if ("bumps/"+x) not in (INTRO,OUTRO)]
MUSIC = ["music/"+x for x in os.listdir("music")]
BUMPC = 5
MUSCNT = 30
MAXATT = 15

print(" - {!s} possible track{}".format(len(MUSIC),"" if len(MUSIC)==1 else "s"))
if len(MUSIC)>MUSCNT:
	print(" - Limited to {!s} track{}".format(MUSCNT,"" if MUSCNT==1 else "s"))
print(" - Asked to place {!s} bump{}".format(BUMPC,"" if BUMPC==1 else "s"))

rng.shuffle(MUSIC)
MUSIC = MUSIC[:MUSCNT]
SHOW = [INTRO]+MUSIC+[OUTRO]
print(" - {!s} tracks in the show (w/o bumps)".format(len(SHOW)))
while BUMPC>0:
	att = MAXATT
	print(" - now {!s} tracks ({!r})".format(len(SHOW),SHOW))
	i = rng.randint(1,len(SHOW)-2) # don't let it generate the index 0 or the index of SHOW[-1] (no before/after the intro)
#	print(" - Trying position {!s} ({!s},{!s},{!s})".format((i+1),SHOW[((i-1)%len(SHOW))],SHOW[((i+1)%len(SHOW))],len(SHOW)))
	while SHOW[i] in BUMPS or SHOW[(i-1)%len(SHOW)] in BUMPS or SHOW[(i+1)%len(SHOW)] in BUMPS: # no bumps in a row
		att -= 1
		if att==0:
			break
		i = rng.randint(1,len(SHOW)-2)
#		print(" - Trying position {!s} ({!s},{!s},{!s})".format((i+1),SHOW[((i-1)%len(SHOW))],SHOW[((i+1)%len(SHOW))],len(SHOW)))
	if att==0:
		print(" - Unable to place a bump; quitting early")
		break
	print(" - Inserting bump at position {!s}".format(i+1))
	SHOW.insert(i,rng.choice(BUMPS))
	BUMPC-=1

#with open("tracks.pls","w") as f:
#	f.write("\n".join(SHOW))
with open("tracks.pls") as f:
	SHOW = [l.strip() for l in f if l.strip()]

if sys.argv[1]=="genlist":
	subprocess.run = print
	class Duh:
		def __getitem__(self,k):
			return k
	station = Duh()
#print(["/usr/bin/liquidsoap",'output.icecast(%mp3,host="{station[host]}",port={station[port]},mount="{station[mount]}",user="{station[user]}",password="{station[password]}",mksafe(playlist.once("tracks.pls")),on_stop=shutdown)'.format(station=station)])
subprocess.run(["/usr/bin/liquidsoap",'output.icecast(%mp3,host="{station[host]}",port={station[port]},mount="{station[mount]}",user="{station[user]}",password="{station[password]}",mksafe(playlist.once("tracks.pls")),on_stop=shutdown)'.format(station=station)])
