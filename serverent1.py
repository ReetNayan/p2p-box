import os
import socket

def parse_filename(file_name:str)->list:
    """
    This function takes a file name and separates its name from the extension.
    """
    name_data = file_name.split('.') # Split filename on '.'

    extension = name_data[ len(name_data) - 1 ]
    name = '.'.join( name_data[ 0:len(name_data)-1 ] )

    return [name, extension]


    


def send(addr:str, port:int, fileName:str):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((addr, port))

    file_name = parse_filename(fileName)[0]
    file_ext = parse_filename(fileName)[1]

    complete_file_name = file_name+'.'+file_ext

    file_size = os.path.getsize(complete_file_name)

    client.send(f"{file_name}_received.{file_ext}<NAME_END>".encode())
    client.send(f"{file_size}<SIZE_END>".encode())

    with open(complete_file_name, "rb") as f:
        while (chunk := f.read(1024)):
            client.send(chunk)
        client.send("<FILE_END>".encode())
    
    client.close()


if __name__=="__main__":
    print("Sending...")
    send('localhost', 9999, "image.jpg")
    print("Done.")
