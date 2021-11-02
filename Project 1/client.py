import socket

def client():
    try:
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
    
    input = open('in-proj0.txt', 'r')
    output = open('out-proj0.txt', 'w')
    Lines = input.readlines()

    # Define the port on which you want to connect to the server
    port = 50007
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to the server on local machine
    server_binding = (localhost_addr, port)
    cs.connect(server_binding)


    for line in Lines:
        line = line.strip()
        if len(line) > 0:
            # send data to server
            print("[C]: Data sent to server: {}".format(line))
            cs.send(line.encode('utf-8'))
            # rcv data from server 
            data_from_server=cs.recv(1000).decode('utf-8')
            print("[C]: Data received from server: {}".format(data_from_server))
            output.write(data_from_server + '\n')

    # close the client socket
    print("[C]: Client shutting down.")
    cs.close()
    input.close()
    output.close()
    exit()


if __name__ == "__main__":
    client()