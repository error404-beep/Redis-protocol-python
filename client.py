import socket


SERVER = "localhost"
PORT = 6379

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
def ECHO_Check(client):
    message = '*2\r\n$4\r\necho\r\n$3\r\nhey\r\n'
    msg = message.encode('utf-8')
    client.send(msg)


def multiple_ping_check(client):
    msg = '*1\r\n$4\r\nPING\r\n'
    for i in range(10):
        client.send(msg.encode('utf-8'))
        print(client.recv(6).decode('utf-8'))

def set_check(client):
    message = '*3\r\n$3\r\nset\r\n$5\r\nhello\r\n$3\r\nmsg\r\n'
    msg = message.encode('utf-8')
    client.send(msg)
    rev = client.recv(5).decode('utf-8')
    print(rev)
    
    message = '*2\r\n$3\r\nget\r\n$5\r\nhello\r\n'
    msg = message.encode('utf-8')
    client.send(msg)
    rev = client.recv(8).decode('utf-8')
    print(rev)

#multiple_ping_check(client)
#ECHO_Check(client)
#set_check(client)
multiple_ping_check(client)
