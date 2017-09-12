class Song(object):

#    def __init__(self):
#        self.lyrics = []

    lyrics = []

    def sing_me_a_song(self, lyrics):
        for line in lyrics:
            print(line)

happy_bday = Song()

happy_bday.lyrics = ["Happy birthday to you",
                    "I don't want to get sued",
                    "So I'll stop right there"]

bulls_on_parade = Song()

bulls_on_parade.lyrics = ["They rally around tha family",
                        "With pockets full of shells"]

# happy_bday.sing_me_a_song(lyrics)

bulls_on_parade.sing_me_a_song(["They rally around tha family",
                        "With pockets full of shells"])
