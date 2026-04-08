# Alexa Arce PID: 6384093
# Diego Avalos PID: 6347463
# Cristian Mantilla PID: 6393437
# Shreya Sureshbabu Banumathi PID: 6472712

# Import socket module
from email.mime import message
from socket import *
# Import RSA Encryption and Decryption
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP 
import hashlib
import base64
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
    print("Post requested.")
    encrypted_msg = receiveData(dataSocket)
    print("Received encrypted message:", encrypted_msg)
    encrypted_bytes = base64.b64decode(encrypted_msg) # Decodes base64 string to bytes
    cipher = PKCS1_OAEP.new(serverKey) # Decrypts message using the server's private key
    decrypted_msg = cipher.decrypt(encrypted_bytes).decode("utf-8")
    print("Decrypted message:", decrypted_msg)
    print("Computing hash")
    hash_value = hashlib.sha256(decrypted_msg.encode("utf-8")).hexdigest() # Computes the hash of decrypted message
    cipher_client = PKCS1_OAEP.new(clientPubKey) # Will encypt the hash using client's public key
    encrypted_hash = cipher_client.encrypt(hash_value.encode("utf-8"))
    encrypted_hash_str = base64.b64encode(encrypted_hash).decode("utf-8")
    print("Responding with hash:", hash_value)
    dataSocket.sendall(encrypted_hash_str.encode("utf-8"))


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
    message = "Hello"
    print("Encrypting message:", message)
    cipher = PKCS1_OAEP.new(serverPubKey) # Encrypt message using server's public key
    encrypted_msg = cipher.encrypt(message.encode("utf-8"))
    encrypted_msg_str = base64.b64encode(encrypted_msg).decode("utf-8") # Will encode messafe to base64 string to send
    print("Sending encrypted message:", encrypted_msg_str)
    clientSocket2.sendall(encrypted_msg_str.encode("utf-8")) # Send message to server
    encrypted_hash_str = receiveData(clientSocket2) # Receives encrypted hash 
    print("Received hash")
    encrypted_hash = base64.b64decode(encrypted_hash_str)
    cipher_client = PKCS1_OAEP.new(clientKey) # Deccrypts the hash using the client's private key
    server_hash = cipher_client.decrypt(encrypted_hash).decode("utf-8")
    print("Computing hash")
    local_hash = hashlib.sha256(message.encode("utf-8")).hexdigest()

    # Compares the hash received from server with hash computed locally to check if message was compromised
    if local_hash == server_hash:
        print("Secure")
    else:
        print("Compromised")

def main():
    if sys.argv[1] == "server":
        server()
    elif sys.argv[1] == "client":
        client()

if __name__ == "__main__":
    main()
