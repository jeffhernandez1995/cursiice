import time
import xmlrpc.client
import sys
import os
path=os.getcwd()
path+='/'
import lxml.etree
import lxml.builder 
from .tempmail import TempMail
from pulp.solvers import LpSolver_CMD
from pulp.solvers import PulpSolverError
from pulp.constants import *

class Kestrel(LpSolver_CMD):
    """
    API Wrapper for Neos Solver XML-RPC API. Compatible with pulp linear programming api.
    Only Xpress solver works; in the future more solvers will be added
    :param ptype: problem type for example 'milp': mixed integer linear programming
    olny tested with 'milp', 'lp'
    :param maximize: 'yes' or 'no' to maximize or minimize respectibly
    :param email: (Controversial) gets temporal email address to use with solver; it is possible
    to specify a custom adress for example 'someone@email.com'
    :param priority: default 'long', if 'short' is scpecified job will be killed after 5 min
    :param path: (optional) path to store temporal files
    :param  keepFiles = 0, mip = 1, msg = 0, options = []: neccesary to make LpSolver_CMD  work
    """
    def __init__(self, ptype, maximize=None, email=None, priority=None, path=path, keepFiles = 0, mip = 1, msg = 0, options = []):
        #super(Kestrel, self).__init__()
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
        LpSolver_CMD.__init__(self, path, keepFiles, mip, msg, options)

    def defaultPath(self):
        return self.path

    def copy(self):
        """Make a copy of self"""
        aCopy = LpSolver_CMD.copy(self)
        aCopy.cuts = self.cuts
        aCopy.presolve = self.presolve
        aCopy.dual = self.dual
        aCopy.strong = self.strong
        return aCopy

    def actualSolve(self, lp, **kwargs):
        """Solve a well formulated lp problem"""
        return self.solve_Kestrel(lp, **kwargs)

    def available(self):
        """True if the solver is available"""
        neos = xmlrpc.client.ServerProxy("https://neos-server.org:3333")
        alive = neos.ping()
        if alive!="NeosServer is alive\n":
            print("Could not make connection to NEOS Server")
            avlble=False
        else:
            avlble=True
        return avlble

    def solve_Kestrel(self, lp):
        vs=lp.writeMPS(self.path+"problem.mps",rename = 0)
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
                #print(msg.data.decode())
                tmpSol=open(self.path+'tmpSol.txt', 'w')
                tmpSol.write(msg.data.decode())
                tmpSol.close()
        values= self.readsol_MPS(self.path+'tmpSol.txt')
        #print(values)
        try:
            os.remove(self.path+'tmpSol.txt')
        except:
            pass
        kestrelStatus = {"Done":LpStatusOptimal}
        if status not in kestrelStatus:
            raise PulpSolverError("Unknown status returned by Kestrel: "+statusString)
        lp.status=kestrelStatus[status]
        lp.assignVarsVals(values)
        return lp.status
    def readsol_MPS(self, filename):
        with open(filename,'r') as f:
            values = {}
            while 1:
                l = f.readline()
                if l == "": break
                line = l.split()
                if len(line) and line[0] == 'C':
                    name = line[2]
                    value = float(line[4])
                    values[name] = value
        return values
        
