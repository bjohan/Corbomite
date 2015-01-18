import common.tcpCommunication

cl = common.tcpCommunication.TcpClient()
cl.write("#info\r\n")
print cl.read()
cl.write("#tja\r\n")
print cl.read()
