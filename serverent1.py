import os
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999))

file_name = 'image.jpg'
file_size = os.path.getsize(file_name)

client.send(f"{file_name}_sent.jpg<NAME_END>".encode())
client.send(f"{file_size}<SIZE_END>".encode())

with open(file_name, "rb") as f:
    while (chunk := f.read(1024)):
        client.send(chunk)
    client.send("<FILE_END>".encode())



client.close()
