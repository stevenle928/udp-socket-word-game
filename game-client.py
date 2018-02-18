#Team Members: Steven Le, John Lee
#Programming Language: Python 3.6.4
#To compile and run, we used Visual Studio Code with the Python plug-in installed and the extension Code-Runner to run it. Must have python installed beforehand.

#Author of this UDP_Client: Steven Le



import socket 
import socketserver

#Used the wireless LAN ipv4 address of server's computer as the destination address
UDP_IP = '10.0.0.245'
UDP_PORT = 12000 #used the port # made by server side.


mrequest = 'Request to play'
mrequest = mrequest.encode(encoding='utf-8',errors='strict')#convert to byte code.
# addr = (UDP_IP, UDP_PORT)

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #creates a UDP socket
clientSocket.sendto(mrequest, (UDP_IP, UDP_PORT)) #sends message to server socket with destination "192.168.1.13" adress and port# 12000

print('Waiting for another player to join...')

modifiedMessage, serverAddress = clientSocket.recvfrom(2048)#creates a variable to receive the returning message with buffer size 2048 bytes
message = modifiedMessage.decode()
playerid = list(message)
playerid = int(playerid[len(playerid) - 1])

# if(type(message) is str):
#     print('true')

print (message) #prints the new message, should be "Welcome you are player [playerid]"
rules, serverAddress = clientSocket.recvfrom(2048)
print (rules.decode())


if playerid == 1:
    state, serverAddress = clientSocket.recvfrom(2048)
    state = state.decode()
    while state != '1' or state != '2':
        print("\nWaiting...")
        state, serverAddress = clientSocket.recvfrom(2048)
        state = state.decode()
        playerState = state

        if state == '0':
            print ('Your turn!\nEnter a word')
            word = input().encode()
            clientSocket.sendto(word,(UDP_IP, UDP_PORT))

        elif state == '1':
            print('You Win!')
            break

        elif state == '2':
            print ('You Lose!')
            break
            #reason, serverAddress = clientSocket.recvfrom(2048)
            #print ('You lost because: ' + reason.decode())
        elif state == '3':
            letter, serverAddress = clientSocket.recvfrom(1024)
            letter = letter.decode()
            print ('Your turn Player 1!\nEnter a word beginning with the random letter')
            print ('Your letter: ' + letter)
            word = input().encode()
            clientSocket.sendto(word,(UDP_IP,UDP_PORT))

    clientSocket.close() #closes socket after completion of message transfer

if playerid == 2:
    state, serverAddress = clientSocket.recvfrom(2048)
    state = state.decode()
    while state != '1' or state != '2':

        print("\nWaiting...")
        state, serverAddress = clientSocket.recvfrom(2048)
        state = state.decode()
        
        if state == '0':
            print ('Your turn!\nEnter a word')
            word = input().encode()
            clientSocket.sendto(word,(UDP_IP, UDP_PORT))

        elif state == '1':
            print('You Win!')
            break
        elif state == '2':
            print ('You Lose!')
            break
            #reason, serverAddress = clientSocket.recvfrom(2048)
            #print ('You lost because: ' + reason.decode())


    clientSocket.close() #closes socket after completion of message transfer
