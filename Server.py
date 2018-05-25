from flask import Flask
from flask_ask import Ask, statement,question
from flask import request
from mutagen.mp3 import MP3

app = Flask(__name__)
ask = Ask(app, '/')


import serial
import time  
import vlc   

player = vlc.MediaPlayer()

counter = 0

#data strcuture that stores the informations that will be used to calculate the mood
state = {
  "Happy": 0, 
  "Neutral": 0,
  "Angry": 0, 
  "Sad" : 0
  }

#serial channel for the communication wih Arduino  
Arduino = serial.Serial("/dev/ttyACM0",9600)


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
    
    #check if another song is currently playing
    if player.is_playing():
        return statement("I am already playing a song, wait!")
    else:
        return question("Welcome! I can play a song for you based on your current mood. First of all, how are you?")

#handle the response for the four moods
@ask.intent('Happy')
def happy():
    global counter
    global state
    counter += 1
    #if we asked only the first question, counter==1 and we ask the second
    if counter == 1:
        state["Happy"]+= 1
        return question("And now, tell me, how was your day?")
    #else, calculate the mood with the chooseSong() function
    elif counter == 2:
        counter = 0
        state["Happy"]+= 1
        
        chooseSong()
        
        return statement("This is the song  I chose for you!")
        
        
        
#same as above, for every mood    
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
        
        return statement("This is the song  I chose for you!")

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
        
        return statement("This is the song  I chose for you!")

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
        return statement("This is the song  I chose for you!")
        
        
#calculate the mood, play the song and send a signal to Ardunino
def chooseSong():
    global ser
    global player 
    
    if state["Happy"] == 2 or ( state["Happy"] ==1 and state["Angry"]==1  ) or (state["Happy"] ==1 and state["Sad"]==1 ):
        player = vlc.MediaPlayer("/home/pi/Desktop/Happy/PharrellWilliams-Happy.mp3")
        player.play()
        Arduino.write(b'H')
  
    if state["Neutral"] == 2 or (state["Happy"] ==1 and state["Neutral"]==1  ):
        player = vlc.MediaPlayer("/home/pi/Desktop/Neutral/Riders_on_the_Storm.mp3")
        player.play()
        Arduino.write(b'N')
        
    #if Angry
    if state["Angry"] == 2 or (state["Angry"]==1 and state["Sad"]==1  ) or (state["Angry"]==1 and state["Neutral"]==1 ):
        player = vlc.MediaPlayer("/home/pi/Desktop/Angry/Enter_Sandman.mp3")
        player.play()
        Arduino.write(b'A')
        
    #if Sad
    if state["Sad"] == 2 or (state["Sad"]==1 and state["Neutral"]==1 ):
        player = vlc.MediaPlayer("/home/pi/Desktop/Sad/Wish_You_Were_Here.mp3")
        player.play()
        Arduino.write(b'S')
    state = {"Happy": 0, "Neutral": 0,"Angry": 0, "Sad" : 0}
    
    return;

#the server listens on localhost:5000
if __name__ == '__main__':
    app.run(host='localhost', port = 5000, debug = True)
