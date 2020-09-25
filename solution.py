#import socket module
from socket import *
from datetime import datetime
from time import gmtime, strftime
import sys # In order to terminate the program
import os

def send_bytes(bytes, socket):
  total_bytes_sent = 0
  bytes_to_send = len(bytes)
  while total_bytes_sent < bytes_to_send:
    bytes_sent = socket.send(bytes)
    total_bytes_sent = total_bytes_sent + bytes_sent

def webServer(port=13331):
  serverSocket = socket(AF_INET, SOCK_STREAM)

  #Prepare a sever socket
  #Fill in start
  serverSocket.bind(('', port))
  serverSocket.listen()
  #Fill in end

  while True:
    #Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    try:
      message = connectionSocket.recv(1048).decode()#Fill in start    #Fill in end
      filename = message.split()[1]
      f = open(filename[1:])
      outputdata = f.read()#Fill in start     #Fill in end
      f.close()

      #Send one HTTP header line into socket
      #Fill in start
      header_lines = []
      encoded_data = outputdata.encode()
      status_line = "HTTP/1.1 200 OK"
      header_lines.append(("Date", datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S") + " GMT"))
      header_lines.append(("Last-Modified", strftime("%a, %d %b %Y %H:%M:%S", gmtime(os.path.getmtime(filename[1:]))) + " GMT"))
      header_lines.append(("Content-Type", "text/html; charset=utf-8")) #just assume for this assignment
      header_lines.append(("Content-Length", str(len(encoded_data))))
      header_lines.append(("Connection", "close"))
      header_lines.append(())

      response_lines = [status_line]
      response_lines.extend(map(lambda x: ": ".join(x), header_lines))
      send_bytes("\r\n".join(response_lines).encode(), connectionSocket)
      send_bytes("\r\n".encode(), connectionSocket)

      #Fill in end

      #Send the content of the requested file to the client
      send_bytes(encoded_data, connectionSocket)

      connectionSocket.send("\r\n".encode())
      connectionSocket.close()
    except IOError:
        #Send response message for file not found (404)
        #Fill in start
        header_lines = []
        status_line = "HTTP/1.1 404 Not Found"
        header_lines.append(("Date", datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S") + " GMT"))
        header_lines.append(("Connection", "close"))
        header_lines.append(())

        response_lines = [status_line]
        response_lines.extend(map(lambda x: ": ".join(x), header_lines))
        send_bytes("\r\n".join(response_lines).encode(), connectionSocket)
        send_bytes("\r\n".encode(), connectionSocket)
        #Fill in end

        #Close client socket
        #Fill in start
        connectionSocket.close()
        #Fill in end

  serverSocket.close()
  sys.exit()  # Terminate the program after sending the corresponding data

if __name__ == "__main__":
  webServer(13331)
