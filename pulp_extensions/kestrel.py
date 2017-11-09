import time
import xmlrpc.client
import sys
import os
path=os.getcwd()
path+='/'
import lxml.etree
import lxml.builder 
from .tempmail import TempMail

class Kestrel(object):
    """docstring fo kestrel."""
    def __init__(self, problem, ptype, maximize=None, email=None, priority=None, path=path):
        super(Kestrel, self).__init__()
        self.problem = problem
        self.path=path
        self.ptype = ptype
        if maximize:
            self.maximize=maximize
        else:
            self.maximize="no"
        if email:
            self.email=email
        else:
            tm=TempMail()
            self.email=tm.get_email_address()
        if priority:
            self.priority=priority
        else:
            self.priority='long'
    def lptoxml(self):
        self.problem.writeMPS("problem.mps")
        file = open(self.path+'problem.mps', "r")
        E = lxml.builder.ElementMaker()
        root=E.document
        field1=E.category
        field2=E.solver
        field3=E.inputMethod
        field4=E.MPS
        field5=E.maximize
        field6=E.nosol
        field7=E.email
        field8=E.priority
        xmldoc=root(
                    field1(self.ptype),
                    field2("FICO-Xpress"),
                    field3("MPS"),
                    field4(lxml.etree.CDATA(file.read())),
                    field5(self.maximize),
                    field6("no"),
                    field7(self.email),
                    field8(self.priority))
        xml=lxml.etree.tostring(xmldoc).decode()
        file.close()
        try:
            os.remove(self.path+'problem.mps')
        except:
            pass
        return xml
    def solve(self):
        xml=self.lptoxml()
        neos = xmlrpc.client.ServerProxy("https://neos-server.org:3333")
        alive = neos.ping()
        if alive!="NeosServer is alive\n":
            print("Could not make connection to NEOS Server")
            sys.exit(1)
        else:
            (jobNumber, password) = neos.submitJob(xml)
            print("Job number = %d Job password = %s" % (jobNumber, password))
            if jobNumber == 0:
                print("NEOS Server error: %s" % password)
                sys.exit(1)
            else:
                #offset=0
                status=""
                while status!="Done":
                    time.sleep(5)
                    #(msg, offset)=neos.getIntermediateResults(jobNumber, password, offset)
                    #print(msg.data.decode())
                    status= neos.getJobStatus(jobNumber, password)
                    print('Solving... Problem status: ', status)
                msg=neos.getFinalResults(jobNumber, password)
                print(msg.data.decode())
        
        
        
        

            
        
        








