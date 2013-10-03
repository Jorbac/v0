class openstack:
	def __init__(self,itp,config,admin):
		self.itp=itp
		self.config=config
		self.admin=admin

	#***********************************************

	#*******************************************Produce OpenStack Rules from permissions in license view**********************
	def ProduceOpenStackRule(self,tenant):
		itp=self.itp
		for licence in itp.readObject(tenant,'licence',{}):
			r=licence['attr']['role']
			a=licence['attr']['activity']
			v=licence['attr']['view']
			context=licence['attr']['context']
			for aa in itp.readObject(tenant,'activity_assignment',{'attr.activity':a}):
				#insert a concrete permission to allow a subject to perform certain action on the "view" object
				action_name=aa['attr']['action']
				if action_name=='insert' or action_name=='delete':
					pass
				else:
					print "\""+action_name+"\": "+"[[\""+r+"\"]]\n"
					
		return 

