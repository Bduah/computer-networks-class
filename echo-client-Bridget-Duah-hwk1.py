#!/usr/bin/env python3
# echo-client
# Author - Bridget Duah
# In this file, the user chooses a command they want processed
# There will be 3 commands
# 1. Add - The user can add a new string to the storage
# 2. Delete - The user can delete a string from the storage 
# 3. Char in all - The user can return the character that appears in every string in the storage

import socket

HOST = "127.0.0.1"  # This is the loopback address
PORT = 65432        # The port used by the server

def run_client():
    print("client starting - connecting to server at IP", HOST, "and port", PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print(f"connection established")
        while True:
            # loop until the user asks to quit
            if not talk_to_server(s):
                break

def talk_to_server(sock):
    cmd = ""
    msg = ""
    string = ""
    
    while True:
        cmd = input("\nWhat command do you want processed?\n"
                    "Enter 1 to add\n"
                    "Enter 2 to delete\n"
                    "Enter 3 to return the char that appears in all the stored strings:\n"
                    "Enter 'quit' to exit: ")
        
        if cmd == 'quit':
            print("Client quitting at operator request.")
            return False
        
        if cmd in ["1", "2", "3"]:
            break
        else:
            print("\nINVALID INPUT, choose a command again or enter 'quit' to end.")
    
    if cmd == "1":
        string = input("\nEnter the String you want to add:\n")
        msg = "add " + string
    elif cmd == "2":
        string = input("\nEnter the string you want to delete:\n")
        msg = "delete " + string
    elif cmd == "3":
        msg = "returnAll Nothing"

    print(f"sending message '{msg}' to server")
    sock.sendall(msg.encode('utf-8'))
    print("message sent, waiting for reply")
    reply = sock.recv(1024)
    if not reply:
        return False
    else:
        print(f"received reply '{reply}' from server")
        return reply

if __name__ == "__main__":
    run_client()
    print("Client is done, exiting...")