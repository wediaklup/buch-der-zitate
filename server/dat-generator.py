print("$exit um zu gehen, $break um zur nächsten person zu gehen, $capt um caption einzufügen")
name = ""
quot = ""

res = ""

while True:
    lst = []
    name = input("Name> ")
    if name.lower() == "$exit":
        break
    res += f"&{name.upper()}\n"
    while True:
        quot = input("Zitat> ")
        if quot.lower() == "$capt":
            capt_auth = input("[CAPTION] Wer?> ")
            capt_quot = input("[CAPTION] Was?> ")
            zitt = input("Zitat> ")
            lst.append(f'({capt_auth}: "{capt_quot}")<br>"{zitt}"')
            print(lst)
            continue
        elif quot.lower() == "$break":
            res += f"{str(lst)}\n"
            break
        else:
            lst.append(f'"{quot}"')
            print(lst)
            continue
        

print(f"\n=== FILE ===\n{res}")
input()
