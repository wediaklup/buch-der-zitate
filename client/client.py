import socket
import os
from colorama import Style as S, Fore as F, Back as B, init
from time import sleep
from win10toast import ToastNotifier

toaster = ToastNotifier()
init()

SERVER = "wediaklup.de"
PORT = 9807
FRMT = "utf-8"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER, PORT))

s.send("DUMP".encode(FRMT))
new = eval(s.recv(20480).decode(FRMT))
s.close()
confirmed = []

color = None
if len(new) == 0:
    color = F.LIGHTGREEN_EX
else: 
    color = F.LIGHTYELLOW_EX


def format(dictionary : dict):
    res = ""
    name = dictionary['name']
    quote = dictionary['quote']
    name_capt = dictionary['name_capt']
    quote_capt = dictionary['quote_capt']

    if len(name_capt) > 0 and len(quote_capt) > 0:
        return f'({name_capt}: "{quote_capt}")\n{name}: "{quote}"'
    else:
        return f'{name}: "{quote}"'


def check(dictionary : dict):
    name = dictionary['name']
    quote = dictionary['quote']
    name_capt = dictionary['name_capt']
    quote_capt = dictionary['quote_capt']
    if len(name) > 0 and len(quote) > 0:
        return True
    elif len(name) > 0 and len(quote) > 0 and len(name_capt) > 0 and len(quote_capt) > 0:
        return True
    else:
        return False


def confirmall():
    print(f"{new = }")
    for entry in new:
        if check(entry):
            print(f"==================\n{format(entry)}")
            accept = input("Accept? (Y/n)> ")
            if accept.upper() == "Y":
                confirmed.append(entry)
                print("Confirmed!")
            elif accept.lower() == "n":
                edit = input("Edit? (Y/n)> ")
                if edit.upper() == "Y":
                    new_name = input("Name> ")
                    new_quote = input("Quote> ")
                    new_name_capt = input("Name (Capt)> ")
                    new_quote_capt = input("Quote (Capt)> ")

                    new_entry = {}
                    new_entry['name'] = new_name
                    new_entry['quote'] = new_quote
                    new_entry['name_capt'] = new_name_capt
                    new_entry['quote_capt'] = new_quote_capt

                    print(format(entry))
                    sure = input("Sure? (Y/n)> ")
                    if sure.upper() == "Y": 
                        confirmed.append(entry)
    print("==================")
    print(confirmed)


def apply(dictionary: dict):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER, PORT))

    print("APCL")
    s.send("APCL".encode(FRMT))
    sleep(1)
    s.send(str(dictionary).encode(FRMT))
    
    s.close()


print(f"{color}There are {len(new)} proposed entries.\nCheck? (Y/n){S.RESET_ALL}")
user = input("> ")
if user.upper() == "Y":
    confirmall()
    apply(confirmed)
    input("Press any key to exit ... ")
