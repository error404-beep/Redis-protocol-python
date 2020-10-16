import threading
import time
import socket

ENCODING = 'utf-8'

KEYS = {}

def main():
    s = socket.create_server(("localhost", 6379), reuse_port=True)
    print(s)
    # s.settimeout(5)
    s.listen()
    while(True):
        
        conn, addr = s.accept() # wait for client
        thread = threading.Thread(target=handle_client, args=(conn, addr)) 
        thread.start()
        

def handle_client(conn, addr):
    while(True):
        print(f'CURRENT NUMBER OF KEYS: {len(KEYS)}')
        arr_length = take_input(conn)
        
        print(f'arr_length recv: {arr_length}')
        length = arr_length[1:]
        try:
            length = int(length)
        except:
            break
        print(f'arr_length: {arr_length} and length: {length}')

        while(length>0):
            msg_length = take_input(conn)
            print(f'msg_length before int: {msg_length}')
            try:
                ms_l = int(msg_length[1])
                length -= 1
            except:
                break
            print(f'msg_length: {msg_length} and ms_l: {ms_l}')
            if(ms_l):
                res = take_input(conn,ms_l+2)
                print(f'res {res}')
                #To Check is Command
                if res == "echo\r\n":
                    cmd_echo(conn)
                    length -= 1
                elif res == "set\r\n":
                    length = cmd_set(conn, length)
                    print('SET COMMAND EXITED')
                    print(f'Current keys in KEYS {len(KEYS)}')
                    length -= 2
                    print(f'Message length left: {length}')
                elif res == "get\r\n":
                    cmd_get(conn)
                    length -= 1
                else:
                    send_msg = "+PONG\r\n"
                    send_msg = send_msg.encode(encoding=ENCODING)
                    conn.send(send_msg)
                    length -= 1
        print(f'{length}')

def cmd_echo(conn):
    print('ECHO COMMAND ENTERED')
    msg_len = take_input(conn)
    msg_l = int(msg_len[1])
    msg = take_input(conn, msg_l+2)
    print(f'Recived Message to ECHO: {msg}')
    msg = '+' + msg + '\r\n'
    msg = msg.encode(encoding=ENCODING)
    conn.send(msg)

def cmd_set(conn, length):
        print("SET Command entered")
        key_len = take_input(conn)
        key_l = int(key_len[1])
        key = take_input(conn, key_l+2)
        print(f'Key recived: {key}')
        #
        msg_len = take_input(conn)
        msg_l = int(msg_len[1])
        msg = take_input(conn, msg_l+2)
        print(f' The message recvd {msg} with key {key}')
        KEYS[key] = msg
        if length > 2:
            px_l = int(take_input(conn)[1]) + 2 #Will take the lenght of PX
            print(f'Length of PX {px_l}')
            px = take_input(conn, px_l)#Will take the command PX
            print(f'Command of PX {px}')
            time_l = int(take_input(conn)[1]) + 2#Will take the lenght of next number
            print(f'Length of expiry time {time_l}')
            exp = int(take_input(conn, time_l)[:time_l-2])#Take the expiry time
            print(f'Expiry time of PX {exp}')
            length -= 2            
            thrd2 = threading.Thread(target=expiry_time, args=(exp, key))
            thrd2.start()
            # expiry_time(conn)
        for i in KEYS:
            print(f'Key {i} Message Stored {KEYS[i]}')
        conn.send("+OK\r\n".encode(ENCODING))
        return length

def cmd_get(conn):
    print("GET COMMAND ENTERED")
    key_len = take_input(conn)
    key_l = int(key_len[1])
    key = take_input(conn,key_l+2)
    print(f'Key recived: {key}')
    print('SEARCHING IN KEYS')
    if key in KEYS.keys():
        print('KEY FOUND')
        print(f'Value sent {KEYS[key]}')
        len_msg = len(KEYS[key]) - 2
        msg = KEYS[key]
        msg = '$' + str(len_msg) + '\r\n' + str(msg)
        conn.send(msg.encode(ENCODING))
    else:
        print('KEY NOT FOUND')
        conn.send("$-1\r\n".encode(ENCODING))

def take_input(conn, n=4):
    return conn.recv(n).decode(ENCODING)

def expiry_time(exp, key):
    exp = float(exp)
    exp = exp/1000.00
    time.sleep(exp)
    KEYS.pop(key)




if __name__ == "__main__":
    main()
