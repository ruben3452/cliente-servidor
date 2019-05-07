from sfml import sf


try music = sf.Music.from_file("music/s3.ogg")
except IOError: exit(1)

#play it
music.play()
while True:
    pass
