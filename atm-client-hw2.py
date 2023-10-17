#!/usr/bin/env python3
#
# Automated Teller Machine (ATM) client application.

import socket

HOST = "127.0.0.1"      # The bank server's IP address
PORT = 65432            # The port used by the bank server

##########################################################
#                                                        #
# ATM Client Network Operations                          #
#                                                        #
# NEEDS REVIEW. Changes may be needed in this section.   #
#                                                        #
##########################################################

def send_to_server(sock, msg):
    """ Given an open socket connection (sock) and a string msg, send the string to the server. """
    # TODO make sure this works as needed
    return sock.sendall(msg.encode('utf-8'))

def get_from_server(sock):
    """ Attempt to receive a message from the active connection. Block until message is received. """
    # TODO make sure this works as needed
    msg = sock.recv(1024)
    return msg.decode('utf-8')

def login_to_server(sock, acct_num, pin):
    """ Attempt to login to the bank server. Pass acct_num and pin, get response, parse and check whether login was successful. """
    # TODO: Write this code!
    request = f"LOGIN {acct_num} {pin}"
    send_to_server(sock, request)
    print("sent your log in info to the server")
    # Receive and check the response
    response = get_from_server(sock)
    validated = 0
    if response == "0":
        validated = 1
    else:
        if response == "1":
            print("The account number or pin doesn't have the right format")
        elif response == "2":
            print("The account number you entered does not exist")
        elif response == "3":
            print("You entered the wrong pin")
        elif response == "4":
            print("Account already logged in :(")
    return validated

def get_login_info():
    """ Get info from customer. TODO: Validate inputs, ask again if given invalid input. """
    acct_num = input("Please enter your account number: ")
    pin = input("Please enter your four digit PIN: ")
    return acct_num, pin

def process_deposit(sock, acct_num):
    """ TODO: Write this code. """
    bal = get_acct_balance(sock, acct_num)
    amt = input(f"How much would you like to deposit? (You have ${bal} available)")
    # TODO communicate with the server to request the deposit, check response for success or failure.
    request = f"DEPOSIT {acct_num} {amt}"
    send_to_server(sock, request)
    response = get_from_server(sock).split(" ")
    code, new_bal = response[0], response[1]
    if code == "0":
        print("Deposit transaction completed.")
        print(f"Your new balance is {new_bal}")
    else:
        print("Invalid Amount Given")
    return 

def get_acct_balance(sock, acct_num):
    """ TODO: Ask the server for current account balance. """
    bal = 0.0
    # TODO code needed here, to get balance from server then return it
    request = f"GETBALANCE {acct_num}"
    send_to_server(sock, request)
    # Receive and check the response
    bal = float(get_from_server(sock))
    return bal

def process_withdrawal(sock, acct_num):
    """ TODO: Write this code. """
    bal = get_acct_balance(sock, acct_num)
    amt = input(f"How much would you like to withdraw? (You have ${bal} available)")
    # TODO communicate with the server to request the withdrawal, check response for success or failure.
    request = f"WITHDRAW {acct_num} {amt}"
    send_to_server(sock, request)
    response = get_from_server(sock).split(" ")
    code, new_bal = response[0], response[1]
    if code == "0":
        print("Withdrawal transaction completed.")
        print(f"Your new balance is {new_bal}")
    elif code == "1":
        print("Invalid Amount Given")
    else:
        print("Attempted Overdraft")
    return

def process_customer_transactions(sock, acct_num):
    """ Ask customer for a transaction, communicate with server. TODO: Revise as needed. """
    while True:
        print("Select a transaction. Enter 'd' to deposit, 'w' to withdraw, or 'x' to exit.")
        req = input("Your choice? ").lower()
        if req not in ('d', 'w', 'x'):
            print("Unrecognized choice, please try again.")
            continue
        if req == 'x':
            # if customer wants to exit, break out of the loop
            break
        elif req == 'd':
            process_deposit(sock, acct_num)
        else:
            process_withdrawal(sock, acct_num)

def run_atm_core_loop(sock):
    """ Given an active network connection to the bank server, run the core business loop. """
    acct_num, pin = get_login_info()
    validated = login_to_server(sock, acct_num, pin)
    if validated:
        print("Thank you, your credentials have been validated.")
    else:
        print("Account number and PIN do not match. Terminating ATM session.")
        return False
    process_customer_transactions(sock, acct_num)
    print("ATM session terminating.")
    return True

##########################################################
#                                                        #
# ATM Client Startup Operations                          #
#                                                        #
# No changes needed in this section.                     #
#                                                        #
##########################################################

def run_network_client():
    """ This function connects the client to the server and runs the main loop. """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            run_atm_core_loop(s)
    except Exception as e:
        print(f"Unable to connect to the banking server - exiting...")

if __name__ == "__main__":
    print("Welcome to the ACME ATM Client, where customer satisfaction is our goal!")
    run_network_client()
    print("Thanks for banking with us! Come again soon!!")