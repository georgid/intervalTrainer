'''
Created on Jun 18, 2015

@author: joro
'''


from flask import Flask
from flask import request
import json
from musixMatch import searchTrackID, getSubtitlesForATrack, getThumbnail
import logging
from museScoreParser import getNotesList, parseNoteList, getIntervalsFromScore
app = Flask(__name__)

logger = logging.getLogger(__name__)


# @app.route('/user/<username>')
# def show_user_profile(username):
#     # show the user profile for that user
#     return 'User blah %s' % username

@app.route('/', methods=['GET', 'POST'])
def parse_request():
    if request.method == 'POST':
        print "post"
        result = parseRequest(request)
    elif request.method == 'GET':
        result ="get result"
        print "get"
    return result

def parseRequest(request):
#     body = request.body.read()
#     print "body: {} ".format(body)
    
    from flask import jsonify
    responseVal = ""
    
    dataString = request.data
    data = json.loads(dataString)
    artistName = data["artist"]
    
    songList = data["songs"]
    if len(songList) == 0:
        logger.warning("no songs with scores with lyrics for artist ")
        return
    
    subtitles = None
    for track in songList: 
        trackTitle = track["name"]
        print trackTitle
    
    ######### get MXM stuff 
        trackid, trackSpotifyId, subtitleID = searchTrackID(artistName, trackTitle)
        if subtitleID == None:
            statusVal =""
            responseVal = ""
            
            
        elif subtitleID != 0: 
            subtitles = getSubtitlesForATrack(trackid)
            lyricsThumbnail, beginTs, endTs  = getThumbnail(trackid, subtitles)
            
            # HARD CODED:
            lyricsThumbnail = "tall and tan and young and lovely"
            
            print ("lyricsThumbnail is : " + lyricsThumbnail)
            
            # get intervals for lyricsThumbnail from museScore
            interval,  listSyllables, idxSyllable = getIntervalsFromScore(trackTitle, lyricsThumbnail)
            
            statusVal ="OK"
            responseVal = {'trackSpotifyId':trackSpotifyId, 'beginTs':beginTs, 'endTs':endTs, 'interval':interval, 'syllables':listSyllables, 'idxSyll':idxSyllable}
            # TODO: check length of audio makes sense for playback
            break
        
    if subtitles == None:
        logger.warning( "no subtitles for any song")
        statusVal =""
        responseVal = ""
    
    
    
     
    return jsonify(status=statusVal, reponse=responseVal)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0')