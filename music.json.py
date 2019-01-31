from tinytag import TinyTag
import os, json

songs = [os.path.join("music",x) for x in os.listdir("music")]
metadata = {}

for song in songs:
	md = TinyTag.get(song)
	metadata[os.path.basename(song)]=dict(performer=md.artist,title=md.title)

with open("music.json","w") as f:
	json.dump(dict(songs=metadata),f,indent=4)
