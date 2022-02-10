'''
Minh Pham & Maiah Pardo
CIS 41B  |  Spring 2019
Assignment 5 - Server
'''
import sys, socket, numpy as np, pickle, math, threading

HOST = "localhost"
PORT = 5551
MAXCLIENTS = 4
MINTIME = 10
MAXTIME = 30
DATAPOINTS = 50

class server():
    def __init__(self):
        '''Initalize the server and starts threads for new clients, waiting using a menu'''
        if len(sys.argv) != 3:
            print("Usage: server.py num_of_clients num-of_secs_timeout")
            return
        try:
            numClients = int(sys.argv[1])
            timeoutTimer = int(sys.argv[2])
        except ValueError:
            print("Invalid argument. Try again.")
            return

        if numClients <= 0 or numClients > MAXCLIENTS:
            print(f"Please select between 1 and {MAXCLIENTS} clients")
            return
        elif timeoutTimer < MINTIME or timeoutTimer >MAXTIME:
            print(f"Please set timeout to a value between {MINTIME} and {MAXTIME} seconds.")
            return

        with socket.socket() as s:
            s.bind((HOST, PORT))
            print("Server hostname:", HOST, "  |  port:", PORT)

            s.settimeout(timeoutTimer)
            s.listen()
            threads = []
            for i in range(1, numClients+1):
                try:
                    (conn, addr) = s.accept()

                    conn.send(f"{i} {addr[1]}".encode('utf-8') )
                    t = threading.Thread(target=self.clientRequest, args=(conn,))
                    t.start()
                    threads.append(t)
                except socket.timeout:
                    print(f"Connection {i} timed out")

        # wait for all clients to quit before closing server
        for t in threads:
            t.join()


    def clientRequest(self, conn):
        '''Menu to wait for client's request'''
        while True:
            inputList = conn.recv(1024).decode('utf-8').split()
            if inputList[0] == 'p':
                conn.send( pickle.dumps( self.powerFunc(inputList) ) )     # passing p, exp, min, max; sending pickled np.array
            elif inputList[0] == 's':
                conn.send( pickle.dumps( self.sineFunc(inputList) ) )      # passing s, freq; sending pickled np.array
            else:                                                          # input is q
                break

    def minMax(func):
        '''Decorator to print the min and max return value of the function on console'''
        def printReturn(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f"{result.min()}, {result.max()}")
            return result
        return printReturn

    @minMax
    def powerFunc(self, inputList:list):
        '''Creates an np.array with input and exponent provided'''
        return np.linspace(int(inputList[2]), int(inputList[3]), DATAPOINTS)**int(inputList[1])

    @minMax
    def sineFunc(self, inputList:list):
        '''Creates np.array with specified input and function for sine/cos graphing'''
        return np.linspace(0,1,DATAPOINTS)*int(inputList[1])*2*math.pi

server()