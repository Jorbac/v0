from interpretor.py import interpretor

class evaluator:
	def __init__(self,ip,port):
		self.itp=interpretor(ip,port)
	def evaluate(org,s,a,o):
		#get role list
		r=itp.
		



if __name__=="__main__":
	itp=interpretor('localhost',27017)
#Major entities and administrative views are all represented as collections 
	collections=[]
	R='role'
	A="activity"
	V="view"
	s="subject"
	a="action"
	o="object"
	c="context"
	t="org"
	ro="R_Org"
	ao="A_Org"
	vo="V_Org"
	soo="so_Org"
	sro="s_R_Org"
	aao="a_A_Org"
	ovo="o_V_Org"
	lic="license"
	collections.append(R)
	collections.append(A)
	collections.append(V)
	collections.append(s)
	collections.append(a)
	collections.append(o)
	collections.append(c)
	collections.append(t)
	collections.append(ro)
	collections.append(ao)
	collections.append(vo)
	collections.append(sro)
	collections.append(aao)
	collections.append(ovo)
	collections.append(lic)

	itp.cleanAllCollection(collections)

	itp.insertObject(R,"user")
	itp.insertObject(A,"manange")
	itp.insertObject(V,"resource")
	itp.insertObject(s,"John")
	itp.insertObject(a,"create")
	itp.insertObject(a,"delete")
	itp.insertObject(o,"vm")
	itp.insertObject(t,"org1")
	itp.insertObject(c,"norminal")
	itp.insertObject(lic,"first",{'issuer':'org1', 'auth':'org1','grantee':'user','privilege':'manage','target':'resource'})
	itp.insertObject(sro,"john",{'issuer':'org1','auth':'org1','subject':"John",'role':'user'})
	itp.insertObject(aao,"a1",{'issuer':'org1','auth':'org1','action':'create','activity':'manange'})
	itp.insertObject(aao,"a2",{'issuer':'org1','auth':'org1','action':'delete','activity':'manange'})
	itp.insertObject(ovo,"b1",{'issuer':'org1','auth':'org1','object':'vm','activity':'resource'})
	print itp.db.object.find()
