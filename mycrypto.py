# Alexa Arce PID: 6384093
# Diego Avalos PID: 6347463
# Cristian Mantilla PID: 6393437
# Shreya Sureshbabu Banumathi PID: 6472712

# Import socket module
from socket import *
import sys


def sendCommand(clientSocket, command): #for the client side
    dataOut = command.encode("utf-8")
    clientSocket.sendall(dataOut) #send to server
    dataIn = clientSocket.recv(1024) #recieve the response in bytes
    data = dataIn.decode("utf-8") #decode the data
    return data #return the decoded data

def receiveData(clientSocket): #for server side
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    return data

def main():
    #part 1 of rubric
    clientSocket = socket(AF_INET, SOCK_STREAM) #Create first socket
    clientSocket.connect((sys.argv[1], int(sys.argv[2]))) #connect socket to the server with the IP and port
    port = sendCommand(clientSocket, "connect") #send the command and receive the port 
    print('Port return: ', port) #print port
    clientSocket2 = socket(AF_INET, SOCK_STREAM) #create second socket
    clientSocket2.connect((sys.argv[1], int(port))) #connect second socket to the new port using hte same IP

if __name__ == "__main__":
    main()


    



    

