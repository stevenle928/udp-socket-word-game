import socket

UDP_SERVER_IP = '192.168.1.30'
UDP_PORT = 12000

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverSocket.bind((UDP_SERVER_IP, UDP_PORT))

message = ''
message1 = ''
message2 = ''

turn = 0
win = 1
lose = 2
begin = 3

player1State = begin
player2State = begin


gameState = 1

while True:
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
        serverSocket.sendto()