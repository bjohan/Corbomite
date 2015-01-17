import IbasicInterface
import Hp8922mScope
import time
import csv
ibas = IbasicInterface.IbasicInterface()
scope = Hp8922mScope.Hp8922mScope(ibas)
print "init done"
for i in range(10):
    output = scope.readTrace()
    print output
    w = csv.writer(open('data.csv', 'w'))
    w.writerow(output)
del ibas
del scope
