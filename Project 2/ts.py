import socket
import sys

def ts(argv):
    if len(argv) != 1:
        print("[TS]: Please enter arguments: tsListenPort")
        return

    try:
        ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('socket open error: {}\n'.format(err))
        exit()
    
    tsListenPort = int(argv[0])

    server_binding = ('', tsListenPort)
    ss.bind(server_binding)
    ss.listen(1)
    host = socket.gethostname()
    print("[TS]: host name is {}".format(host))
    localhost_ip = (socket.gethostbyname(host))
    print("[TS]: IP address is {}".format(localhost_ip))
    cs, addr = ss.accept()
    print ("[TS]: Got a connection request from a client at {}".format(addr))

    input = open('PROJI-DNSTS.txt', 'r')
    Lines = input.readlines()
    hostnameMap = generateMap(Lines)

    print('[TS]: starting main loop')
    while True:
        hostname = cs.recv(4096)
        print("[TS]: Recieved a host to lookup {}".format(hostname))
        if hostname in hostnameMap:
            print("[TS]: Found host in TS")
            resp = hostname + ' ' + ' '.join(hostnameMap[hostname])
            print("[TS]: Sending client {}".format(resp))
            cs.send(resp.encode())
        else:
            # not in TS
            not_found_resp = host + ' - Error:HOST NOT FOUND'
            try:
                cs.send(not_found_resp.encode())
            except:
                ss.close()
                exit()

def generateMap(Lines):
    Dict = {}
    for line in Lines:
        line = line.strip().lower()
        tokens = line.split()
        Dict[tokens[0]] = [tokens[1], tokens[2]]

    return Dict


if __name__ == "__main__":
    ts(sys.argv[1:])