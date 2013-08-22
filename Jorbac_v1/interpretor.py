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
		cursor=self.client[tenant][view].find(expression)
		result=[]
		for ob in cursor:
			result.append(ob)
		return result

	def readOneObject(self,tenant,view,expression):
		return self.client[tenant][view].find_one(expression)

	#check if such object exists
	def hasObject(self,tenant,view,expression):
		return not(self.client[tenant][view].find(expression).limit(1).count()==0)

	#reinitialize a single collection or whole db
	def cleanView(self,tenant,view):
		return self.client[tenant][view].remove()
	def cleanAllCollection(self,tenant):
		allView=self.client[tenant].collection_names()
		for v in allView:
			if v!='system.indexes':
				self.client[tenant][v].remove() 		


