import socket
import sys
import threading
import time
from random import *

host = '127.0.0.1'
port = 65432
buzzer = None
i=0
connections = []

score = {}

Questions = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
dAnswers = {}

Answers = ['c', 'a', 'a', 'a', 'a', 'a', 'a', 'b', 'b', 'c', 'c', 'a', 'b', 'a', 'b']
dAnswers = {}
for i in range(len(Questions)):
    dAnswers[Questions[i]] = Answers[i]


                    

def Send(msg):
    for conn in all_connections:
        try:
            conn.send(msg)
        except:
            conn.close()
            remove(conn)
Rquestions = []
for i in range(len(Questions)):
    n = choice(Questions)
    Rquestions.append(n)
    Questions.remove(n)
def clientThread(conn, ip, port, buzzer, Rquestions, index, times,counter,Time):
    conn.settimeout(10)
    while index!=15:
        if len(connections) == 3:
            start = conn.recv(1).decode()
            if start=="L":
                Time = time.time()
                Q = Rquestions[index]
                A = dAnswers[Q]
                index+=1
                conn.send(b'Q')
                conn.sendall(str(Q).encode())
                try:
                    buzzer = conn.recv(1).decode()
                    for i in connections:
                        i.sendall(b'W')
                    endt = time.time()
                    times.append(endt)
                except:
                    # si len(l) need a cross check
                    if len(times)!=0 and counter<len(times):
                        var = times[len(times)-1]
                        if counter>Time:
                            #print ("did first")
                            time.sleep(var-Time)
                            counter+=1
                    score[conn]-=0.5
                    conn.send(b't')
                if buzzer is not None:
                    Time = time.time()
                    conn.send(b'R')
                    try:
                        rec = conn.recv(1).decode()
                        conn.send(b'W')
                        f = time.time()
                        time.sleep(10-f+Time)
                        if rec == str(A):
                            score[conn] += 1
                            conn.send(b'T')
                        else:
                            score[conn]-=0.5
                            conn.send(b'F')
                    except:
                        score[conn]-=0.5
                        conn.send(b't')
                    buzzer = None
        for i in connections:
             print(i,"    ",score[i])
             if score[i]>=5:
                 print ("Winner: ",i)
                 return
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen()

    while True:
        conn, addr = s.accept()
        connections.append(conn)
        score[conn] = 0
        buzzer =None
        Time=time.time()
        counter=0
        index = 0
        times=[]
        threading.Thread(target = clientThread, args = (conn, str(addr[0]), str(addr[1]),buzzer,Rquestions, index, times,counter,Time)).start()
s.close()
