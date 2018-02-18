#Team Members: Steven Le, John Lee
#Programming Language: Python 3.6.4
#To compile and run, we used Visual Studio Code with the Python plug-in installed and the extension Code-Runner to run it. Must have python installed beforehand.
#In settings for Code-Runner Plug-in, must set 'run in terminal' setting to true to run in terminal of VSCode

#Author of this UDP game-server: Steven Le, John Lee

import socket
import enchant #must install pyenchant first, done in terminal using 'pip install pyenchant' command
import random
import string

#Local server ipv4 address and port number
UDP_SERVER_IP = '10.0.0.245'
UDP_PORT = 12000
#creates a socket for the server.
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Binds server ip and port number to the server socket.
serverSocket.bind((UDP_SERVER_IP, UDP_PORT))
wordCheck = enchant.Dict('en-US') #create enchant object to check if the words is real.
while True:
    randomLetter = random.choice(string.ascii_lowercase) #generates a new random lower case letter to start off the game.
    prevword = '' #variable to hold the word that the previous player input
    wordHistory = list() #list to hold all words used
    gameState = 1 #variable to set game whileloop
    message = '' 
    message1 = ''
    message2 = ''
    turn = '0' #a playerState, used string '0' to let server and client know that the game is still going.
    win = '1' #a string to let client and server know if a player has won
    lose = '2' #a string value to let client and serer know if a player has won
    begin = '3' #a string value to signify round 1
    playerState = begin
    global reason 
    reason = ''
    notBegin ='Your word did not begin with the Random letter.'
    notRealWord ='You did not input an actual word.'
    notLast = 'Your word did not begin with the last letter of the previous word.'
    alreadyUsed = "Your word was already used."

    #This function is to extract the last letter of the word.
    def lastLetter(word):
        listToWord = list(word)
        last = (len(listToWord) - 1)
        return listToWord[last]
    #This function is to extract the first letter of the word.
    def firstLetter(word) :
        listToWord = list(word)
        return listToWord[0]
    #This function is to check if the first letter of the word input by player1, turn1, 
    # matches the random letter given by server..
    def matchRandom (word, random):
        if (firstLetter(word) != random):
            return False
        else:
            return True
    #This function checks if the first letter of the input word matches the last letter of the previous word.
    def matchLastLetter (word, prevword):
        if (firstLetter(word) != lastLetter(prevword)):
            return False
        else:
            return True
