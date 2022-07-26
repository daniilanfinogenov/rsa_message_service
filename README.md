# RSA message service

This service will provide users to exchange their message without a server.

This application uses hybrid connection ,you connect to the server to get information about users online from it and then you are going to connect to user directly instead of using client-server data transfering. Hybrid connection was made to make it difficult for third parties to obtain your data.

Also all the messages will be encrypted by using rsa method of encryption, so everyfing you send will be decrypted only by the second client.


client.py - client part of this service, you should change SERVER variable to your server if you want to use your own server or use standart to see other clients.

message_server.py - server part of this service, you should run it on your server to made it a node in the service servers (this function will be added in a future) or make it your own server


My tasks now:

* [ ] Fix some throubles with clients interaction
* [ ] Change client-server innteraction
* [ ] Add user interface for a client part of it
* [ ] Add user authentication to get information from the server



If you want to participate in its development you can text me here:

Telegram: @abby_raymond

Gmail: daniilanfinogenov@gmail.com
