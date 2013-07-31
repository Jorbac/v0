from interpretor import interpretor
class configurer:
	def __init__(self,itp):
		self.itp=itp

	#Action to use an object in a view
	#attention, a constraint on view is not added yet, this constraint should check if a view exists in the view collection before adding anything into this view

	def Use(self,issuer,tenant,obj,view):
		self.itp.insertObject(tenant,view,obj['_id'],obj['attr'],issuer)
	#Action to unuse an object in a view
	def Unuse(self,tenant,identifier,view):
		self.itp.deleteObject(tenant,view,identifier)

	def CreateTenant(self,issuer,tenantName):
		self.Use(issuer,'TenantDB',{'_id':tenantName,'attr':{}},'tenant')
	def TenantHierarchy(self,issuer,tenantA,tenantB):
		flag=self.itp.hasObject('TenantDB','tenant',{'_id':tenantA}) and self.itp.hasObject('TenantDB','tenant',{'_id':tenantB})
		if flag==True:
			self.Use(issuer,'TenantDB',{'_id':'_'.join([tenantA,tenantB]),'attr':{'parent':tenantA,'child':tenantB}},'tenant_hierarchy')
		else:
			print "Tenant A or Tenant B does not exist"


	#assign subject,action,object,role,activity,view to a tenant
	def AssignSubject(self,issuer,tenant,obj):
		self.Use(issuer,tenant,obj,'subject')
	def AssignAction(self,issuer,tenant,obj):
		self.Use(issuer,tenant,obj,'action')
	def AssignObject(self,issuer,tenant,obj):
		self.Use(issuer,tenant,obj,'object')
	def AssignRole(self,issuer,tenant,obj):
		self.Use(issuer,tenant,obj,'role')
	def AssignActivity(self,issuer,tenant,obj):
		self.Use(issuer,tenant,obj,'activity')
	def AssignView(self,issuer,tenant,obj):
		self.Use(issuer,tenant,obj,'view')
	def AssignContext(self,issuer,tenant,obj):
		self.Use(issuer,tenant,obj,'context')
		#need to create a collection for it?
	#corresponding unassign actions
	def UnassignSubject(self,tenant,identifier):
		self.Unuse(tenant,identifier,'subject')
	def UnassignAction(self,tenant,identifier):
		self.Unuse(issuer,identifier,'action')
	def UnassignObject(self,tenant,identifier):
		self.Unuse(tenant,identifier,'object')
	def UnassignRole(self,tenant,identifier):
		self.Unuse(tenant,identifier,'role')
	def UnassignActivity(self,tenant,identifier):
		self.Unuse(issuer,tenant,identifier,'activity')
	def UnassignView(self,tenant,identifier):
		self.Unuse(tenant,identifier,'view')
	def UnassignContext(self,tenant,identifier):
		self.Unuse(tenant,identifier,'context')

	#role,activity assignment
	def Empower(self,issuer,tenant,subject,role):
		flag=self.itp.hasObject(tenant,'subject',{'_id':subject}) and self.itp.hasObject(tenant,'role',{'_id':role})
		if flag==True:
			self.Use(issuer,tenant,{'_id':'_'.join([subject,role]),'attr':{'subject':subject,'role':role}},'role_assignment')
		else:
			print "error: no such subject or role in the tenant"

	def Consider(self,issuer,tenant,action,activity):
		flag=self.itp.hasObject(tenant,'action',{'_id':action}) and self.itp.hasObject(tenant,'activity',{'_id':activity})
		if flag==True:
			self.Use(issuer,tenant,{'_id':'_'.join([action,activity]),'attr':{'action':action,'activity':activity}},'activity_assignment')
		else:
			print "error: no such action or activity in the tenant"

	#corresponding role,activity unassignment
	def Unempower(self,tenant,subject,role):
		self.Unuse(tenant,'_'.join([subject,role]),'role_assignment')
	def Unconsider(self,tenant,action,activity):
		self.Unuse(tenant,'_'.join([action,activity]),'activity_assignment')

	#permission assignment, for now we do not use multi-grainularity licence
	def Permission(self,issuer,permission_name,tenant,role,activity,view,context):
		flag=self.itp.hasObject(tenant,'role',{'_id':role}) and self.itp.hasObject(tenant,'activity',{'_id':activity}) and self.itp.hasObject(tenant,'view',{'_id':view}) and self.itp.hasObject(tenant,'context',{'_id':context})
		if flag==True:
			self.Use(issuer,tenant,{'_id':permission_name,'attr':{'role':role,'activity':activity,'view':view,'context':context}},'licence')	
		else:
			print "error: in permission, no role/activity/view or context"

	#permission unassignment
	def Unpermission(self,tenant,permission_name):
		self.Unuse(tenant,permission_name,'licence')

	#produce concrete rules
	def ProduceConcreteRule(self,tenant):
		itp=self.itp
		for licence in itp.readObject(tenant,'licence',{}):
			r=licence['attr']['role']
			a=licence['attr']['activity']
			v=licence['attr']['view']
			context=licence['attr']['context']
			for ra in itp.readObject(tenant,'role_assignment',{'attr.role':r}):
				for aa in itp.readObject(tenant,'activity_assignment',{'attr.activity':a}):
					for va in itp.readObject(tenant,v,{}):
						subject_name=ra['attr']['subject']
						action_name=aa['attr']['action']
						object_name=va['_id']
						#print '_'.join([subject_name,action_name,object_name,context])
						self.Use(tenant,tenant,{'_id':'_'.join([subject_name,action_name,object_name,context]),'attr':{'subject':subject_name,'action':action_name,'object':object_name,'context':context}},'concrete_rules')
					

if __name__=="__main__":
	itp=interpretor('localhost',27017)
	config=configurer(itp)
	config.Use('tenant','tenant',{'_id':'a3','attr': {}},'action')

		