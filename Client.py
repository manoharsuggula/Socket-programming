import socket
import threading
import time
import sys

host = '127.0.0.1'
port = 65432

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.settimeout(0.1)
inp = None
rec = None
flag = 0

def user():
    global inp
    inp = input()
Questions = [
    "What is biggest planet in the Universe : \n a.Saturn  b.Uranus  c.JupTimeer  d.Earth",
    "Who discovered Radio : \n a.Marconi  b.J.L.Baird  c.Newton  d.Einstein",
    "Which is most populated Country : \n a.China  b.India  c.Russia  d.USA",
    "Which is the biggest country in terms of Land : \n a.Russia  b.China  c.USA  d.BrTimeain",
    "Water boils at 212 UnTimes at which scale? \na.FahrenheTime b.Celsius c.Rankine d.Kelvin",
    "Hg stands for? \na.Mercury b.Hulgerium c.Argenine d.Halfnium",
    "What element does not exist? \na.Xf b.Re c.Si d.Pa",
    "Who was the first Indian female astronaut ? \na.SunTimea Williams b.Kalpana Chawla c.None of them d.Both of them ",
    "How many states are there in India? \na.24 b.28 c.30 d.31",
    "How many players are on the field in baseball? \na.6 b.7 c.9 d.8",
    "How many players are on the field in cricket? \na.6 b.9 c.11 d.8",
    "How many wonders are there in the world? \na.7 b.8 c.10 d.4",
    "Which sea creature has three hearts? \na.Dolphin b.Octopus c.Walrus d.Seal",
    "Which planet is closest to the sun? \na.Mercury b.Pluto c.Earth d.Venus",
    "Who gifted the Statue of Libery to the US? \na.Brazil b.France c.Wales d.Germany"
]

no_q = {}

for i in range(len(Questions)):
    no_q[i+1] = Questions[i]


s.send(b"L")

while True:
    try:
        rec = s.recv(1).decode()
        if rec == 'Q':
            #rec = None
            #print(rec)
            Ques = s.recv(2).decode()
            print ("Question: ",no_q[int(Ques)])
            rec = None
            print ("Buzzer: ", end='')
            send = threading.Thread(target=user)
            send.start()
            flag=0
        if rec == 'R':
            print ("Answer: ",end='')
            send = threading.Thread(target=user)
            send.start()
            rec = None
        if rec == 'W' and inp is not None:
            print ("Waiting...")
            rec = None
            inp = None
        if rec == 'W' and inp is None:
            print ("contestant answered...")
            rec = None
            flag = 1
            time.sleep(10)
            s.send(b'L')
    
        if rec == 'T':
            print ("Correct")
            s.send(b'L')
            rec = None
        elif rec == 'F':
            print("Incorrect")
            s.send(b'L')
            rec = None
        if rec == 't' and flag == 0:
            print ("Time up")
            rec = None
            s.send(b'L')

    except:
        rec = None

    if inp is not None:
        print ("sent")
        s.sendall(inp.encode())

