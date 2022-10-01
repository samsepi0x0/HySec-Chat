# HySec Chat
This is a simple broadcast server which encrypts chats with AES encryption.

## Description:
This project is a demonstration of a simple chat server with broadcast feature implemented with python. What makes this repo different is the use of encryption algorithms like AES and RSA to secure the communication over insecure channel. Firstly, RSA keys are generated for server and each client. As soon as the client joins the server, the public keys are exchanged. Once the keys are exchanged, AES keys are generated for the client along with IV and encrypted messages are sent to the server for broadcast. The plain text in encrypted with AES, while the AES keys are encrypted with the RSA encryption standard.

## Requirements:
The code requires Python 3.x+ installed on the system with following libraries:
```
pycryptodomex
termcolor
json
argparse
base64
hashlib
```

## Usage:
Clone the repo on the local system by downloading the main branch as ZIP or using cli.
```bash
$> git clone https://github.com/heven07/HySec-Chat.git
$> cd HySec-Chat
```
After cloning, install the requirements using pip.
```bash
$> pip install -r requirements.txt
```

To start the server, run the following command specifying the port number.
```bash
$> python3 server.py -p <PORT_NUMBER>
```

Client can be connected to server using the following command with previous port number.
```bash
$> python3 client.py -s 127.0.0.1 -p <PORT_NUMBER> -u <USERNAME>
```

The server can be terminated by typing `TERMINATE` on the console.

The client can be terminated by typing `EXIT` on the console.
