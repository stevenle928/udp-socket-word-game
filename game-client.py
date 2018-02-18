#Team Members: Steven Le, John Lee
#Programming Language: Python 3.6.4
#To compile and run, we used Visual Studio Code with the Python plug-in installed and the extension Code-Runner to run it. Must have python installed beforehand.
#To compile and run, we used Visual Studio Code with the Python plug-in installed and the extension Code-Runner to run it. Must have python installed beforehand.
#In settings for Code-Runner Plug-in, must set 'run in terminal' setting to true to run in terminal of VSCode

#Author of this UDP game-client: Steven Le, John Lee

import socket 
import socketserver

#Used the wireless LAN ipv4 address of server's computer as the destination address
UDP_IP = '10.0.0.245'
UDP_PORT = 12000 #used the port # made by server side.
#message to send to server for initial request to play
mrequest = 'Request to play'
mrequest = mrequest.encode(encoding='utf-8',errors='strict')#convert to byte code.
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #creates a UDP socket
clientSocket.sendto(mrequest, (UDP_IP, UDP_PORT)) #sends message to server socket with destination ip adress and port# 12000

print('Waiting for another player to join...')
#creates a variable to receive the returning message with buffer size 2048 bytes
#Should receive the message: "Welcome! Your are Player 1"
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
message = modifiedMessage.decode()#decodes string from byte to string, should be "Welcome you are player [playerid]"
playerid = list(message)#turns message into a string array list
#takes last index object in string, which is a string number and casts to an integer value
#used to set client's playerid
playerid = int(playerid[len(playerid) - 1])
#client socket waits to receive rules from server, decodes to string, and prints it
rules, serverAddress = clientSocket.recvfrom(2048)
print (rules.decode())
print (message) #prints the new message, should be "Welcome you are player [playerid]"

#if playerid is 1
if playerid == 1:
    #receives initial state of game from server, should be '3' meaning game has begun
    state, serverAddress = clientSocket.recvfrom(2048)
    state = state.decode()
    #checks state and invokes while loop if state of the game has not been won or lost yet
    #'1' meaning won, '2' meaning lost
    while state != '1' or state != '2':
        print("\nWaiting...")
        #client/player waits to receive state of the game again.
        state, serverAddress = clientSocket.recvfrom(2048)
        state = state.decode()
        #if state is '0', meaning player's turn:
        #player receives the last word input
        #player inputs a word to assign to 'word' variable, encodes it into bytes also
        #client socket then sends word server
        if state == '0':
            prevword, serverAddress = clientSocket.recvfrom(1024)
            print ('Your turn!\nEnter a word: ' + prevword.decode())
            word = input().encode()
            clientSocket.sendto(word,(UDP_IP, UDP_PORT))
        #if state is '1', meaning player has won, prints Win message and breaks loop
        elif state == '1':
            print('You Win!')
            break
        #if state is '2', player has lost, client receives a message from server
        #message should contain the string of the reason why player has lost
        #reason is printed, then loop breaks.
        elif state == '2':
            print ('You Lose!')
            reason, serverAddress = clientSocket.recvfrom(2048)
            print(reason.decode())
            print ('You lost because: ' + reason.decode())
            break
        #if state is '3', meaning beginning of game for player1
        #client receives a random letter from server for player1 to start with and prints it
        #player inputs a word and assigns it to 'word' variable and encodes it into bytes
        #client socket sends word to server 
        elif state == '3':
            letter, serverAddress = clientSocket.recvfrom(1024)
            letter = letter.decode()
            print ('Your turn Player 1!\nEnter a word beginning with the random letter')
            print ('Your letter: ' + letter)
            word = input().encode()
            clientSocket.sendto(word,(UDP_IP,UDP_PORT))
    clientSocket.close() #closes socket after completion of message transfer(s)
#if playerid sent from server is 2
if playerid == 2:
    #checks state of game to see if it is continueing, been won, or been lost
    #'0' = turn, '1' = won, '2' = lost
    state, serverAddress = clientSocket.recvfrom(2048)
    state = state.decode()
    #while game has not been won or lost
    while state != '1' or state != '2':
        print("\nWaiting...")
        #client waits to receive state message from server again
        state, serverAddress = clientSocket.recvfrom(2048)
        state = state.decode()
        #if state is '0', game is continueing and player proceeds to input a word
        if state == '0':
            #client waits to receive previous word and prints it
            #player then inputs a word, then is assigned to 'word' variable and is encoded into bytes
            #client sends word to server.
            prevword, serverAddress = clientSocket.recvfrom(1024)
            print ('Your turn!\nEnter a word: ' + prevword.decode())
            word = input().encode()
            clientSocket.sendto(word,(UDP_IP, UDP_PORT))
        #if state is '1', player has won and prints message and breaks loop
        elif state == '1':
            print('You Win!')
            break
        #if state is '2', player has lost
        #client waits to receive message of string 'reason'
        #prints out reason why player lost then breaks loop
        elif state == '2':
            print ('You Lose!')
            reason, serverAddress = clientSocket.recvfrom(2048)
            print ('You lost because: ' + reason.decode())
            break
    clientSocket.close() #closes socket after completion of message transfer(s)
