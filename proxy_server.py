#!/usr/bin/env python3

import socket
import time

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


def main():
    #google_addr = None
    addr_info = socket.getaddrinfo("www.google.com",PORT)
    for addr in addr_info:
        (family, socktype, proto, canonname, sockaddr) = addr
        if family == socket.AF_INET and socktype == socket.SOCK_STREAM:
            google_addr = addr
            
            
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST,PORT))
        s.listen(1) #listen one connection at a time
        while True:
            conn, addr = s.accept()
            print("connected by", addr)

            (family, socktype, proto, canonname, sockaddr) = google_addr
            with socket.socket(family, socktype) as proxy_end:
                proxy_end.connect(sockaddr)
                
                send_full_data = b""
                while True:
                    data = conn.recv(BUFFER_SIZE)
                    if not data: break
                    send_full_data += data
                proxy_end.sendall(send_full_data)
                proxy_end.shutdown(socket.SHUT_WR)

                recv_full_data = b""
                while True:
                    data = proxy_end.recv(BUFFER_SIZE)
                    if not data: break
                    recv_full_data += data
                    
            time.sleep(0.5)
            conn.sendall(full_data)
        
if __name__ == "__main__":
    main()
