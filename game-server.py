import socket
import enchant #pip install pyenchant

import random
import string

UDP_SERVER_IP = '10.0.0.245'
UDP_PORT = 12000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverSocket.bind((UDP_SERVER_IP, UDP_PORT))

wordCheck = enchant.Dict('en-US') #create enchant object to check if the words is real.



while True:

    randomLetter = random.choice(string.ascii_lowercase) #generates a new random lower case letter to start off the game.
    prevword = ''
    wordHistory = list()
    gameState = 1
    message = ''
    message1 = ''
    message2 = ''
    turn = '0'
    win = '1'
    lose = '2'
    begin = '3'
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

    #This function is to check the integrity of the first word sent by player 1.
    def matchRandom (word, random):
        if (firstLetter(word) != random):
            return False
        else:
            return True

    #This function is to check the integrity of the word sent by players after the 1st round.
    def matchLastLetter (word, prevword):
        if (firstLetter(word) != lastLetter(prevword)):
            return False
        else:
            return True

    def checkRepeat (word):
        global wordHistory
        for i in wordHistory:
            if word == i:
                return True

    #Checks to see if the word returned by the player is valid and follows the rules.
    def ruleCheck(word):
        global playerState
        global randomLetter
        global prevword
        global reason

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
    player1, addr1 = serverSocket.recvfrom(2048)

    print('Player1 has entered the lobby \n'
        + 'Address:' + str(addr1))
    print('\n \nNow waiting for player 2...')
    player2, addr2 = serverSocket.recvfrom(2048)

    print('Player2 has entered the lobby \n'
        + 'Address: ' + str(addr2))
    
    message1 = '\nWelcome! You are player 1'.encode()
    message2 = '\nWelcome! You are player 2'.encode()

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
        
    rulesOfGame = rulesOfGame.encode()
    serverSocket.sendto(rulesOfGame, addr1)
    serverSocket.sendto(rulesOfGame, addr2)

    serverSocket.sendto(playerState.encode(), addr1)
    serverSocket.sendto(playerState.encode(), addr2)


    while (gameState == 1):
        if(gameState != 0):
            print('Checking on Player 1...')
            serverSocket.sendto(playerState.encode(), addr1)

            if playerState == begin:
                serverSocket.sendto(randomLetter.encode(), addr1)
                word1, addr = serverSocket.recvfrom(2048)
                word1 = word1.decode()
                word1 = word1.lower()
                print('Word received from player1: ' + word1)
            elif playerState != win or playerState != lose:
                word1, addr = serverSocket.recvfrom(2048)
                word1 = word1.decode()
                word1 = word1.lower()
                print('Word received from player1: ' + word1)
            # else:
            #     gameState = 0
            #     print ("Game over! Player1 has won the game!")
            #     # break

        #after player 1 sends back the word, this will have all the checking functions.
            ruleCheck(word1)
        
            if(playerState == '2'):
                serverSocket.sendto(playerState.encode(), addr1)
                serverSocket.sendto(reason.encode(), addr1)
                playerState = '1'
                serverSocket.sendto(playerState.encode(), addr2)
                print("\nGame Over Player2 has won!")
                gameState = 0
            else:
                prevword = word1
                wordHistory.append(word1)
                print(wordHistory[len(wordHistory) - 1])
        

        
        if(gameState != 0):
            print('Checking on Player 2...')
            serverSocket.sendto(playerState.encode(), addr2)


            if playerState != win or playerState != lose:
                word2, addr = serverSocket.recvfrom(2048)
                word2 = word2.decode()
                word2 = word2.lower()
                print('Word received from player2: ' + word2)
            # else:
            #     gameState = 0
            #     print("Game over! Player2 has won the game!")
            #     # break

            #after player 2 sends back the word, this will have all the checking functions.
            ruleCheck(word2)

            if(playerState == '2'):
                serverSocket.sendto(playerState.encode(), addr2)
                serverSocket.sendto(reason.encode(), addr2)
                playerState = '1'
                serverSocket.sendto(playerState.encode(), addr1)
                print("\nGame Over! Player1 has won!")
                gameState = 0
            else:
                prevword = word2
                wordHistory.append(word2)
                print(wordHistory[len(wordHistory) - 1])