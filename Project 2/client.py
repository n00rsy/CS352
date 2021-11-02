import socket
import sys

def client(argv):

    if len(argv) != 3:
        print("[C]: Please enter arguements: rsHostname rsListenPort tsListenPort")
        return

    try:
        rs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()
    
    input = open('PROJI-HNS.txt', 'r')
    output = open('RESOLVED.txt', 'w')
    Lines = input.readlines()

    rsListenPort = int(argv[1])
    tsListenPort = int(argv[2])
    localhost_addr = socket.gethostbyname(socket.gethostname())

    # connect to root DNS
    rs_server_binding = (localhost_addr, rsListenPort)
    rs_socket.connect(rs_server_binding)

    # connect to top-level DNS
    ts_server_binding = (localhost_addr, tsListenPort)
    ts_socket.connect(ts_server_binding)

    for line in Lines:
        line = line.strip().lower()
        if len(line) > 0:
            # send data to server
            rs_socket.send(line.encode('utf-8'))
            # rcv data from server 
            data_from_server=rs_socket.recv(1000).decode('utf-8')
            tokens = data_from_server.split(" ")
            if (len(tokens) != 3):
                print("Error retrieving IP from root DNS.")
                continue
            
            if (tokens[2] == 'A'):
                res = tokens[0] + " " + tokens[1]  + "\n"
                print(res)
                output.write(tokens[0] + " " + tokens[1]  + "\n")
            else:
                # send data to server
                ts_socket.send(line.encode('utf-8'))
                # rcv data from server 
                data_from_server=ts_socket.recv(1000).decode('utf-8')
                tokens = data_from_server.split(" ")
                if (len(tokens) != 3):
                    print("Error retrieving IP from root DNS.")
                    continue
                
                if (tokens[2] == 'A'):
                    print("URL: " + tokens[0] + "\tIP:" + tokens[1])
                    output.write(tokens[0] + " " + tokens[1]  + "\n")

        # close the client socket
        print("[C]: Client shutting down.")
        rs_socket.close()
        input.close()
        output.close()
        exit()


if __name__ == "__main__":
    client(sys.argv[1:])