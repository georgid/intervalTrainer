'''
Created on Jun 18, 2015

@author: joro
'''
import sys
from Cython.Compiler.Naming import self_cname
from docutils.nodes import note


class Note(object):
    def __init__(self, pitchMIDI, lyric):
        self.pitchMIDI = pitchMIDI
        # interval from this note to next note
        self.intervalToNext = None
        self.lyric = lyric  
        
    def setInterval(self, interval):
        self.intervalToNext = interval

class MelodicMotif(object):
    def __init__(self, notes):
        if len(notes) == 0:
            sys.exit("no notes in list of notes. cannot construct motif")

        self.notes = notes
        self._intervalize()
     
     
    def _intervalize(self):
        for i in range(len(self.notes) - 1):
             currNote = self.notes[i]
             nextNote = self.notes[i+1]
             currNote.setInterval(nextNote.pitchMIDI - currNote.pitchMIDI)
            
    def getFirstInterval(self):
        '''
        # return first non-trivial interval and its lyrics
        '''
        for i in range(len(self.notes) - 1):
            currNote = self.notes[i]
            if not currNote.intervalToNext == 0 and not currNote.intervalToNext == 1 and not currNote.intervalToNext == -1: # exclude trivial intervals in the beginning
                return currNote.intervalToNext, i
             
    def getLyricSyllables(self):
        listSyllables = []
        for note in self.notes:
            listSyllables.append(note.lyric)
        return listSyllables
       
    def printIntervals(self):
        for note in self.notes:
            print note.intervalToNext
        


        

if __name__=="__main__":
    
    note1 = Note(62, "I")
    note2 = Note(62,"am") 
    note3 = Note(68, "mine")
    
    notes = []
    notes.append(note1)
    notes.append(note2)
    notes.append(note3)
      
    melodicMotif = MelodicMotif(notes)
    melodicMotif.printIntervals()
    interval, lyric1, lyric2 = melodicMotif.getFirstInterval()
    print interval, lyric1, lyric2