#A function that checks the wordHistory list that contains all words used to check if the input word is a repeat.
    def checkRepeat (word):
        global wordHistory
        for i in wordHistory:
            if word == i:
                return True
    #Checks to see if the word returned by the player is valid and follows the rules of the game.
    def ruleCheck(word):
        #global variables 
        global playerState
        global randomLetter
        global prevword
        global reason
        #checks if word input follows rules for turn1, subsequent turns, and if word is a real word
        if playerState == '3' and (not matchRandom(word, randomLetter) or not wordCheck.check(word) ):
            playerState = '2'
            if not matchRandom(word, randomLetter):
                reason = notBegin
            else:
                reason = notRealWord
        elif playerState == '0' and (not matchLastLetter(word,prevword) or checkRepeat(word) or not wordCheck.check(word)):
            playerState = '2'
            if not matchLastLetter(word, prevword):
                reason = notLast
            elif not (wordCheck.check(word)):
                reason = notRealWord
            else:
                reason = alreadyUsed
        else:
            playerState = '0'

    print ('\nWaiting for player 1...')
    #waiting to receive a message from player1
    player1, addr1 = serverSocket.recvfrom(2048)
    #prints the "connecting" player's address and port)
    print('Player1 has entered the lobby \n'
        + 'Address:' + str(addr1))
    print('\n \nNow waiting for player 2...')
    player2, addr2 = serverSocket.recvfrom(2048)

    print('Player2 has entered the lobby \n'
        + 'Address: ' + str(addr2))
    
    message1 = '\nWelcome! You are player 1'.encode()
    message2 = '\nWelcome! You are player 2'.encode()
    #sends players their respective message, message1 to player1 and message2 to player2
    serverSocket.sendto(message1, addr1)
    serverSocket.sendto(message2, addr2)
    print('\nLet\'s begin the game!')
    rulesOfGame = ('\nRules of the game: \n'
                + '-Player 1 must input a word beginning with a randomly generated\n'
                + 'letter at the start of the game for only the first turn\n'
                + '-Player 2 must then respond with a word beginning with the last\n'
                + 'letter of player 1\'s word and the game will continue as such\n'
                + 'for each player until one loses\n'
                + '-You will lose if:\n'
                + '\t 1) The word entered is not a real word\n'
                + '\t 2) The word entered does not begin with the last letter of\n'
                + '\t    the previous word (but on turn 1, player 1\'s word must)\n'
                + '\t    start with the randomly generated letter\n'
                + '\t 3) Your word cannot be a repeat of the previous word.'
                + '\t 4) You do not enter a word within 5 seconds')
    #encodes rulesOfGame string to byte to send to players
    rulesOfGame = rulesOfGame.encode()
    serverSocket.sendto(rulesOfGame, addr1)
    serverSocket.sendto(rulesOfGame, addr2)
    #Send the initial playerState to each player.
    serverSocket.sendto(playerState.encode(), addr1)
    serverSocket.sendto(playerState.encode(), addr2)

    #gameState set to 1 to start the game
    while (gameState == 1):
        if(gameState != 0):
            print('Checking on Player 1...')
            #sends playerState value to client to notify if game is still continueing
            serverSocket.sendto(playerState.encode(), addr1)
            if playerState == begin:
                #sends randomly generated letter to player1 to start turn1, 
                #server waits to receive message back from player1
                # prints the word input by player
                serverSocket.sendto(randomLetter.encode(), addr1)
                word1, addr = serverSocket.recvfrom(2048)
                word1 = word1.decode()
                word1 = word1.lower()
                print('Word received from player1: ' + word1)
            #if not turn1 or player2 has not won yet
            elif playerState != win or playerState != lose:
                #Sends player the previous word
                serverSocket.sendto(prevword.encode(), addr1)
                word1, addr = serverSocket.recvfrom(2048)
                word1 = word1.decode()
                word1 = word1.lower()
                print('Word received from player1: ' + word1)
            #after player 1 sends back the word, this will have all the checking functions.
            ruleCheck(word1)
            #if word violates rules, sends the violating player the 'loss' playerState value,
            #sends violating player 'reason' string to tell why they lost
            #sets playerState to '1', meaning win, to send to the other player.
            #releases memory of wordHistory list
            if(playerState == '2'):
                serverSocket.sendto(playerState.encode(), addr1)
                serverSocket.sendto(reason.encode(), addr1)
                playerState = '1'
                serverSocket.sendto(playerState.encode(), addr2)
                print("\nGame Over Player2 has won!")
                gameState = 0
                del wordHistory
            #if no rules are violated by input word,
            #saves input word into prevword variable for next player
            #adds input word into wordHistory List
            else:
                prevword = word1
                wordHistory.append(word1)
                print(wordHistory[len(wordHistory) - 1])
        #start of player2's turn
        if(gameState != 0):
            print('Checking on Player 2...')
            #sends status of game to player2, if it's still continueing
            serverSocket.sendto(playerState.encode(), addr2)
            #if game has not been won or lost yet,
            #sends previous word to player2
            #server waits to receive a word input back from player2
            #prints the word input by player2
            if playerState != win or playerState != lose:
                serverSocket.sendto(prevword.encode(), addr2)
                word2, addr = serverSocket.recvfrom(2048)
                word2 = word2.decode()
                word2 = word2.lower()
                print('Word received from player2: ' + word2)
            #after player 2 sends back the word, this will check if the word violates any game rules.
            ruleCheck(word2)
            #if word violates rules, sends the violating player the 'loss' playerState value,
            #sends violating player 'reason' string to tell why they lost
            #sets playerState to '1', meaning win, to send to the other player.
            #releases memory of wordHistory list
            if(playerState == '2'):
                serverSocket.sendto(playerState.encode(), addr2)
                serverSocket.sendto(reason.encode(), addr2)
                playerState = '1'
                serverSocket.sendto(playerState.encode(), addr1)
                print("\nGame Over! Player1 has won!")
                gameState = 0
                del wordHistory
            #if no rules are violated by input word,
            #saves input word into prevword variable for next player
            #adds input word into wordHistory List 
            else:
                prevword = word2
                wordHistory.append(word2)
                print(wordHistory[len(wordHistory) - 1])