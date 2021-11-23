import socket
import sys

def rs(argv):
    if len(argv) != 2:
        print("[RS]: Please enter arguements: rsListenPort tsHostname")
        return
    
    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    
    rsListenPort = int(argv[0])
    tsHostname = str(argv[1])

    server_binding = ('', rsListenPort)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[RS]: host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[RS]: IP address is {}".format(localhost_ip))

    input = open('PROJI-DNSRS.txt', 'r')
    Lines = input.readlines()
    hostnameMap = generateMap(Lines)

    while True:
        cs, addr = ss.accept()
        print ("[RS]: Got a connection request from a client at {}".format(addr))
        
        while True:
            # recieve hostname from client
            try:
                hostname = cs.recv(4096).decode('utf-8')
            except:
                cs.close()
                break
            print ("[RS]: recieved host from client: {}".format(hostname))

            # process hostname
            res = hostnameMap.get(hostname, ['-', 'NS'])
            if res[1] == 'NS':
                hostname = tsHostname

            print('[RS]: sending ' + (hostname + ' ' + res[0] + ' ' + res[1]))
            
            # send response to client
            try:
                cs.send((hostname + ' ' + res[0] + ' ' + res[1]).encode('utf-8'))
            except:
                cs.close()
                break

    # close the server socket
    print ("[RS]: Server shutting down.")
    cs.close()
    exit()


def generateMap(Lines):
    Dict = {}
    for line in Lines:
        line = line.strip().lower()
        tokens = line.split()
        Dict[tokens[0]] = [tokens[1], tokens[2].upper()]

    return Dict

    

if __name__ == "__main__":
    rs(sys.argv[1:])