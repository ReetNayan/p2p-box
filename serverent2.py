import socket
import tqdm

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen(1)

sender, addr = server.accept()

buffer = b""
while b"<SIZE_END>" not in buffer:
    buffer += sender.recv(1024)

file_name_encoded, remaining_data = buffer.split(b"<NAME_END>")
file_size_encoded, remaining_data = remaining_data.split(b"<SIZE_END>")

file_name = file_name_encoded.decode()+"_recieved.jpg"
file_size = int(file_size_encoded.decode())

print(f"[FILE] {file_name}")
print(f"[FILE SIZE] {file_size} bytes")
print("\n--RECIEVING--\n")

progress = tqdm.tqdm(unit="B", unit_scale=True, unit_divisor=1000, total=int(file_size))

with open(file_name, "wb") as f:
    f.write(remaining_data)
    bytes_recv = len(remaining_data)

    while bytes_recv < file_size:
        chunk = sender.recv(min(4096, file_size-bytes_recv))
        if not chunk: 
            break
        f.write(chunk)
        bytes_recv+=len(chunk)
        progress.update(len(chunk))
    
sender.close()
server.close()

