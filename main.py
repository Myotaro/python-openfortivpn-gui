#!/usr/bin/python3

import subprocess
import threading
import os
import signal
from tkinter import *
from tkinter.messagebox import *

applicationName = "openfortivpn"

root = Tk()
root.title(applicationName)

# Fonctions
def vpnConnect():
    findProcessId = subprocess.Popen(['pgrep', 'openfortivpn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     stdin=subprocess.PIPE)
    processId = findProcessId.stdout.read()
    if processId:
        showwarning(applicationName, 'Déjà connecté!!')
    else:
        def callback():
            pConnect = subprocess.Popen(['openfortivpn',
                                  vpngateway.get(),
                                  '--username='+username.get(),
                                  '--trusted-cert',
                                  vpngatewaycert.get()
                                  ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            pConnect.stdin.write((password.get()).encode())

            output = pConnect.communicate()

            shellOutput.delete('1.0', END)
            shellOutput.insert(END, output)

        t = threading.Thread(target=callback)
        t.start()

def vpnDisConnect():
    findProcessId = subprocess.Popen(['pgrep', 'openfortivpn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    processId = findProcessId.stdout.read()
    if processId:
        processIdInt = int(str(processId,'utf-8'))
        if processIdInt > 0:
            os.kill(processIdInt, signal.SIGKILL)

def callbackQuitWindow():
    vpnDisConnect()
    root.quit()

# GUI
Label(root, text='Gateway : Port').grid(row=1,column=0, sticky="w")
vpngateway = Entry(root, width=45)
vpngateway.grid(row=1,column=1,padx=0, pady=5)

Label(root, text='Username').grid(row=2,column=0, sticky="w")
username = Entry(root, width=45)
username.grid(row=2,column=1,padx=0, pady=5)

Label(root, text='Password').grid(row=3,column=0, sticky="w")
password = Entry(root, width=45)
password.grid(row=3,column=1,padx=0, pady=5)

Label(root, text='Gateway Trusted Cert').grid(row=4,column=0, sticky="w")
vpngatewaycert = Entry(root, width=45)
vpngatewaycert.grid(row=4,column=1,padx=0, pady=5)

shellOutput = Text(root)
shellOutput.config(width=79, height=15)
shellOutput.configure(background='#333333', foreground='#dedede')
shellOutput.grid(row=99,column=0, columnspan=5)
shellOutput.insert(END, '')

connectButton = Button(root, text="Connect", command=vpnConnect, height=2, width=20)
connectButton.configure(background='green', foreground='#dedede', border="2px")
connectButton.grid(row=110,column=0)

quitButton = Button(root, text='Quit', command=callbackQuitWindow, height=2, width=20)
quitButton.configure(background='red', foreground='#dedede', border="2px")
quitButton.grid(row=110,column=1,padx=0, pady=0, sticky="e")

root.mainloop()