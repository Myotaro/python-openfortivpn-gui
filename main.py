#!../../.local/share/virtualenvs/LearnPython-UdQ-JvbQ/bin/python3

import subprocess
import time
from tkinter import *
from tkinter.messagebox import *

import requests

applicationName = "VPN Com'Unity"
#WINDOW_SIZE = "800x800"

root = Tk()
root.title(applicationName)
#root.geometry(WINDOW_SIZE)

response = requests.get('https://httpbin.org/ip')

Label(root, text='Votre IP: ' + format(response.json()['origin'])).pack()
Label(root, text='Heure de lancement ' + time.strftime("%I:%M:%S") + '\n').pack()

Label(root, text='Username').pack()
username = Entry(root)
username.pack()

Label(root, text='Password').pack()
password = Entry(root)
password.pack()

Label(root, text='Gateway').pack()
vpngateway = Entry(root)
vpngateway.pack()

Label(root, text='Port').pack()
vpngatewayport = Entry(root)
vpngatewayport.pack()

Label(root, text='Gateway Cert').pack()
vpngatewaycert = Entry(root)
vpngatewaycert.pack()

shellOutput = Text(root)
shellOutput.config(width=99, height=25)
shellOutput.pack()
shellOutput.insert(END, 'Ready to connect')

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

Button(root, text="Connect", command=vpnConnect).pack()


def callbackQuitWindow():
    showwarning(applicationName, 'The application will now kill the VPN tunnel')
    root.quit()

Button(root, text='Quit', command=callbackQuitWindow).pack()

root.mainloop()