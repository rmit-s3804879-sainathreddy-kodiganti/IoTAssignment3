#!/usr/bin/env python3
# Documentation: https://docs.python.org/3/library/struct.html
import socket, json, struct, sys, os

# This method is used to send the json over socket
def sendJson(socket, object):
    """ This method is used to send the json over socket
    :param (object)object
    """
    jsonString = json.dumps(object)
    data = jsonString.encode("utf-8")
    jsonLength = struct.pack("!i", len(data))
    socket.sendall(jsonLength)
    socket.sendall(data)
    #print ("sent ", object)

# This method is used to send thr pickle file over socket
def sendPickle(socket, file_path):
    """ This method is used to send thr pickle file over socket
    :param (str)file_path
    """
    with open(file_path, "rb") as f:
        # read the bytes from the file
        bytes_read = f.read(4096)
        # we use sendall to assure transimission in 
        # busy networks
        socket.sendall(bytes_read)

# This method is used to receive a pickle file and save in path provided
def recvPickle(socket_obj, path_to_write):
    """ This method is used to receive a pickle file and save in path provided
    :param (str)path_to_write
    """
    socket_obj.setblocking(False)
    with open(path_to_write, "wb") as f:
        data= b''
        while True:
            buffer = socket_obj.recv(25384, socket.MSG_WAITALL)
            # write to the file the bytes we just received
            if not buffer:break
            data += buffer
        print('writing')
        f.write(data)
        socket_obj.close()
    return True

# This method is used to receive a json from socket
def recvJson(socket):
    """ This method is used to receive a json from socket
    :param (object)socket
    """
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

def checkFile(path_to_write):
    """ This method is used to check is the file exist
    :param (str)path_to_write
    """
    return os.path.exists(path_to_write)