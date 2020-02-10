
Nicholas Koran
6:50 PM (0 minutes ago)
to me

def encode(text, music):
    music = music[:26]

    code = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    code = list(code)
    alpha='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    for i in range(25):
        dif = (abs(music[i] - music[i+1])) % 26
        temp1 = code[i]
        temp2 = code[dif]
        code[i] = temp2
        code[dif] = temp1
    "".join(code)

    mapping = {}
    key = {}
    for i in range(26):
        mapping[alpha[i]] = code[i]

    for i in range(26):
        key[code[i]] = alpha[i]

    text=text.upper()
    text = list(text)

    for i in range(len(text)):
        text[i] = mapping[text[i]]
    "".join(text)

    return  text
