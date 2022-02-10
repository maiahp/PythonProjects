'''
Minh Pham & Maiah Pardo
CIS 41B  |  Spring 2019
Assignment 5 - Client
'''
import socket, pickle, matplotlib.pyplot as plt, math, numpy as np

HOST = '127.0.0.1'
PORT = 5551

class Client():
    def __init__(self):
        '''Initalize the server and starts threads for new clients, waiting using a menu'''
        functions = {'p': self.plotPower, 's': self.plotSine}

        with socket.socket() as self.s :
            self.s.connect((HOST, PORT))
            print("Client connected to:", HOST, "  |  port:", PORT)
            self.num, self.ID = self.s.recv(512).decode('utf-8').split()
            print(f"Client {self.num}  | ID: {self.ID}")

            while True:
                #menu option selection
                if( self.menu() == 'q'): break

    def menu(self):
        '''Displays the menu for user selection which loops until the user types "q"'''
        functions = {'p': self.plotPower, 's': self.plotSine, 'q':self.quit}

        while True:
            print("p: power function\ns: sine function\nq: quit")
            choice = input("Enter choice: ").lower()
            if choice in functions: return functions[choice]()
            else: print("Invalid choice, try again")

    def quit(self):
        '''Helper function to close the connection on the client's and server's side'''
        self.s.send('q, '.encode('utf-8'))
        return 'q'

    def plotPower(self):
        '''Asks for user input and plot the power graph using the given array'''
        try:
            power, xMin, xMax = [int(i) for i in input("Enter exponent, min-x, max-x: ").split(',')]
        except ValueError:
            print("Invalid or missing argument(s). Try again.")
            return

        self.s.send(' '.join(['p', str(power), str(xMin), str(xMax)]).encode('utf-8'))
        data = pickle.loads( self.s.recv(4096) )

        plt.figure(f"Client {self.num}  | ID: {self.ID}")
        plt.title(f"x^{power:.0f} for x = {xMin} to {xMax}")
        plt.xlabel("x")
        plt.grid()
        plt.plot(np.linspace(xMin, xMax, len(data)), data)
        plt.show()

    def plotSine(self):
        '''Asks for user input and plot the sine graph using the given array'''
        try:
            freq = int(input("Enter frequency: "))
        except ValueError:
            print("Invalid argument. Try again.")
            return

        self.s.send(f"s {freq}".encode('utf-8'))

        data = pickle.loads( self.s.recv(2048) )
        plt.figure(f"Client {self.num}  | ID: {self.ID}")
        plt.title(f"sine {freq}x")
        plt.xlabel("x")
        plt.grid()
        plt.plot(np.linspace(0,1,len(data)), np.sin(data))

        plt.show()

if __name__ == "__main__":
    Client()