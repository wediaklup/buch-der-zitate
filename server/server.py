import socket
import threading
from colorama import init, Fore as F, Style as S, Back as B
import os

SERVER = ''
PORT = 9807
FRMT = "utf-8"

init()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((SERVER, PORT))

new_quotes = []
print(f"{new_quotes = }")

with open("/root/qe-flask/new_quotes.dat", "r") as f:
    data = f.read()
    if len(data) > 0:
        restore = input("Because 'new_quotes.dat' wasn't empty, it's assumed that the server crashed.\nWould you like to restore the proposed entries? (Y/n)> ")
        data = eval(data)
        print(f"{data = }")

        if restore.upper() == "Y":
            for entry in data:
                new_quotes.append(entry)
            print(f"{new_quotes = }")


def append_data_file(dictionary : dict):
    list_of_lines = None
    to_add = dictionary
    dict_map = None
    app_lines = {}

    with open("/root/qe-flask/dicts.dat", "r") as f:
        list_of_lines = f.readlines()
        dict_map = list_of_lines[0]
        print(f"{dict_map = }")
        print(f"{list_of_lines = }")

    dict_map = eval(dict_map)

    for entry in to_add:
        line = dict_map[entry['name']]
        print(f"{line}")
        if len(entry['name_capt']) > 0 and len(entry['quote_capt']) > 0:
            app_lines[line] = f'''({entry['name_capt']}: "{entry['quote_capt']}")<br>"{entry['quote']}"'''
        else:
            app_lines[line] = f'''"{entry['quote']}"'''

# VERKNÜPF DAS SHUTDOWN ?A PROGRAMM MIT DEM STREAM DECK

    print(app_lines)

    for i in range(len(list_of_lines)):
        print(f"{F.BLACK}{B.WHITE} {i} {S.RESET_ALL} {list_of_lines[i]}")

    for n in app_lines:
        current_quotes = eval(list_of_lines[n])
        current_quotes.append(app_lines[n])
        list_of_lines[n] = f"{current_quotes}\n"

    with open("/root/qe-flask/dicts.dat", "w") as f:
        f.writelines(list_of_lines)

    print(f"{F.LIGHTGREEN_EX}Wrote {len(list_of_lines) + 1} lines{S.RESET_ALL}\n")


def handle_client(conn, addr):
    print(conn, addr)
    header = conn.recv(4).decode(FRMT)
    print(f"{header = }")
    global new_quotes

    if header == "NEW+":
        print(f"{header = }")
        received = eval(conn.recv(20480).decode(FRMT))
        print(f"{received = }")
        new_quotes.append(received)
        print(f"{new_quotes = }")

        with open("/root/qe-flask/new_quotes.dat", "w") as f:
            f.write(str(new_quotes))

        name = received['name']
        quote = received['quote']
        name_capt = received['name_capt']
        quote_capt = received['quote_capt']

        print("Added", name, quote, name_capt, quote_capt)
    elif header == "DUMP":
        conn.send(str(new_quotes).encode(FRMT))
    elif header == "APCL":
        print("APCL")
        apcl_recv = eval(conn.recv(20480).decode(FRMT))
        print(apcl_recv)
        append_data_file(apcl_recv)
        new_quotes = []
        
        with open("/root/qe-flask/new_quotes.dat", "w") as f:
                f.write("")
    elif header == "QLEN":
        conn.send(str(len(new_quotes)).encode(FRMT))

    conn.close()


s.listen()
print(f"STARTED")
while True:
    try:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"{threading.active_count() - 1} active connections")
    except KeyboardInterrupt:
        input()
        exit()
