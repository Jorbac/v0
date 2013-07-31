import pymongo
class interpretor:
	def __init__(self,ip,port):
		self.ip=ip
		self.port=port
		self.client=pymongo.MongoClient(ip,port)
        def insertObject(self,tenant,view,identifier,attr,usedBy):
		"""we assume that identifier is unique
		attr is a dictionary that stores some static attributes of the object """
		obj={"_id":identifier,
		     "attr":attr,
		     "usedBy":usedBy
		     }
		db=self.client[tenant][view].save(obj)
	def deleteObject(self,tenant,view,identifier):
		self.client[tenant][view].remove({'_id':identifier})
		
	def readObject(self,tenant,view,expression):
		return self.client[tenant][view].find(expression)

	def readOneObject(self,tenant,view,expression):
		return self.client[tenant][view].find_one(expression)

	#check if such object exists
	def hasObject(self,tenant,view,expression):
		return not(self.client[tenant][view].find(expression).limit(1).count()==0)
	def cleanView(self,tenant,view):
		return self.client[tenant][view].remove()
	def cleanAllCollection(self,tenant,allView):
		for v in allView:
			self.client[tenant][v].remove() 		

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
	conc="concrete_rule"
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
	collections.append(conc)
	itp.cleanAllCollection('tenant',collections)

	itp.insertObject('tenant',R,"user",{},'tenant')
	itp.insertObject('tenant',A,"manange",{},'tenant')
	itp.insertObject('tenant',V,"resource",{},'tenant')
	itp.insertObject('tenant',s,"John",{},'tenant')
	itp.insertObject('tenant',a,"create",{},'tenant')
	itp.insertObject('tenant',a,"delete",{},'tenant')
	itp.insertObject('tenant',o,"vm",{},'tenant')
	itp.insertObject('tenant',t,"org1",{},'tenant')
	itp.insertObject('tenant',c,"norminal",{},'tenant')
	itp.insertObject('tenant',lic,"first",{'issuer':'org1', 'auth':'org1','grantee':'user','privilege':'manage','target':'resource'},'tenant')
	itp.insertObject('tenant',sro,"john",{'issuer':'org1','auth':'org1','subject':"John",'role':'user'},'tenant')
	itp.insertObject('tenant',aao,"a1",{'issuer':'org1','auth':'org1','action':'create','activity':'manange'},'tenant')
	itp.insertObject('tenant',aao,"a2",{'issuer':'org1','auth':'org1','action':'delete','activity':'manange'},'tenant')
	itp.insertObject('tenant',ovo,"b1",{'issuer':'org1','auth':'org1','object':'vm','activity':'resource'},'tenant')
	print itp.hasObject('tenant',a,{"identifier":"ddfd"})
	print itp.client.tenant.object.find()

