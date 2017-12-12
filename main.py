#!../../.local/share/virtualenvs/LearnPython-UdQ-JvbQ/bin/python3

import subprocess
import time
from tkinter import *
from tkinter.messagebox import *
import threading
import requests
import os
import signal

#Défition des variables fixes
applicationName = "openfortivpn"
#WINDOW_SIZE = "800x800"

root = Tk()
root.title(applicationName)
#root.geometry(WINDOW_SIZE)
#root.configure(background='#666666')
root.minsize(width=700,height=650)
root.maxsize(width=700,height=650)

#Défition des fonctions
def bytes_to_int(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + int(b)

    return result

def vpnConnect():
    findProcessId = subprocess.Popen(['pgrep', 'openfortivpn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     stdin=subprocess.PIPE)
    processId = findProcessId.stdout.read()
    #processIdInt = int(str(processId, 'utf-8'))
    if processId:
        showwarning(applicationName, 'Déjà connecté!!')
    else:
        def callback():
            pConnect = subprocess.Popen(['openfortivpn',
                                  vpngateway.get() + ":" + vpngatewayport.get(),
                                  '--username='+username.get(),
                                  '--trusted-cert',
                                  vpngatewaycert.get()
                                  ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            pConnect.stdin.write((password.get()).encode())

            output = pConnect.communicate()

            shellOutput.delete('1.0', END)
            shellOutput.insert(END, output)
            #showwarning(applicationName, output)

        t = threading.Thread(target=callback)
        t.start()

def vpnDisConnect():
    findProcessId = subprocess.Popen(['pgrep', 'openfortivpn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    processId = findProcessId.stdout.read()
    if processId:
        processIdInt = int(str(processId,'utf-8'))
        if processIdInt > 0:
            #showwarning(applicationName, processIdInt)
            os.kill(processIdInt, signal.SIGKILL)  # signal.SIGTERM or signal.SIGKILL

def callbackQuitWindow():
    vpnDisConnect()
    root.quit()

#Template
response = requests.get('https://httpbin.org/ip')
Label(root, text='Votre IP: ' + format(response.json()['origin'])).grid(row=0, column=0)
Label(root, text='Heure de lancement ' + time.strftime("%I:%M:%S")).grid(row=0, column=1)

Label(root, text='Username').grid(row=1,column=0)
username = Entry(root, width=22)
username.grid(row=1,column=1)

Label(root, text='Password').grid(row=2,column=0)
password = Entry(root, width=22)
password.grid(row=2,column=1)

Label(root, text='Gateway').grid(row=3,column=0)
vpngateway = Entry(root, width=22)
vpngateway.grid(row=3,column=1)

Label(root, text='Port').grid(row=4,column=0)
vpngatewayport = Entry(root, width=22)
vpngatewayport.grid(row=4,column=1)

Label(root, text='Gateway Trusted Cert').grid(row=5,column=0)
vpngatewaycert = Entry(root, width=22)
vpngatewaycert.grid(row=5,column=1)

connectButton = Button(root, text="Connect", command=vpnConnect, height=1, width=19)
connectButton.grid(row=7,column=1)

shellOutput = Text(root)
shellOutput.config(width=99, height=25)
shellOutput.configure(background='#333333', foreground='#dedede')
shellOutput.grid(row=99,column=0, columnspan=2)
shellOutput.insert(END, 'Ready to connect')

quitButton = Button(root, text='Quit', command=callbackQuitWindow, height=2, width=20)
quitButton.grid(row=110,column=1,padx=0, pady=0)

root.mainloop()
