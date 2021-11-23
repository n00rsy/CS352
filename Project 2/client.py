import socket
import sys

def client(argv):
    print(argv)
    if len(argv) != 3:
        print("[C]: Please enter arguements: rsHostname rsListenPort tsListenPort")
        return

    try:
        rs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ts_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('[C]: socket open error: {} \n'.format(err))
        exit()
    
    input = open('PROJI-HNS.txt', 'r')
    output = open('RESOLVED.txt', 'w')
    Lines = input.readlines()

    rsHostname = str(argv[0])
    rsListenPort = int(argv[1])
    tsListenPort = int(argv[2])

    localhost_addr = socket.gethostbyname(socket.gethostname())
    print("[C]: localhost: " + localhost_addr)

    # connect to root DNS
    rs_server_binding = (rsHostname, rsListenPort)
    rs_socket.connect(rs_server_binding)

    init = False

    for line in Lines:
        line = line.strip().lower()
        if len(line) > 0:
            print('[C]: sending ' + line)
            # send data to server
            rs_socket.send(line.encode('utf-8'))
            # rcv data from server 
            data_rs = rs_socket.recv(1000).decode('utf-8')
            print('[C]: recieved: ' + data_rs)
            tokens = data_rs.split()
            if (len(tokens) != 3):
                print("Error retrieving IP from root DNS.")
                continue
            
            if (tokens[2] == 'A'):
                output.write(tokens[0] + " " + tokens[1]  + "\n")
            elif tokens[2] == 'NS':
                if not init:
                    tsHostName = tokens[0]
                    ts_server_binding = (tsHostName, tsListenPort)
                    ts_socket.connect(ts_server_binding)
                    init = True

                # send data to TS
                ts_socket.send(line.encode('utf-8'))

                # rcv data from TS 
                data_ts = ts_socket.recv(1000).decode('utf-8')
                if "Error" in data_ts:
                    continue
                else:
                    output.write(data_ts + '\n')
            
            else:
                print('[C]: unexpected response from server.')

    # close the client socket
    print("[C]: Client shutting down.")
    rs_socket.close()
    ts_socket.close()
    input.close()
    output.close()
    exit()


if __name__ == "__main__":
    client(sys.argv[1:])