import socket
import cv2
import numpy

def recvall(server, count):
    buf = b''
    while count:
        newbuf = server.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
	
TCP_IP = '140.116.164.19'
TCP_PORT = 5001

# AF_INET -> IPv4, SOCK_STREAM -> TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
server.bind((TCP_IP, TCP_PORT))
print 'Socket bind complete'
server.listen(True)
print 'Socket now listening'
conn, addr = server.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])

while (True):
    length = recvall(conn,16)
    stringData = recvall(conn, int(length))
    #stringData = conn.recv(102400)
    data = numpy.fromstring(stringData, dtype='uint8')
    
    decimg=cv2.imdecode(data,1)
    cv2.imshow('Server', decimg)
    cv2.waitKey(10)

server.close()
cv2.destroyAllWindows() 