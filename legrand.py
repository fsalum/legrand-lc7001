#!/usr/bin/env python3
from Crypto.Cipher import AES
import binascii
import hashlib
import socket
import sys
import time


HOST = 'LCM1.local'
PORT = 2112
LC7001_PASSWORD = b'12345678' # For testing purposes :)

def socket_connection():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    print('Socket Created')

    try:
        remote_ip = socket.gethostbyname(HOST)
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    s.connect((remote_ip , PORT))
    print('Socket Connected to ' + HOST + ' on ip ' + remote_ip)

    return s


def recv_timeout(the_socket,timeout=5):
    #make socket non blocking
    the_socket.setblocking(0)

    #total data partwise in an array
    total_data=[];
    data='';

    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break

        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break

        #recv something
        try:
            data = str(the_socket.recv(8192).decode('ascii'))
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin=time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass

    #join all parts to make final string
    return ''.join(total_data)


def encrypt_key(challenge):
    private_key = binascii.unhexlify(hashlib.md5(LC7001_PASSWORD).hexdigest())
    print('Password MD5:', binascii.hexlify(private_key).decode('ascii'))
    encryptor = AES.new(private_key, AES.MODE_ECB)
    lc7001_hello = binascii.unhexlify(challenge)
    ciphertext = encryptor.encrypt(lc7001_hello)
    challenge_answer = binascii.hexlify(ciphertext)
    print('Encrypted Response:', challenge_answer.decode('ascii').upper())

    return challenge_answer


if __name__ == "__main__":
    s = socket_connection()

    total_data = recv_timeout(s).split( )
    total_data = [x.replace('\x00', '') for x in total_data]
    challenge = total_data[2]
    print('LC7001 password:', LC7001_PASSWORD.decode('ascii'))
    print("Challenge:", challenge)

    challenge_answer = encrypt_key(challenge)

    #Answer the challenge to the server
    try:
        s.sendall(challenge_answer)
        print(recv_timeout(s))
    except socket.error:
        print('Send failed')
        sys.exit(1)

    #Close the socket
    s.close()
