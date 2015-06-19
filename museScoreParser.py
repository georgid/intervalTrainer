'''
Created on Jun 19, 2015

@author: joro
'''

from music21 import *
import os
import json
import requests
import urllib
from MelodicMotif import MelodicMotif, Note
 
def findSentence(sentence, musicxmlFile):
    sentence = sentence.lower()
    try:
        score = converter.parse(musicxmlFile) 
    except AttributeError :
        print "error parsing " + musicxmlFile
        return ""
    found = False
    curPart = 0
    for part in score.parts:
        lyrics = text.assembleLyrics(part).lower()
        if sentence in lyrics:
            found = True
            curPart = part
 
    if found:
        lyrics =[]
        sentenceCopy = sentence
        for note in curPart.flat.getElementsByClass('Note'):
            if sentenceCopy == "":
                break
            if len(note.lyrics) > 0:
                pitch = note.pitch.midi
                lyric = note.lyrics[0].text.lower()
                if sentenceCopy.startswith(lyric):
                    lyrics.append({"pitch":pitch, "lyric": lyric})
                    sentenceCopy = sentenceCopy[len(lyric):].strip()
                elif sentenceCopy != "":
                    sentenceCopy = sentence
                    lyrics = []
#         print json.dumps(lyrics)
        return json.dumps(lyrics)
 
def getNotesList(title, sentence):
    titleParts = title.split(" ")
    title = ""
    for titlePart in titleParts:
        title = title + "+" + titlePart + " "
    title = title.strip()
#     print title
    for p in range(0,1):
        r = requests.get('http://api.musescore.com/services/rest/score.json?oauth_consumer_key=musichackday2014&text='+urllib.quote_plus(title)+"&lyrics=1")
        print r.url
        scores = r.json()
        print "len scores = {}".format(len(scores))
        for score in scores:
            url = "http://static.musescore.com/" + score['id'] + "/" + score['secret'] + "/score.mxl"
            r = requests.get(url)
            filename = "xml/" + score['id'] + ".mxl"
            with open(filename, "wb") as xmlFile:
                xmlFile.write(r.content)
#             print url
            result = findSentence(sentence, filename)
            #os.remove(filename)
            if result:
                return result

def parseNoteList(noteListJSONArray):
    noteList = []
    noteListJSONArray = json.loads(noteListJSONArray)
    for noteItem in noteListJSONArray:
        currNote = Note(noteItem["pitch"], noteItem["lyric"])
        noteList.append(currNote)
    melodicMotif = MelodicMotif(noteList)
    return melodicMotif

def getIntervalsFromScore(trackTitle, lyricsThumbnail):
    '''
    top-most logic
    '''
    noteListJSONArray = getNotesList(trackTitle, lyricsThumbnail)
    if noteListJSONArray:
        melodicMotif = parseNoteList(noteListJSONArray)
    
    interval, idxSyllable = melodicMotif.getFirstInterval()
    listSyllables = melodicMotif.getLyricSyllables()
    return interval, listSyllables, idxSyllable

if __name__=="__main__":
    outDir = "xml"
    if not os.path.exists(outDir):
        os.mkdir(outDir)
       
    trackTitle = "girl from Ipanema"
    sentence = "tall and tan and young and lovely"
    #musicxmlFile = 'Girl_from_Ipanema.mxl'
    #findSentence(sentence, musicxmlFile)
    
    interval, listSyllables, idxSyllable = getIntervalsFromScore(trackTitle, sentence)
    print interval, listSyllables, idxSyllable