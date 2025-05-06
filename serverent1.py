import os
import socket

def send(addr:str, port:int, fileName:str):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((addr, port))

    file_name = fileName
    file_size = os.path.getsize(file_name)

    name_to_send = file_name.split('.')[0]

    client.send(f"{name_to_send}<NAME_END>".encode())
    client.send(f"{file_size}<SIZE_END>".encode())

    with open(file_name, "rb") as f:
        while (chunk := f.read(1024)):
            client.send(chunk)
        client.send("<FILE_END>".encode())
    
    client.close()


if __name__=="__main__":
    print("Sending...")
    send('localhost', 9999, 'image.jpg')
    print("Done.")
