#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/struct.html
import socket, json, struct, sys

# This method is used to send the json over socket
def sendJson(socket, object):
    jsonString = json.dumps(object)
    data = jsonString.encode("utf-8")
    jsonLength = struct.pack("!i", len(data))
    socket.sendall(jsonLength)
    socket.sendall(data)
    #print ("sent ", object)

# This method is used to send thr pickle file over socket
def sendPickle(socket, file_path):
    with open(file_path, "rb") as f:
        # read the bytes from the file
        bytes_read = f.read(4096)
        # we use sendall to assure transimission in 
        # busy networks
        socket.sendall(bytes_read)

# This method is used to receive a pickle file and save in path provided
def recvPickle(socket, path_to_write):
    with open(path_to_write, "wb") as f:
        buffer = socket.recv(4096)
        # write to the file the bytes we just received
        f.write(buffer)
    return True

# This method is used to receive a json from socket
def recvJson(socket):
    buffer = socket.recv(4)
    if buffer:
        print('recieved')
        jsonLength = struct.unpack("!i", buffer)[0]
        # Reference: https://stackoverflow.com/a/15964489/9798310
        buffer = bytearray(jsonLength)
        view = memoryview(buffer)
        while jsonLength:
            nbytes = socket.recv_into(view, jsonLength)
            view = view[nbytes:]
            jsonLength -= nbytes

        jsonString = buffer.decode("utf-8")
        return json.loads(jsonString)
