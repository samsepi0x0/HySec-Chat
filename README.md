#Python app to communicate securely over a public network
It is a simple app to send messages over a public network while encrypting it with two different algorithms and packaging the keys through RSA.

For development python version 3.8.3 has been used. The server and the client generate public and private keys at runtime and exchange them. Then the server uses the client public key to encrypt a random generated session key and it will be shared with the client. After this process the client will decrypt it with its own private key and uses that secret to encrypt/decrypt messages using AES and DES in CFB mode. The server can handle multiple clients and cannot log/see messages.

Usage:
The server can be started using one parameter which should be the port number on which the server will listen
- python3 server.py -p 9999

The client has three parameters, -s server ip, -p server port number, -u username of the user
- python3 client.py -s 0.0.0.0 -p 9999 -u Hemant

The server can be terminated by typing 'TERMINATE' on the console.
The client can be terminated by typing 'EXIT' on the console.
