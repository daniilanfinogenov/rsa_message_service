import sys
import socket
import sys
import rsa
import threading
sys.path.insert(1, '../rsa_server/') #Select another path on device (~/rsa_service)
import main


#----------------------------------Global variables--------------------------------------#


HEADER = 64
PORT = 55555
FORMAT = 'utf-8'
KEY_FORMAT = "PEM"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.31.77"


#--------------You should install openssl for generate_openssl_keys function-------------#


try: 
    pubkey, privkey = main.load_keys() #Trying to get rsa_keys from /keys directory
except:
    main.generate_openssl_keys() #Faster then generate_keys() ,cause using openssl lib


#-------------------------------Not global functions------------------------------------#



#------------------------------------Main Part------------------------------------------#

rendezvous = (SERVER, PORT)

# connect to rendezvous
print('connecting to rendezvous server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50001))
sock.sendto(b'0', rendezvous)
sock.sendto(rsa.PublicKey.save_pkcs1(pubkey, format=KEY_FORMAT), rendezvous) 


while True:
    data = sock.recv(1024).decode(FORMAT)

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break


data = sock.recv(1024).decode(FORMAT)

print(data)
ip, sport, dport = data.split(' | ')
sport = int(sport)
dport = int(dport) 


print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}'.format(dport))



while True:
    pubkey = sock.recv(1024)

    try: 
        pubkey = rsa.PublicKey.load_pkcs1(pubkey, format=KEY_FORMAT)
        print('public key was found   \n')

        break
    except:
        pass

# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('\npunching hole    \n')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', sport))
sock.sendto(b'0', (ip, dport))


print('ready to exchange messages\n')

#closing the socket ,cause if I wouldn't it is gonna happen an error like: OSError: [Errno 98] Address already in use
sock.close()

# listen for
# equiv: nc -u -l 50001

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))

    while True:
        data = sock.recv(1024)
        
        try:
            decmsg = main.decrypt(data, privkey)
            print('\rpeer: {}\n> '.format(decmsg), end='')
        except: 
            print("couldn't decode text message")

        

listener = threading.Thread(target=listen, daemon=True)
listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))

active_threads_of_service = threading.active_count()

print(f'number of active threads: {active_threads_of_service}')

while True:

    if threading.active_count() < active_threads_of_service:
        listener = threading.Thread(target=listen, daemon=True)
        listener.start()

    msg = input('> ')
    encmsg = main.encrypt(msg ,pubkey)

    sock.sendto(encmsg, (ip, sport))
