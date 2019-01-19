from gtts import gTTS
from time import sleep

DELAY = 4 # Tweak if Google gives 429s or refuses to convert

with open("bumplist.txt") as f:
	bumps = [l.rstrip() for l in f if l.rstrip()]

SERIAL = 0
for bump in bumps:
	b = gTTS(bump)
	b.save("bumps/bump-{:05}.mp3".format(SERIAL))
	SERIAL+=1
	sleep(DELAY)
