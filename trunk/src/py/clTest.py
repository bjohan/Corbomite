import com.tcpCommunication

cl = com.tcpCommunication.TcpClient()
cl.write("#info\r\n")
print cl.read()
cl.write("#tja\r\n")
print cl.read()
