
import socket

def server():
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[S]: Server socket created")
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()

    server_binding = ('', 50007)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[S]: Server host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[S]: Server IP address is {}".format(localhost_ip))
    cs, addr = ss.accept()
    print ("[S]: Got a connection request from a client at {}".format(addr))

    while True:
        # recieve msg from client
        msg = cs.recv(1000).decode('utf-8')
        if not msg: break
        print ("[S]: recieved data from client: {}".format(msg))
        cs.send(reverse(msg).encode('utf-8'))

    # close the server socket
    print ("[S]: Server shutting down.")
    cs.close()
    exit()

def reverse(str):
    return str[::-1] + str


if __name__ == "__main__":
    server()