import socket
import cv2
import numpy

UDP_IP = '140.116.164.19'
UDP_PORT = 5001

# AF_INET -> IPv4, SOCK_STREAM -> TCP, SOCK_DGRAM -> UDP
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print 'Socket created'
server.bind((UDP_IP, UDP_PORT))
print 'Socket bind complete'
#server.listen(True)
print 'Socket now listening'
#conn, addr = server.accept()
#print 'Connected with ' + addr[0] + ':' + str(addr[1])

def recvall(server, count):
    buf = b''
    while count:
        newbuf,addr = server.recvfrom(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
s=""
while (True):
    #length = recvall(server,16)
    #stringData = recvall(server, int(length))
    #stringData, addr = server.recv(64950)
    #data = numpy.fromstring(stringData, dtype='uint8')
    
    #decimg=cv2.imdecode(data,1)
    data, addr = server.recvfrom(23040)
    s += data
    if len(s) == (23040*40):
        frame = numpy.fromstring(s,dtype=numpy.uint8)
        frame = frame.reshape(480,640,3)
        cv2.imshow('frame',frame)
        s=""
    #cv2.imshow('Server', decimg)
    cv2.waitKey(10)

conn.close()
server.close()
cv2.destroyAllWindows() 