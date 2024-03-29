import socket


class TcpServer:
    def __init__(self, ifAddrToBind='127.0.0.1', port=8472):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((ifAddrToBind, port))
        self.s.listen(1)
        self.accept()

    def accept(self):
        print("Waiting for connection")
        self.conn, self.remoteAddr = self.s.accept()

    def read(self):
        data = self.conn.recv(1024)
        if len(data) == 0:
            self.accept()
            return self.read()
        # print "TCP got data", data
        return data

    def write(self, data):
        # print "TCP sending data", data
        self.conn.send(data)

    def __del__(self):
        print("Freeing socket")
        self.conn.close()


class TcpClient:
    def __init__(self, destAddr='127.0.0.1', port=8472):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((destAddr, port))
        self.port = destAddr  # Ugly, but when notebook tab is created in gui
        # the port member is used as name. FIXME later

    def read(self):
        data = self.s.recv(1024)
        # print "TCP got", data
        return data

    def write(self, data):
        self.s.send(data)

    def __del__(self):
        # print "Freeing socket"
        self.s.close()
