'''
Created on Jun 19, 2015

@author: joro
'''
import requests
import json

def ServerTest():
    
    
    
    artistName='Astrud Gilberto'
    name1= 'girl from ipanema'
    name2= 'how insensitive'
    
    
    
    listSongs = []
    song1 = {'name':name1}
    song2 = {'name':name2}
    listSongs.append(song1)
    listSongs.append(song2)
    
    
    query = {'artist':artistName, 'songs':listSongs}
    
    import json
    
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    
    endpoint = 'http://10.172.8.161'
    url = endpoint + ':5000/'
    
    import requests
    r = requests.post(url, data=json.dumps(query), headers=headers)
    print r.text