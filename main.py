#!/usr/bin/python3

import subprocess
import threading
import os
import signal
from tkinter import *
from tkinter.messagebox import *

applicationName = "python-openfortivpn-gui"

root = Tk()
root.title(applicationName)
root.resizable(width=False, height=False)
root.minsize(width=650, height=25)

# Fonctions
def findTrustedCert( s, first, last ):
    try:
        start = s.rindex( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def getProcessId():
    findProcessId = subprocess.Popen(['pgrep', 'openfortivpn'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    processId = findProcessId.stdout.read()
    return (processId)

def vpnConnect():
    processId = getProcessId()

    if processId:
        showwarning(applicationName, 'You are already connected')
    else:
        def callback():
            def askAccess():
                pConnect = subprocess.Popen(['openfortivpn',
                                      vpngateway.get(),
                                      '--username='+username.get(),
                                      '--trusted-cert',
                                      vpngatewaycert.cget('text')
                                      ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

                pConnect.stdin.write((password.get()).encode())

                output = pConnect.communicate()
                outputCert = findTrustedCert(str(output),'--trusted-cert ', '\\n' )
                vpngatewaycert.config(text=outputCert)

                if outputCert:
                    showwarning(applicationName, 'Connected')
                    askAccess()  # Connect
                else:
                    showwarning(applicationName, 'Please verify your credentials')

            askAccess() # Get Cert string

        t = threading.Thread(target=callback)
        t.start()

def vpnDisconnect():
    processId = getProcessId()

    if processId:
        processIdInt = int(str(processId,'utf-8'))
        if processIdInt > 0:
            showwarning(applicationName, 'Disconnected')
            os.kill(processIdInt, signal.SIGKILL)
    root.quit()

# GUI
banner = PhotoImage(file="logo.png")

canvas = Canvas(root, width=650, height=50)
canvas.create_image(0, 0, anchor=NW, image=banner)
canvas.grid(row=1,column=0, columnspan=2, pady=15)

Label(root, text='Gateway : Port').grid(row=10,column=0, sticky="w", padx=25, pady=5)
vpngateway = Entry(root, width=45)
vpngateway.grid(row=10,column=1,padx=5, pady=5)

Label(root, text='Username').grid(row=20,column=0, sticky="w", padx=25, pady=5)
username = Entry(root, width=45)
username.grid(row=20,column=1,padx=0, pady=5)

Label(root, text='Password').grid(row=30,column=0, sticky="w", padx=25, pady=5)
password = Entry(root, show="*", width=45)
password.grid(row=30,column=1,padx=0, pady=5)

Label(root, text='Gateway Trusted Cert').grid(row=40,column=0, sticky="w", padx=25, pady=5)
vpngatewaycert = Label(root, text=' ', width=45)
vpngatewaycert.grid(row=40,column=1,padx=0, pady=5)

connectButton = Button(root, text="Connect", command=vpnConnect, height=2, width=20)
connectButton.configure(background='#63b044', foreground='#dedede', border="0")
connectButton.grid(row=100,column=0, pady=25)

quitButton = Button(root, text='Quit', command=vpnDisconnect, height=2, width=20)
quitButton.configure(background='#cb4141', foreground='#dedede', border="0")
quitButton.grid(row=100,column=1, padx=25, pady=25, sticky="e")

root.protocol("WM_DELETE_WINDOW", vpnDisconnect)
root.mainloop()