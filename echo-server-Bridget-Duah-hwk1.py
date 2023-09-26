#!/usr/bin/env python3

import socket
from collections import defaultdict
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
storage = []
def run_server():
    print("server starting - listening for connections at IP", HOST, "and port", PORT)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"\nConnected established with {addr}")
            while True:
                data = conn.recv(1024)
                print(f"Received client message: '{data!r}' [{len(data)} bytes]")
                if not data:
                    break
                cmd, string = data.decode().strip().split(" ", 1)
                msg = ""
                if cmd == "add":
                    print("Trying to add " + string + " to storage")
                    res = handle_add(string)
                    msg = "You added " + string + " to your storage now you have " + str(res) + " item(s) in your storage"
                elif cmd == "delete":
                    print("Trying to delete " + string + " from storage")
                    try:
                        res = handle_deleted(string) 
                        msg = "You deleted " + string + " from your storage now you have " + str(res) + " item(s) in your storage"
                    except ValueError:
                        msg = "The string you entered doesn't exist in the storage :("
                else:
                    print("Trying to get the character that appears in very item storage")
                    res = handle_return_all()
                    msg = str(res) + " appear in every string your storage"
                print(f"\nechoing '{msg!r}' back to client")
                conn.sendall(msg.encode('utf-8'))

def handle_add(string):
    storage.append(string)
    return len(storage)

def handle_deleted(string):
    storage.remove(string)
    return len(storage)

def handle_return_all():
    result = []
    dict = defaultdict(set)
    for i in range(len(storage)):
        for chr in storage[i]:
                dict[chr].add(i)
    for key, val in dict.items():
        if len(val) == len(storage):
            result.append(key)          
    return result

if __name__ == "__main__":
    run_server()
    print("server is done! exiting ....")