#!../../.local/share/virtualenvs/LearnPython-UdQ-JvbQ/bin/python3

import subprocess
import time
from tkinter import *
from tkinter.messagebox import *

import requests

#Défition des variables fixes
applicationName = "VPN Com'Unity"
#WINDOW_SIZE = "800x800"

root = Tk()
root.title(applicationName)
#root.geometry(WINDOW_SIZE)

#Défition des fonctions
def vpnConnect():
    p = subprocess.Popen(['openfortivpn',
                          vpngateway.get() + ":" + vpngatewayport.get(),
                          '--username='+username.get(),
                          '--trusted-cert',
                          vpngatewaycert.get()
                          ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    p.stdin.write((password.get()).encode())

    output = p.communicate()[0]

    shellOutput.delete('1.0', END)
    shellOutput.insert(END, output)
    #showwarning(applicationName, output)

def callbackQuitWindow():
    showwarning(applicationName, 'The application will now kill the VPN tunnel')
    root.quit()

#Template
response = requests.get('https://httpbin.org/ip')
Label(root, text='Votre IP: ' + format(response.json()['origin'])).grid(row=0, column=0)
Label(root, text='Heure de lancement ' + time.strftime("%I:%M:%S") + '\n').grid(row=0, column=1)

Label(root, text='Username').grid(row=1,column=0)
username = Entry(root)
username.grid(row=1,column=1)

Label(root, text='Password').grid(row=2,column=0)
password = Entry(root)
password.grid(row=2,column=1)

Label(root, text='Gateway').grid(row=3,column=0)
vpngateway = Entry(root)
vpngateway.grid(row=3,column=1)

Label(root, text='Port').grid(row=4,column=0)
vpngatewayport = Entry(root)
vpngatewayport.grid(row=4,column=1)

Label(root, text='Gateway Cert').grid(row=5,column=0)
vpngatewaycert = Entry(root)
vpngatewaycert.grid(row=5,column=1)

Button(root, text="Connect", command=vpnConnect).grid(row=6,column=2)

shellOutput = Text(root)
shellOutput.config(width=99, height=25)
shellOutput.grid(row=99,column=0, columnspan=3)
shellOutput.insert(END, 'Ready to connect')

Button(root, text='Quit', command=callbackQuitWindow).grid(row=100,column=2)

root.mainloop()