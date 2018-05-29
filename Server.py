from flask import Flask
from flask_ask import Ask, statement, question
from flask import request
from mutagen.mp3 import MP3

app = Flask(__name__)
ask = Ask(app, '/')


import serial
import time  
import vlc   

player = vlc.MediaPlayer()
counter = 0

state = {
  "Happy": 0, 
  "Neutral": 0,
  "Angry": 0, 
  "Sad" : 0
  }

#Arduino = serial.Serial("/dev/ttyACM0",9600)


def calculateState( mood ):
    global counter
    global state
   
    counter += 1
    if counter == 1:
        state[mood]= 1
        return question("How was your day?")
    elif counter == 2:
        counter = 0
        state[mood]= 2
        return statement("Trying to calculate your state...")

@ask.launch
def handler():
    global counter
    global player
    if player.is_playing():
        return statement("Humour dj is already playing a song, wait!")
    else:
        return question("Hi! I can play a song for you based on your current mood. First of all, how are you?")

@ask.intent('Happy')
def happy():
    global counter
    global state
    counter += 1
    if counter == 1:
        state["Happy"]+= 1
        return question("And now, tell me, how was your day?")
    elif counter == 2:
        counter = 0
        state["Happy"]+= 1
        chooseSong()
        
        return statement("This is the song  i chose for you, i hope you like it! ")
        
        
        
@ask.intent('Neutral')
def neutral():
    global counter
    global state
    counter += 1
    if counter == 1:
        state["Neutral"]+= 1
        return question("And now, tell me, how was your day?")
    elif counter == 2:
        counter = 0
        state["Neutral"]+= 1

        chooseSong()
        
        return statement("This is the song  i chose for you, i hope you like it!")

@ask.intent('Angry')
def angry():
    global counter
    global state
    counter += 1
    if counter == 1:
        state["Angry"]+= 1
        return question("And now, tell me, how was your day?")
    elif counter == 2:
        counter = 0
        state["Angry"]+= 1
        chooseSong()
        
        return statement("This is the song  i chose for you, i hope you like it!")

@ask.intent('Sad')
def sad():
    global counter
    global state
    global player 
    
    counter += 1
    if counter == 1:
        state["Sad"]+= 1
        return question("And now, tell me, how was your day?")
    elif counter == 2:
        counter = 0
        state["Sad"]+= 1
        chooseSong()
        return statement("This is the song  i chose for you, i hope you like it!")
        
        
def chooseSong():
    global ser
    global player 
    global state
    if state["Happy"] == 2 or ( state["Happy"] ==1 and state["Angry"]==1  ) or (state["Happy"] ==1 and state["Sad"]==1 ):
        player = vlc.MediaPlayer("/home/pi/MS/music/happy/Mika - We Are Golden.mp3")
        player.play()
        #Arduino.write(b'H')
      
    if state["Neutral"] == 2 or (state["Happy"] ==1 and state["Neutral"]==1  ):
        player = vlc.MediaPlayer("/home/pi/MS/music/neutral/Florence + The Machine - Dog Days Are Over (2010 Version).mp3")
        player.play()
        #Arduino.write(b'N')
        
    if state["Angry"] == 2 or (state["Angry"]==1 and state["Sad"]==1  ) or (state["Angry"]==1 and state["Neutral"]==1 ):
        player = vlc.MediaPlayer("/home/pi/MS/music/angry/Disturbed - Land Of Confusion [Official Music Video].mp3")
        player.play()
        #Arduino.write(b'A')
        
    if state["Sad"] == 2 or (state["Sad"]==1 and state["Neutral"]==1 ):
        player = vlc.MediaPlayer("/home/pi/MS/music/sad/R I T U A L - Josephine.mp3.mp3")
        player.play()
        #Arduino.write(b'S')
    state = {"Happy": 0, "Neutral": 0,"Angry": 0, "Sad" : 0}
    
    return

if __name__ == '__main__':
    app.run(host='localhost', port = 5000, debug = True)

