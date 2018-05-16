songs = []

with open('db.txt', 'r') as f:
    for line in f.readlines():
        #print(line)
        song = line[:-1].split()
        songs.append(' '.join(str(s).lower() for s in song))

