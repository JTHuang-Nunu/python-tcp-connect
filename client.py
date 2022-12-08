import socket

HOST = "127.0.0.1"
# HOST = "192.168.1.115"
PORT = 7000

server = (HOST, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server)

end = "q"
while True:
    print("===================")
    print("Mode 1 for manual")
    print("Mode 2 for auto read txt file")
    print("q for exit")
    mode = input("Mode :")

    if mode == end:
        print("Quit calling~")
        print("Connection close!")
        s.send(end.encode())
        s.close()
        break
    elif mode == "1":
        s.send(mode.encode())
        while True:
            output = input("Enter your formula(enter q to stop looping)\n")
            if output == end:
                s.send(output.encode())
                print("Quit mode 1~")
                break
            else:
                s.send(output.encode())
                result = s.recv(1024)
                result = result.decode('utf-8')
                print("Received from server -> ", result)
    elif mode == "2":
        s.send(mode.encode())
        try:
            f = open("Testcase.txt", "r")
            for line in f.readlines():
                line.strip()
                s.send(line.encode())
                s.recv(1024)  # ???
            f.close()

        except:
            print("File not found")

        s.send(end.encode())
        print("Quit mode 2~")
