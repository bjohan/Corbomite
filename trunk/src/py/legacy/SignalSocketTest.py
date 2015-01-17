import SignalSocket
print "Creating sockets"
sa = SignalSocket.SignalSocket()
sb = SignalSocket.SignalSocket()

with sa:
    print "Adding sb as forward socket to sa"
    sa.AddForwardSocket(sb)

    print "Samples in a and b:"
    print "sa:", sa.GetEndSamplesByNumber(2)
    print "sb:", sb.GetEndSamplesByNumber(2)

    print "Adding one sample with value 1 in socket a"
    sa.AddSample(1)
    print "Samples in a and b"
    print "sa:", sa.GetEndSamplesByNumber(4)
    print "sb:", sb.GetEndSamplesByNumber(4)

    print "Adding a sample with value 2 in socket a"
    sa.AddSample(2)
    print "Samples in a and b"
    print "sa:", sa.GetEndSamplesByNumber(4)
    print "sb:", sb.GetEndSamplesByNumber(4)

    print "Adding a sample with value 3 in socket b"
    sb.AddSample(3)
    print "Samples in a and b"
    print "sa:", sa.GetEndSamplesByNumber(4)
    print "sb:", sb.GetEndSamplesByNumber(4)
