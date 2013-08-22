from interpretor import interpretor
class configurer:
	def __init__(self,itp):
		self.itp=itp

	#Action to use an object in a view
	def Use(self,issuer,tenant,obj,view):
		self.itp.insertObject(tenant,view,obj['_id'],obj['attr'],issuer)

	#Action to unuse an object in a view
	def Unuse(self,issuer,tenant,identifier,view):

		self.itp.deleteObject(tenant,view,identifier)
	


	#evaluate if a tenant is superior than another tenant
	def Dominance(self,tenantA,tenantB):
		return tenantA==tenantB or self.itp.hasObject('TenantDB','tenant_hierarchy',{'attr.parent':tenantA,'attr.child':tenantB})



	#create a tenant and assign it to a hierarchy
	def CreateTenant(self,issuer,tenantName):
		self.Use(issuer,'TenantDB',{'_id':tenantName,'attr':{}},'tenant')
	def TenantHierarchy(self,issuer,tenantA,tenantB):
		flag=self.itp.hasObject('TenantDB','tenant',{'_id':tenantA}) and self.itp.hasObject('TenantDB','tenant',{'_id':tenantB})
		if flag==True:
			self.Use(issuer,'TenantDB',{'_id':'_'.join([tenantA,tenantB]),'attr':{'parent':tenantA,'child':tenantB}},'tenant_hierarchy')
		else:
			print "Tenant A or Tenant B does not exist"

	#delete a tenant and remove it from an hierarchy
	def DeleteTenant(self,issuer,tenantName):
		self.UnUse(issuer,'TenantDB',tenantName,'tenant')
		#remove from hierarchy not implemented yet
	def UnTenantHierarchy(self,issuer,tenantA,tenantB):
		self.UnUse(issuer,'TenantDB','_'.join([tenantA,tenantB]),'tenant_hierarchy')



	#assign role,activity,view to a tenant
	def AssignRole(self,issuer,tenant,obj):
		self.Use(issuer,tenant,obj,'role')
	def AssignActivity(self,issuer,tenant,obj):
		self.Use(issuer,tenant,obj,'activity')
	def AssignView(self,issuer,tenant,obj):
		self.Use(issuer,tenant,obj,'view')
	def AssignContext(self,issuer,tenant,obj):
		self.Use(issuer,tenant,obj,'context')

	#corresponding unassign actions
	def UnassignRole(self,issuer,tenant,identifier):
		self.Unuse(issuer,tenant,identifier,'role')
	def UnassignActivity(self,issuer,tenant,identifier):
		self.Unuse(issuer,tenant,identifier,'activity')
	def UnassignView(self,issuer,tenant,identifier):
		self.Unuse(issuer,tenant,identifier,'view')
	def UnassignContext(self,issuer,tenant,identifier):
		self.Unuse(issuer,tenant,identifier,'context')

	#role,activity assignment
	def Empower(self,issuer,tenant,subject,role):
		flag=self.itp.hasObject(tenant,'role',{'_id':role})
		if flag==True:
			self.Use(issuer,tenant,{'_id':'_'.join([subject,role]),'attr':{'subject':subject,'role':role}},'role_assignment')
		else:
			print "error: no such subject or role in the tenant"

	def Consider(self,issuer,tenant,action,activity):
		flag=self.itp.hasObject(tenant,'activity',{'_id':activity})
		if flag==True:
			self.Use(issuer,tenant,{'_id':'_'.join([action,activity]),'attr':{'action':action,'activity':activity}},'activity_assignment')
		else:
			print "error: no such action or activity in the tenant"

	#corresponding role,activity unassignment
	def Unempower(self,issuer,tenant,subject,role):
		self.Unuse(issuer,tenant,'_'.join([subject,role]),'role_assignment')
	def Unconsider(self,issuer,tenant,action,activity):
		self.Unuse(issuer,tenant,'_'.join([action,activity]),'activity_assignment')

	#permission assignment, for now we do not use multi-grainularity licence
	def Permission(self,issuer,permission_name,tenant,role,activity,view,context):
		flag=self.itp.hasObject(tenant,'role',{'_id':role}) and self.itp.hasObject(tenant,'activity',{'_id':activity}) and self.itp.hasObject(tenant,'view',{'_id':view}) and self.itp.hasObject(tenant,'context',{'_id':context})
		if flag==True:
			self.Use(issuer,tenant,{'_id':permission_name,'attr':{'role':role,'activity':activity,'view':view,'context':context}},'licence')	
		else:
			print "error: in permission, no role/activity/view or context"

	#permission unassignment
	def Unpermission(self,issuer,tenant,permission_name):
		self.Unuse(issuer,tenant,permission_name,'licence')


	#cross tenant permission, have one additional attribute in the licence, the target_tenant
	def Cross_Permission(self,issuer,permission_name,init_tenant,role,target_tenant,activity,target_view,context):
		flag=self.itp.hasObject(init_tenant,'role',{'_id':role}) and self.itp.hasObject(target_tenant,'view',{'_id':target_view}) and self.itp.hasObject(init_tenant,'context',{'_id':context})
		if flag==True:
			self.Use(issuer,init_tenant,{'_id':permission_name,'attr':{'role':role,'target_tenant':target_tenant,'mgmt_activity':activity,'target_view':target_view,'context':context}},'cross_licence')	
		else:
			print "error: in cross_permission, no init role or target /activity/view or context"

	#cross tenant unpermission
	def Cross_Unpermission(self,issuer,tenant,permission_name):
		self.Unuse(issuer,tenant,permission_name,'cross_licence')

	#produce concrete rules for cross_permission, since the cross permission only performs administrative actions, thus no need to enter in target view to get object
	def Cross_ProduceConcreteRule(self,tenant):
		itp=self.itp
		itp.cleanView(tenant,'cross_concrete_rules')
		for licence in itp.readObject(tenant,'cross_licence',{}):
			r=licence['attr']['role']
			a=licence['attr']['mgmt_activity']
			target=licence['attr']['target_tenant']
			v=licence['attr']['target_view']
			context=licence['attr']['context']
			for ra in itp.readObject(tenant,'role_assignment',{'attr.role':r}):
				for aa in itp.readObject(tenant,'activity_assignment',{'attr.activity':a}):
					#insert a concrete permission to allow a subject to perform certain action on the "view" object
					subject_name=ra['attr']['subject']
					action_name=aa['attr']['action']
					self.Use(tenant,tenant,{'_id':'_'.join([subject_name,action_name,target,v,context]),'attr':{'subject':subject_name,'action':action_name,'target':target,'object':v,'context':context}},'cross_concrete_rules')
		return 

	#produce concrete rules for permission
	def ProduceConcreteRule(self,tenant):
		itp=self.itp
		itp.cleanView(tenant,'concrete_rules')
		for licence in itp.readObject(tenant,'licence',{}):
			r=licence['attr']['role']
			a=licence['attr']['activity']
			v=licence['attr']['view']
			context=licence['attr']['context']
			for ra in itp.readObject(tenant,'role_assignment',{'attr.role':r}):
				for aa in itp.readObject(tenant,'activity_assignment',{'attr.activity':a}):
					#insert a concrete permission to allow a subject to perform certain action on the "view" object
					subject_name=ra['attr']['subject']
					action_name=aa['attr']['action']
					self.Use(tenant,tenant,{'_id':'_'.join([subject_name,action_name,v,context]),'attr':{'subject':subject_name,'action':action_name,'object':v,'context':context}},'concrete_rules')

					#if the "view" is administrative view, then we do not need to generate concrete rules that allow a subject to manage an object in the administrative view, we only need to specify that the subject can either "insert" or "delete" in this view, we thus skip the next loop that generate concrete rules for each object in the view
					if action_name=='insert' or action_name=='delete':
						pass
					else:
						for va in itp.readObject(tenant,v,{}):
							object_name=va['_id']
							#insert concrete permissions to allow a subject to perform certain action on objects in view
							self.Use(tenant,tenant,{'_id':'_'.join([subject_name,action_name,object_name,context]),'attr':{'subject':subject_name,'action':action_name,'object':object_name,'context':context}},'concrete_rules')

		return 
					

if __name__=="__main__":
	itp=interpretor('localhost',27017)
	config=configurer(itp)
	config.Use('tenant','tenant',{'_id':'a3','attr': {}},'action')

		
