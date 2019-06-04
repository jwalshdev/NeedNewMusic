import collections
import operator
import pandas as pd
import datetime
from settings import sp, conn

def checkUpdateLog(artist, date, alb):
    try:
        df = pd.read_sql('select * from dates',conn)
    except:
        df = pd.DataFrame()
    try:
        rdate = df[artist][0]
        new = False
    except:
        print()
        print(f"\t\t{artist} is not yet in the database. Adding now.")
        new = True
        df[artist] = ['2012-01-01']
        rdate = df[artist][0]

    if datetime.datetime.strptime(date, '%Y-%m-%d') > datetime.datetime.strptime(rdate, '%Y-%m-%d'):
        print(f"\t\t{alb} by {artist} is new as of {date}.")
        df[artist] = [date]
        print()
    df.to_sql('dates', conn, if_exists='replace', index=False)

def show_artist_albums(id):
    albums = []
    results = sp.artist_albums(id, album_type='album')
    albums.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])
    print('Total albums:', len(albums))
    unique = set()  # skip duplicate albums
    for album in albums:
        try:
            alb_date = album['release_date']
            name = album['name'].lower()
            print(f'\t{name}')
            checkUpdateLog(album['artists'][0]['name'], alb_date, name)
            if not name in unique:
                unique.add(name)
        except ValueError:
            print(f"Error on {name} by {album['artists'][0]['name']}")


def getSuggestions(recs, rec_thresh, art_list):
    plist = []
    for r in recs:
        r2 = r
        while len(r2) < 20:
            r2 += ' '
        if recs[r] >= rec_thresh*len(art_list) and r not in art_list:
            plist.append(f'{r2}{recs[r]}')
    if len(plist)==0:
        rec_thresh -= .1
        getSuggestions(recs, rec_thresh, art_list)
    else:
        print('\n\n' + '-' * 20 + 'SUGGESTIONS' + '-' * 20)
        for item in plist:
            print(item)

def getAlbums(n):
    results = sp.search(q=n, type='artist')
    artists = results['artists']['items']
    max = 0
    saved = None
    for i in artists:
        foll = int(i['followers']['total'])
        if foll > max:
            max = foll
            saved = i['id']
    show_artist_albums(saved)
    return saved

def getRecs(saved, recs):
    related = sp.artist_related_artists(saved)
    for i in related['artists']:
        try:
            recs[i['name']] +=1
        except KeyError:
            recs.setdefault(i['name'], 1)
    return recs

def sortDict(d):
    sorted_x = sorted(d.items(), key=operator.itemgetter(1))
    sorted_d = collections.OrderedDict(sorted_x)
    return sorted_d

def getNewest(conn):
    df = pd.read_sql('select * from dates', conn)
    dlist = []
    for col in list(df.columns.values):
        dlist.append(df[col][0])
    dlist = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in dlist]
    max_d = max(dlist)
    for col in list(df.columns.values):
        if datetime.datetime.strptime(df[col][0], '%Y-%m-%d') == max_d:
            print(f'\nThe newest album is {col} on {max_d}')
