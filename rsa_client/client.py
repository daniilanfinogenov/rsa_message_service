import sys
import socket
import sys
import threading
sys.path.insert(1, '../rsa_server/') #Select another path on device (~/rsa_service)
import main


#--------------You should install openssl for generate_openssl_keys function-------------#


try: 
    pubkey, privkey = main.load_keys() #Trying to get rsa_keys from /keys directory
except:
    main.generate_openssl_keys() #Faster then generate_keys() ,cause using openssl lib


#------------------------------------Main Part------------------------------------------#





rendezvous = ('192.168.31.199', 55555)

# connect to rendezvous
print('connecting to rendezvous server')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 50001))
sock.sendto(b'0', rendezvous)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('checked in with server, waiting')
        break

data = sock.recv(1024).decode()
ip, sport, dport = data.split(' ')
sport = int(sport)
dport = int(dport)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))
print('  dest port:   {}\n'.format(dport))

# punch hole
# equiv: echo 'punch hole' | nc -u -p 50001 x.x.x.x 50002
print('punching hole')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', sport))
sock.sendto(b'0', (ip, dport))

print('ready to exchange messages\n')

# listen for
# equiv: nc -u -l 50001
def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', sport))

    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n> '.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True);
listener.start()

# send messages
# equiv: echo 'xxx' | nc -u -p 50002 x.x.x.x 50001
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', dport))

while True:
    command = input("Enter your action: ")

    match command:
        case 'help':
            print("Command list: \nhelp- return all the commands \nexit - close the app \nencode - encode the text you have been written \ndecode - decode the bin you enter")
        case 'exit':
            print("Good bye")
            break
        case 'encode':
            message = input("Enter message: ")
            encmsg = main.encrypt(message ,pubkey)
            print(type(encmsg))
            with open('message.bin', 'wb') as bmessage:
                bmessage.write(encmsg)
            sock.sendto(encmsg.encode(), (ip, sport))
        case 'decode':
            file = input("Type place ...")
            with open(file, "rb") as file:
                file = file.read()
                decmsg = main.decrypt(file, privkey)
                print(decmsg)
    
    