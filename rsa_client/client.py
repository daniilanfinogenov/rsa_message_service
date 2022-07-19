import sys
sys.path.insert(1, '../rsa_server/') #Select another path on device (~/rsa_service)
import main


#--------------You should install openssl for generate_openssl_keys function-------------#


try: 
    pubkey, privkey = main.load_keys() #Trying to get rsa_keys from /keys directory
except:
    main.generate_openssl_keys() #Faster then generate_keys() ,cause using openssl lib


#------------------------------------Main Part------------------------------------------#

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
            print(str(encmsg))
        case 'decode':
            file = input("Type place ...")
            with open(file, "rb") as file:
                file = file.read()
                decmsg = main.decrypt(file, privkey)
                print(decmsg)


