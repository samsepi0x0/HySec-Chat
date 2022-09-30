import os, random, string, datetime
import json, socket, threading, argparse

from termcolor import colored
from Crypto.Cipher import AES
from Crypto.Cipher import DES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode
from Crypto.Random import get_random_bytes

class Client:
    def __init__(self, server, port, username):
        self.server = server
        self.port = port
        self.username = username
        
    def create_connection(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.s.connect((self.server, self.port))
        except:
            print(colored("""
█▀ █▀▀ █▀█ █░█ █▀▀ █▀█   █ █▀   █▄░█ █▀█ ▀█▀   █▀█ █░█ █▄░█ █▄░█ █ █▄░█ █▀▀
▄█ ██▄ █▀▄ ▀▄▀ ██▄ █▀▄   █ ▄█   █░▀█ █▄█ ░█░   █▀▄ █▄█ █░▀█ █░▀█ █ █░▀█ █▄█""",'red'))
        self.s.send(self.username.encode())
        print(colored('[+] Connected successfully', 'yellow'))
        print(colored('[+] Exchanging keys', 'yellow'))
        
        self.create_key_pairs()
        self.exchange_public_keys()
        global secret_key
        secret_key = self.handle_secret()
        print(colored('[+] Initial set up had been completed!\n \n', 'yellow'))
        print("\n" *55)
        print(colored("""
░░░░░░  ░░░░░░ ░░░░░░░░  ░░░░░░░░ ░░░░░░░░░░░░░░ ░░░░░░░░░░░░░░ ░░░░░░░░░░░░░░    ░░░░░░░░░░░░░░ ░░░░░░  ░░░░░░ ░░░░░░░░░░░░░░ ░░░░░░░░░░░░░░     ▄▄▀▀▀▀▀▀▀▀▀▄▄  
░░██░░  ░░██░░ ░░████░░  ░░████░░ ░░██████████░░ ░░██████████░░ ░░██████████░░    ░░██████████░░ ░░██░░  ░░██░░ ░░██████████░░ ░░██████████░░    █             █ 
░░██░░  ░░██░░ ░░░░██░░  ░░██░░░░ ░░██░░░░░░░░░░ ░░██░░░░░░░░░░ ░░██░░░░░░░░░░    ░░██░░░░░░░░░░ ░░██░░  ░░██░░ ░░██░░░░░░██░░ ░░░░░░██░░░░░░   █          ▄▄▄  █ 
░░██░░  ░░██░░   ░░████░░████░░   ░░██░░         ░░██░░         ░░██░░            ░░██░░         ░░██░░  ░░██░░ ░░██░░  ░░██░░     ░░██░░       █  ▄▄▄  ▄  ███  █  
░░██░░░░░░██░░   ░░░░██████░░░░   ░░██░░░░░░░░░░ ░░██░░░░░░░░░░ ░░██░░            ░░██░░         ░░██░░░░░░██░░ ░░██░░░░░░██░░     ░░██░░       ▄█ ▄   ▀▀▀   ▄ █▄  
░░██████████░░     ░░░░██░░░░     ░░██████████░░ ░░██████████░░ ░░██░░            ░░██░░         ░░██████████░░ ░░██████████░░     ░░██░░       █  ▀█▀█▀█▀█▀█▀  █  
░░██░░░░░░██░░       ░░██░░       ░░░░░░░░░░██░░ ░░██░░░░░░░░░░ ░░██░░            ░░██░░         ░░██░░░░░░██░░ ░░██░░░░░░██░░     ░░██░░       ▄██▄▄▀▀▀▀▀▀▀▄▄██▄
░░██░░  ░░██░░       ░░██░░               ░░██░░ ░░██░░         ░░██░░            ░░██░░         ░░██░░  ░░██░░ ░░██░░  ░░██░░     ░░██░░     ▄█ █▀▀█▀▀▀█▀▀▀█▀▀█ █▄
░░██░░  ░░██░░       ░░██░░       ░░░░░░░░░░██░░ ░░██░░░░░░░░░░ ░░██░░░░░░░░░░    ░░██░░░░░░░░░░ ░░██░░  ░░██░░ ░░██░░  ░░██░░     ░░██░░    ▄▀ ▄▄▀▄▄▀▀▀▄▀▀▀▄▄▀▄▄ ▀▄
░░██░░  ░░██░░       ░░██░░       ░░██████████░░ ░░██████████░░ ░░██████████░░    ░░██████████░░ ░░██░░  ░░██░░ ░░██░░  ░░██░░     ░░██░░    █    ▀▄ █▄   ▄█ ▄▀    █
░░░░░░  ░░░░░░       ░░░░░░       ░░░░░░░░░░░░░░ ░░░░░░░░░░░░░░ ░░░░░░░░░░░░░░    ░░░░░░░░░░░░░░ ░░░░░░  ░░░░░░ ░░░░░░  ░░░░░░     ░░░░░░     ▀▄▄ █  █▄▄▄▄▄█  █ ▄▄▀ 
																		▀██▄▄███████▄▄██▀     """,'magenta'))
        print(colored("""
█▄█ █▀█ █░█   █▀▀ ▄▀█ █▄░█   █▀ ▀█▀ ▄▀█ █▀█ ▀█▀   █▀▄▀█ █▀▀ █▀ █▀ ▄▀█ █▀▀ █ █▄░█ █▀▀   █▄░█ █▀█ █░█░█
 █░ █▄█ █▄█   █▄▄ █▀█ █░▀█   ▄█ ░█░ █▀█ █▀▄ ░█░   █░▀░█ ██▄ ▄█ ▄█ █▀█ █▄█ █ █░▀█ █▄█   █░▀█ █▄█ ▀▄▀▄▀""", 'cyan'))
        print(colored("\n","green","on_cyan"))
        message_handler = threading.Thread(target=self.handle_messages,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.input_handler,args=())
        input_handler.start()
        
    def handle_messages(self):
        while True:
            message = self.s.recv(1024).decode()
            if message:
                key = secret_key                                        
                decrypt_message = json.loads(message)                   
                iv = b64decode(decrypt_message['iv'])                   
                cipherText = b64decode(decrypt_message['ciphertext'])   
                cipher = AES.new(key, AES.MODE_CFB, iv=iv)              
                msg = cipher.decrypt(cipherText)                        
                current_time = datetime.datetime.now()
                print(colored(msg.decode()+current_time.strftime('\n%Y-%m-%d %H:%M:%S\n'), 'green'))
            else:
                print("\n" *39)
                print(colored("""
█▀▀ █▀█ █▄░█ █▄░█ █▀▀ █▀▀ ▀█▀ █ █▀█ █▄░█   █░░ █▀█ █▀ ▀█▀
█▄▄ █▄█ █░▀█ █░▀█ ██▄ █▄▄ ░█░ █ █▄█ █░▀█   █▄▄ █▄█ ▄█ ░█░""", 'red'))
                print(colored("\n","green","on_red"))
                self.s.shutdown(socket.SHUT_RDWR)
                os._exit(0)
                
    def input_handler(self):
        while True:
            message = input("\n")               
            if message == "EXIT" or message == "exit":
                print("\n" *39)           
                print(colored("""
█▀▀ ▀▄▀ █ ▀█▀ █ █▄░█ █▀▀
██▄ █░█ █ ░█░ █ █░▀█ █▄█""", 'red'))
                print(colored("\n","green","on_red"))
                break
            else:
                key = secret_key
                cipher = AES.new(key, AES.MODE_CFB)
                message_to_encrypt = self.username + ": \n" + message           
                msgBytes = message_to_encrypt.encode()                          
                encrypted_message = cipher.encrypt(msgBytes)                    
                iv = b64encode(cipher.iv).decode('utf-8')                       
                message = b64encode(encrypted_message).decode('utf-8')          
                result = json.dumps({'iv':iv, 'ciphertext':message})            
                self.s.send(result.encode())                                    
        
        self.s.shutdown(socket.SHUT_RDWR)
        os._exit(0)
        
    def handle_secret(self):
            secret_key = self.s.recv(1024)
            private_key = RSA.importKey(open('client_private_key.key', 'r').read())
            cipher = PKCS1_OAEP.new(private_key)
            return cipher.decrypt(secret_key)
            
    def exchange_public_keys(self):
        try:
            print(colored('[+] Getting public key from the server', 'blue'))
            server_public_key = self.s.recv(1024).decode()
            server_public_key = RSA.importKey(server_public_key)    

            print(colored('[+] Sending public key to server', 'blue'))
            public_pem_key = RSA.importKey(open('client_public_key.key', 'r').read())
            self.s.send(public_pem_key.exportKey())
            print(colored('[+] Exchange completed!', 'yellow'))
        except Exception as e:
            print(colored('[!] ERROR, you messed up something.... '+e, 'red'))
            
    def create_key_pairs(self):
        try:    
            private_key = RSA.generate(2048)
            public_key = private_key.publickey()
            private_pem = private_key.exportKey().decode()
            public_pem = public_key.exportKey().decode()
            with open('client_private_key.key', 'w') as priv:
                priv.write(private_pem)
            with open('client_public_key.key', 'w') as pub:
                pub.write(public_pem)
        except Exception as e:
            print(colored('[!] ERROR, you messed up something.... '+e, 'red'))
if __name__ == "__main__":
    arg_parse = argparse.ArgumentParser()
    arg_parse.add_argument('-s', '--server', required=True, help="server ip to connect")
    arg_parse.add_argument('-p', '--port', required=True, type=int, help="port the server listening on")
    arg_parse.add_argument('-u', '--username', required=True, help="username of the user")
    args = arg_parse.parse_args()
    client = Client(args.server, args.port, args.username)
    try:	
    	client.create_connection()
    except:
    	pass
