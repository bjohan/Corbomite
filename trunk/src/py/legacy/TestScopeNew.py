import IbasicInterface
import Hp8922mScopeNew
import HpIbasicMeasurementService
import time
import csv

ms = HpIbasicMeasurementService.HpIbasicMeasurementService()
#time.sleep(0.1)
#print "Changing screen"
#ms.ExecuteCommand("DISP:SCR OSC",3)
##time.sleep(0.1)
#print "Changing control"
#ms.ExecuteCommand("OSC:CONT MAIN",3)
#time.sleep(0.1)
#for i in range(1):
#	print "measuring"
#	ms.ExecuteCommand("MEAS:OSC:TRACE?",1)
#time.sleep(0.1)
sc = Hp8922mScopeNew.Hp8922mScope(ms)
sc.setVerticalScale('20 uV','INPUT')
for i in range(1):
	print sc.readTrace()

print "quitting"
ms.Quit()
#ibas = IbasicInterface.IbasicInterface()
#scope = Hp8922mScope.Hp8922mScope(ibas)
#print "init done"
#for i in range(10):
#	output = scope.readTrace()
#	print output
#	w = csv.writer(open('data.csv','w'))
#	w.writerow(output)
#del ibas
#del scope
