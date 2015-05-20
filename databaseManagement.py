from urllib import request
import xml.etree.ElementTree as ET
import pickle
from collections import Counter
import re
from nltk.corpus import stopwords
from PyLyrics import *
from nltk.stem.wordnet import WordNetLemmatizer
import gui as gui
from tkinter import END

my_bag_c = {}


def download_list_of_artists():
    x = "http://ws.audioscrobbler.com/2.0/" \
        "?method=chart.gettopartists&api_key=d70d8067d56b2afc78942623d4256817&limit=1000"
    request.urlretrieve(x, "scrobble.xml")


def parse_file_by_moonko(number_of):
    if number_of < 0 or number_of > 500:
        number_of = 200
    tree = ET.parse('scrobble.xml')
    root = tree.getroot()
    list3 = []
    dictionary_per_album = {}
    counter = 0
    print(number_of)
    for x in root.findall('.//name'):
        if counter >= number_of:
            break
        counter += 1
        print(x.text, counter)
        try:
            for g in PyLyrics.getAlbums(x.text):
                try:
                    for track in PyLyrics.getTracks(g):
                        try:
                            dictionary_per_album[track.artist + "," + track.name] = \
                                PyLyrics.getLyrics(track.artist, track.name).lower()
                            # append(PyLyrics.getLyrics(track.artist, track.name).lower())
                            # print(track.artist, track.name)
                        except ValueError:
                            print(track.artist, track.name, " ERROR ")
                            pass
                except:
                    print("MEGA ERROR")
        except:
            print("GIG ERROR")
    with open("pickle" + str(number_of) + ".p", 'wb') as f:
<<<<<<< HEAD
        pickle.dump(dicto, f)
        data2 = pickle.load(open("pickle" + str(number_of) + ".p", 'rb'))
        print(data2)
=======
        pickle.dump(dictionary_per_album, f)


def parse_file_lil_version(number_of):
    if number_of < 0 or number_of > 500:
        number_of = 200
    tree = ET.parse('scrobble.xml')
    root = tree.getroot()
    to_simpler_form = WordNetLemmatizer()
    dictionary_per_album = {}
    dictionary_for_artist = {} # pickle.load(open("pickleLilEvery.p", 'rb'))
    list_of_song_per_album = {}
    list_of_average = {}
    counter = 0
    songs = {}
    print(number_of)
    for x in root.findall('.//name'):
        # starting from always num - 1
        if counter > -1:
            counter += 1
            if counter >= number_of:
                break
            print("Artist: ", x.text, counter)
            # going to albums
            try:
                for g in PyLyrics.getAlbums(x.text):
                    # going to tracks in album

                    try:
                        print("ALBUM", x.text, " : ", g.name, " Parsing... ")
                        for track in PyLyrics.getTracks(g):
                            # going to lyric in song
                            try:
                                print(track.artist, " : ", g.name, " : ", track.name, " : ")

                                # operation on lyrics
                                song = PyLyrics.getLyrics(track.artist, track.name).lower().split()
                                song = [word for word in song if word not in stopwords.words('english')]
                                song = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in song]

                                # changing word for simple form running -> run
                                song = [to_simpler_form.lemmatize(x, 'v') for x in song]

                                # Counting words per album
                                try:
                                    dictionary_per_album[track.artist + "," + g.name] = \
                                        dictionary_per_album[track.artist + "," + g.name] + Counter(song)
                                    # counting songs per album
                                    list_of_song_per_album[track.artist + "," + g.name] += 1
                                except:
                                    dictionary_per_album[track.artist + "," + g.name] = Counter(song)
                                    list_of_song_per_album[track.artist + "," + g.name] = 1

                                # print(dictionary_per_album[track.artist + "," + g.name])

                                # Counting words per artist
                                try:
                                    dictionary_for_artist[track.artist] = \
                                        Counter(dictionary_for_artist[track.artist]) + Counter(song)
                                except:
                                    dictionary_for_artist[track.artist] = Counter(song)
                            except:
                                print(" ERROR ")
                                pass
                        print("Per album " + g.name + " : ", dictionary_per_album[x.text + "," + g.name])
                        list_of_average[x.text + "," + g.name] = \
                            sum(dictionary_per_album[x.text + "," + g.name].values())\
                            / list_of_song_per_album[x.text + "," + g.name]
                        print("Average of word per song in specific album :: " + str(list_of_average[x.text + "," + g.name]))
                        # print("Songs Per album " + track.name + " : ", my_bag_c[track.artist + "," + track.album])
                    except:
                        print("MEGA ERROR")
                print()
                print("Artist : ", x.text, "\All : ", dictionary_for_artist[x.text])
                print()
            except:
                print("GIG ERROR")
        else:
            counter += 1
    with open("pickleLil" + str(number_of) + ".p", 'wb') as f:
        pickle.dump(dictionary_per_album, f)
    with open("pickleLilEvery" + ".p", 'wb') as l:
        pickle.dump(dictionary_for_artist, l)
    with open("pickleLilWordPerSong" + ".p", 'wb') as d:
        pickle.dump(list_of_average, d)


def get_music_stats(self):
    data2 = pickle.load(open("pickleLilEvery.p", 'rb'))
    print(len(list(data2)))
    print_database(self, data2)


def print_database(self, data):
    self.left_list.delete(0, END)
    for x in sorted(list(data), key=lambda s: s.lower()):
        print(x, " : Summary words : ", len(data[x]))
        gui.GUI.insert_to_left_list_box(self, x + " Summary words : " + str(len(data[x])))


def get_music_stats_by_album(self):
    try:
        data2 = pickle.load(open("pickleLil50.p", 'rb'))
        data1 = pickle.load(open("pickleLil100.p", 'rb'))
        data3 = pickle.load(open("pickleLil200.p", 'rb'))
        data2.update(data3)
        data2.update(data1)
        print_database(self, data2)
    except IOError:
        print("Nothing")
>>>>>>> MyBranchYuri
