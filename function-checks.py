
import socket
import random
import enchant

spell_checker = enchant.Dict('en-US') #create enchant object to check if the words is real.

playerState = 3

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
    global playerState

    if (firstLetter(word) != random):
        playerState = 2
    elif (spell_checker.check(word) == False):
        playerState = 2
    else:
        playerState = 0

#This function is to check the integrity of the word sent by players after the 1st round.
def subsequentRound (word, prevword):
    global playerState
    if (lastLetter(word) != firstLetter(prevword)):
        playerState = 2
    elif (spell_checker.check(word) == False):
        playerState = 2
    else:
        playerState = 0

startingRound('alligator','a')

print (playerState)