import pyperclip, re, json

def convert():
    s = input("Enter json:\n")
    istr = s[:]
    if istr[0] == "\"":
        istr = istr[1:]
    if istr[-1] == "\"":
        istr = istr[:-1]
    istr = istr.replace("\\", "")
    istr = re.sub(r"""(", '\d' <repeats .{12})+""", "", istr)
    obj = json.loads(istr)
    res = json.dumps(obj, indent=2)
    pyperclip.copy(res)
    print("Final JSON : \n",res)
    print("JSON COPIED TO CLIPBOARD!\n")

while(True):
    try:
        convert()
    except KeyboardInterrupt:
        print("EXITED.")
        break
    except:
        print("JSON INCORRECT!!! TRY AGAIN...")
        convert()
    
    