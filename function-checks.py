#This file is used just to test out some functions.

import socket
import random
import enchant

checker = enchant.Dict('en-US') #create enchant object to check if the words is real.

playerState = '0'
randomLetter = 'e'
prevword = 'vape'

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
        return False
    elif (checker.check(word) == False):
        return False
    else:
        return True

#This function is to check the integrity of the word sent by players after the 1st round.
def subsequentRound (word, prevword):
    global playerState
    if (firstLetter(word) != lastLetter(prevword)):
        return False
    elif (checker.check(word) == False):
        return False
    else:
        return True

def ruleCheck(word):
    global playerState
    global randomLetter
    global prevword

    if playerState == '3' and (not startingRound(word, randomLetter)):
        playerState = '2'
    elif playerState == '0' and (not subsequentRound(word,prevword)):
        playerState = '2'
    else:
        playerState = '0'
    
    

# startingRound('alligator','b')

# print (playerState)

# subsequentRound('alligator', 'abra')

# print (playerState)

# ruleCheck('elf')
# print(playerState)

for x in 'hello':
    print (x)
