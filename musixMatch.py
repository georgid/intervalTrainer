'''
Created on Jun 18, 2015

@author: joro
'''
import urllib2
import json
import os
import sys
import requests
import logging
from getCoverTrackIDs import hasLyricsAndSubtitles, callMXMGetAPI,\
    getAnnotaitonForResponse
from lyricsProcessor import fetchLyricsThumbnail, parseLyricsThumbnail

# file parsing tools as external lib 
parentDir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__) ), os.path.pardir)) 

pathRedisCover = os.path.join(parentDir, 'redisCover')
# print pathRedisCover
# sys.path.append(pathRedisCover)
# from  getCoverTrackIDs import  hasLyricsAndSubtitles, callMXMGetAPI, getAnnotaitonForResponse
# from lyricsProcessor import fetchLyricsThumbnail, parseLyricsThumbnail

logger = logging.getLogger(__name__)


def getSubtitlesForATrack(trackID):
        '''
        gets thumbnail for a song and its timestamps
        ''' 
        #sanity check: has lyrics and subtitless
        response = callHasLyricsAndSubtitles(trackID)
        if not hasLyricsAndSubtitles(response):
            return None
        
        # get subtitles
        response = callMXMGetAPI(trackID)
        subtitles = getAnnotaitonForResponse(response)
        subtitles = json.loads(subtitles)
        
        return subtitles
        
def getThumbnail(trackID, subtitles):
        
        response = fetchLyricsThumbnail(trackID)
        lyricsThumbnail = parseLyricsThumbnail(response)
        lyricsThumbnail = lyricsThumbnail.lower().strip().replace(',','')
        
        
        endTs = None
        beginTs = None
        
        # loop in subtitles to match  lyrics thumbnail
        for index, subtutleLine in enumerate(subtitles):
            currSubtitle = subtutleLine['text'].lower().strip().replace(',','')
            if currSubtitle == lyricsThumbnail:
                
                # get next line to get duration
                if len(subtitles) == index+1:
                    print("subtitle line is last in lyrics. Not implemented")
                    return None, None, None, None
                
                endTs = subtitles[index+1]['time']['total']
                beginTs = subtutleLine['time']['total']
        
        
        if endTs == None and beginTs == None:
            print "thumbnail not found in subtitles"
            
        return lyricsThumbnail, beginTs, endTs     
            
        
        
def callHasLyricsAndSubtitles(trackID):
    
    # build api url
    url = "http://api.musixmatch.com/ws/1.1/track.get?apikey=3122752d0d32edee9dedd70e79141de9"
    url +="&track_id=" + str(trackID)
    url +="&format=json"

#     print url
    
    # URL lib2
    try:
        responseHTTP = urllib2.urlopen(url)
    except urllib2.HTTPError:
        pass
    
    response = json.load(responseHTTP)

    return response

def searchTrackID(artist, trackTitle):
    endpoint ='http://api.musixmatch.com/ws/1.1/track.search?'

    payload = {'apikey':'3122752d0d32edee9dedd70e79141de9'}
    payload['q_track'] = trackTitle
    payload['q_artist'] = artist
    payload['f_has_lyrics'] = '1'
    payload['f_has_subtitle']='1'
    
    import requests
    r = requests.get( endpoint, params=payload)
    print r.url
    responseJSON = r.json()
    
    if responseJSON['message']["header"]["status_code"] == 404:
        logger.warning("artist not found in musiXmatch")
        return None, None
    else:
        subtitleID = None
        trackList =  responseJSON['message']['body']['track_list']
        for track_ in trackList: # loop in diff track releasesfor same composition
            track = track_['track']
    #     print firstTrack
            trackid = track['track_id']
            trackSpotifyId = track['track_spotify_id']
            subtitleID = track['subtitle_id']
            if subtitleID != 0: # get first version with sibtitles 
                break
        
        if subtitleID == None: # no track version has subtitles
            logger.warning( "no subtitles for song")
    return trackid, trackSpotifyId, subtitleID
    

if __name__=="__main__":
    trackID = '16860631'
    subtitles = getSubtitlesForATrack(trackID)
    
    lyricsThumbnail, beginTs, endTs  = getThumbnail(trackID, subtitles)
    
    print lyricsThumbnail
    print beginTs
    print endTs
    
