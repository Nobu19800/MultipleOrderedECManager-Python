# -*- coding: utf-8 -*-
import struct
import OpenRTM_aist
import os.path
import sys
import imp


class add_Rule:
    def __init__(self):
        self.state = -1
        self.name = ""
        self.r = None

class sub_Rule:
    def __init__(self):
        self.v = ""
        self.r = None
        self.s = 0

class Rule:
    def __init__(self):
        self.SR = []

class main_Rule:
    def __init__(self):
        self.rs = []
        self.ar = []

def ReadString(ifs):
    s = struct.unpack("i",ifs.read(4))[0]
    a = ifs.read(s)

    return a

def WriteString(a, ofs):
    
    a2 = a + "\0"
    s = len(a2)
    
    d = struct.pack("i", s)
    ofs.write(d)
    
    ofs.write(a2)

def LoadSRule(cs, nm, r):
    
    flag = True
    while(flag):
		
        SR = []

        
		
	nm = LoadSubRule(cs, nm, SR)

	

	

	r.SR.append(SR)

		
	nm = nm + 1

	

	
	    
	if cs[nm] == "}":
            flag = False
	    return nm
		


def LoadHRule(cs, nm, rs):
    flag = True;
    while(flag):
	r = Rule()
	
	while(True):
			
	    if cs[nm] == "{":
		break
	    elif(cs[nm] == "}"):
		return nm
	    else:
                nm = nm + 1
        
	    


	nm = nm + 1
		
        
	nm = LoadSRule(cs,nm,r)
	rs.append(r)

	nm = nm + 1

	
	    
	if cs[nm] == "}":
            flag = False;
	    return nm





def LoadAddRule(cs, nm, ar):
	
    flag = True;
    while(flag):
	ae = add_Rule()
	ae.name = cs[nm]
		
	nm = nm + 1

	
		
	if cs[nm] == "なし":
	    ae.state = -1
	elif cs[nm] == "CREATED":
	    ae.state = OpenRTM_aist.RTC.CREATED_STATE
	elif cs[nm] == "INACTIVE":
	    ae.state = OpenRTM_aist.RTC.INACTIVE_STATE
	elif cs[nm] == "ACTIVE":
	    ae.state = OpenRTM_aist.RTC.ACTIVE_STATE
	elif cs[nm] == "ERROR":
	    ae.state = OpenRTM_aist.RTC.ERROR_STATE
		
		
	
	
	ar.append(ae)

	nm = nm + 1

        
	
		
	if cs[nm] == ";":
	    flag = False
	    return nm
	elif cs[nm] == "}":
	    flag = False
	    return nm
		
		


def LoadSubRule(cs, nm, sr):
    flag = True
    while(flag):
        rs = sub_Rule()
		
	rs.v = cs[nm]
	    
	sr.append(rs)
	

	nm = nm + 1

	

	
	    
	if cs[nm] == ";":
            flag = False
	    return nm
	elif cs[nm] == "}":
            flag = False;
	    return nm


def LoadMainRule(rs, fName):

    root, ext = os.path.splitext(fName)
    

    if ext == ".py":
        try:
            pathName = os.path.dirname(fName)
            fileName = os.path.basename(root)
            
            (file, pathname, description) = imp.find_module(fileName,[pathName])
            plugin = imp.load_module(fileName, file, pathname, description)
            Ls = plugin.CompList
            for h in range(0, len(Ls)):
                R = main_Rule()
                for i in range(0, len(Ls[h][0])):
                    ar = add_Rule()
                    ar.name = Ls[h][0][i][0]
                    ar.state = Ls[h][0][i][1]
                    
                    R.ar.append(ar)
                for i in range(0, len(Ls[h][1])):
                    r = Rule()
                    
                    for j in range(0, len(Ls[h][1][i])):
                        
                        SRs = []
                        for k in range(0, len(Ls[h][1][i][j])):
                            SR = sub_Rule()
                            SR.v = Ls[h][1][i][j][k]
                            SR.s = 0
                            SRs.append(SR)
                        r.SR.append(SRs)
                    R.rs.append(r)
                rs.append(R)
        except ImportError:
            return False


    else:
        try:
            infile = open(fName, 'rb')
        except:
            return False
        

        Type = 0
        while True:
            c = infile.read(1)
            if c =="":
                break
            c = struct.unpack("b",c)[0]
            if c == 0x00:
                Type = 1
                
        infile.seek(0)





        if Type == 0:
            infile.close
            try:
                infile = open(fName)
            except:
                return False
            line = infile.readline()

            cs = []

            while line:
                lines1 = line
                lines1 = lines1.replace("\t","")
                lines1 = lines1.replace("\n","")
                lines1 = lines1.split(' ')
                for d in lines1:
                    if d != "":
                        cs.append(d)
                line = infile.readline()
            infile.close

            nm = 0
            while(len(cs) > nm):
                if cs[nm] == "{":
                    mr = main_Rule()

                    while(True):
                        nm = nm + 1
                        if cs[nm] == "{":
                            break
                    nm = nm + 1

            
                                    
                    nm = LoadAddRule(cs, nm, mr.ar)
            

            
                                    

                    while True:
                
                        nm = nm + 1
                        
                        if cs[nm] == "{":
                            break
            
            
                    nm = nm + 1



                    nm = LoadHRule(cs, nm, mr.rs)

            

                    while True:
                        nm = nm + 1
                            
                        if cs[nm] == "}":
                            break
            
                    nm = nm + 1
                    rs.append(mr)
        else:
            m = struct.unpack("i",infile.read(4))[0]
            for h in range(0, m):
                R = main_Rule()
                w = struct.unpack("i",infile.read(4))[0]
                for i in range(0, w):
                    ar = add_Rule()
                    ar.name = ReadString(infile)
                    ar.name = ar.name.replace("\0","")
                    

                    a_t = struct.unpack("i",infile.read(4))[0]

                    
                    
                    a_v = -1
                    if a_t == -1:
                        a_v = -1
                    elif a_t == 0:
                        a_v = OpenRTM_aist.RTC.CREATED_STATE
                    elif a_t == 1:
                        a_v = OpenRTM_aist.RTC.INACTIVE_STATE
                    elif a_t == 2:
                        a_v = OpenRTM_aist.RTC.ACTIVE_STATE
                    elif a_t == 3:
                        a_v = OpenRTM_aist.RTC.ERROR_STATE
                        
                    ar.state = a_v

                    R.ar.append(ar)
                c = struct.unpack("i",infile.read(4))[0]
                
                for i in range(0, c):
                    r = Rule()
                    d = struct.unpack("i",infile.read(4))[0]

                    

                    for j in range(0, d):
                        e = struct.unpack("i",infile.read(4))[0]
                        
                        SRs = []
                        

                        for k in range(0, e):
                            
                            SR = sub_Rule()
                            SR.v = ReadString(infile)
                            
                            SR.v = SR.v.replace("\0","")
                            
                            SR.s = 0
                            SRs.append(SR)
                        r.SR.append(SRs)
                    R.rs.append(r)
                rs.append(R)
                

                     




        infile.close()

    return True
