import rsa
import main
import os
import socket

#-------------------------------------Not global functions-------------------------------------#

def add_user(name, password):
    pass

#-------------------------------------Main block-----------------------------------------------#


known_port = 50002

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 55555))

while True:
    clients = []
    pubkeys = []

    while True:
        data, address = sock.recvfrom(1024)
        pub_key = sock.recv(1024)

        print('connection from: {}'.format(address))
        clients.append(address)
        pubkeys.append(pub_key)

        sock.sendto(b'ready', address)

        if len(clients) == 2:
            print('got 2 clients, sending details to each')
            break

    c1 = clients.pop()
    c1_addr, c1_port = c1
    c1_pubkey = pubkeys.pop()
    c2 = clients.pop()
    c2_addr, c2_port = c2
    c2_pubkey = pubkeys.pop()


    sock.sendto('{} | {} | {} | {}'.format(c1_addr, c1_port, known_port, c1_pubkey).encode(), c2)
    sock.sendto('{} | {} | {} | {}'.format(c2_addr, c2_port, known_port, c2_pubkey).encode(), c1)
    