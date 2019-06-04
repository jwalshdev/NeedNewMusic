from helpers import getSuggestions, getNewest, getAlbums, getRecs
from settings import rec_thresh, conn

##########LIST OF ARTISTS##########
art_list = ['Logic', 'Lil Uzi Vert', 'Drake', 'Skizzy Mars', 'Chance the Rapper', 'Lil Tjay', 'DaBaby', 'Mac Miller', 'J Cole', 'Trippie Redd', 'Lil Skies', 'Joyner Lucas', 'YBN Nahmir', 'Flatbush Zombies', 'Jay Critch']
###################################
recs = {}

if __name__ == "__main__":
    for n in art_list:
        s = getAlbums(n)
        recs = getRecs(s, recs)
    getSuggestions(recs, rec_thresh, art_list)
    getNewest(conn)

conn.close()
