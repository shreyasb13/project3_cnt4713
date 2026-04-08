# Alexa Arce PID: 6384093
# Diego Avalos PID: 6347463
# Cristian Mantilla PID: 6393437
# Shreya Sureshbabu Banumathi PID: 6472712

# Import socket module
from socket import *
# Import RSA Encryption and Decryption
from Crypto.PublicKey import RSA
import sys

# Usage: python mycrypto.py server
# Usage: python mycrypto.py client localhost 8080

def sendCommand(clientSocket, command): # For the client side
    dataOut = command.encode("utf-8")
    clientSocket.sendall(dataOut) # Send to server
    dataIn = clientSocket.recv(1024) # Receive the response in bytes
    data = dataIn.decode("utf-8") # Decode the data
    return data # Return the decoded data

def receiveData(clientSocket): # For server side
    dataIn = clientSocket.recv(1024)
    data = dataIn.decode("utf-8")
    return data

def server():
    print("Starting server...")

    # Part 2 of Rubric - Tunnel
    print("Creating RSA keypair")
    serverKey = RSA.generate(2048)
    serverPubKey = serverKey.publickey()
    print("RSA keypair created")

    # Part 1 of Rubric - Connect
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', 8080))
    serverSocket.listen(1)
    print("Awaiting connections...")
    clientSocket, addr = serverSocket.accept()
    print("Connection requested. Creating data socket")
    dataSocket = socket(AF_INET, SOCK_STREAM)
    dataSocket.bind(('', 0))
    dataSocket.listen(1)
    port = dataSocket.getsockname()[1]
    clientSocket.sendall(str(port).encode("utf-8"))
    clientSocket.close()
    dataSocket, addr = dataSocket.accept()

    # Part 2 of Rubric - Tunnel
    print("Tunnel requested. Sending public key")
    clientKeyData = receiveData(dataSocket)  # Receives tunnel command
    clientPubKey = RSA.importKey(clientKeyData)
    serverKeyData = serverPubKey.exportKey().decode("utf-8")
    dataSocket.sendall(serverKeyData.encode("utf-8"))

    # Part 3 of Rubric - Post


def client():
    print("Starting client...")

    # Part 2 of Rubric - Tunnel
    print("Creating RSA keypair")
    clientKey = RSA.generate(2048)
    clientPubKey = clientKey.publickey()
    print("RSA keypair created")

    # Part 1 of Rubric - Connect
    print("Creating client socket")
    clientSocket = socket(AF_INET, SOCK_STREAM)  # Create first socket
    print("Connecting to server")
    clientSocket.connect((sys.argv[2], int(sys.argv[3])))  # Connect socket to the server with the IP and port
    port = sendCommand(clientSocket, "connect")  # Send the command and receive the port
    print("Creating data socket")
    clientSocket2 = socket(AF_INET, SOCK_STREAM)  # Create second socket
    clientSocket2.connect((sys.argv[2], int(port)))  # Connect second socket to the new port using the same IP

    # Part 2 of Rubric - Tunnel
    print("Requesting tunnel")
    clientKeyData = clientPubKey.exportKey().decode("utf-8")
    serverKeyData = sendCommand(clientSocket2, clientKeyData)
    serverPubKey = RSA.importKey(serverKeyData)
    print("Server public key received")
    print("Tunnel established")

    # Part 3 of Rubric - Post

def main():
    if sys.argv[1] == "server":
        server()
    elif sys.argv[1] == "client":
        client()

if __name__ == "__main__":
    main()


    



    

