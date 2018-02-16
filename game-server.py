import socket
import enchant #pip install pyenchant
import random
import string

UDP_SERVER_IP = #Enter IP Here
UDP_PORT = 12000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverSocket.bind((UDP_SERVER_IP, UDP_PORT))

spell_checker = enchant.Dict('en-US') #create enchant object to check if the words is real.

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
def startingRound (word, random):
    if (lastLetter(word) != random):
        playerState = 2
    elif (spell_checker.check(word) == False):
        playerState = 2
    else:
        playerState = 0

#This function is to check the integrity of the word sent by players after the 1st round.
def subsequentRound (word, prevword):
    if (lastLetter(word) != firstLetter(prevword)):
        playerState = 2
    elif (spell_checker.check(word) == False):
        playerState = 2
    else:
        playerState = 0

message = ''
message1 = ''
message2 = ''

turn = "0"
win = "1"
lose = "2"
begin = "3"

playerState = begin

gameState = 1

while True:

    randomLetter = random.choice(string.ascii_lowercase) #generates a new random lower case letter to start off the game.


    print ('Waiting for player 1...')
    player1, addr1 = serverSocket.recvfrom(2048)

    print('Player1 has entered the lobby \n'
        + 'Address:' + str(addr1))
    print('\n \nNow waiting for player 2...')
    player2, addr2 = serverSocket.recvfrom(2048)

    print('Player2 has entered the lobby \n'
        + 'Address: ' + str(addr2))
    
    message1 = 'Welcome! You are player 1'.encode()
    message2 = 'Welcome! You are player 2'.encode()

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
                + '\t 3) You do not enter a word within 5 seconds')
        
    rulesOfGame = rulesOfGame.encode()
    serverSocket.sendto(rulesOfGame, addr1)
    serverSocket.sendto(rulesOfGame, addr2)


    while (gameState == 1):
        
        print('Checking game state of Player 1...')
        serverSocket.sendto(playerState.encode(), addr1)

        if playerState == begin:
            serverSocket.sendto(randomLetter.encode(), addr1)
            word1, addr = serverSocket.recvfrom(2048)
            print(word1.decode())
        elif playerState != win or playerState != lose:
            word1, addr = serverSocket.recvfrom(2048)
        else:
            gameState = 0
            break

        

        #after player 1 sends back the word, this will have all the checking functions. 

        playerState = turn

        print('Checking game state of Player 2...')
        serverSocket.sendto(playerState.encode(), addr2)

        if playerState != win or playerState != lose:
            word2, addr = serverSocket.recvfrom(2048)
            print(word2.decode())
        else:
            gameState = 0

        #after player 2 sends back the word, this will have all the checking functions.

        playerState = win