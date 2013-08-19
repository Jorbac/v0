from interpretor import interpretor
class configurer:
	def __init__(self,itp):
		self.itp=itp

	#****************************Assign Role,Activity,View to Tenant********************


	#assign role,activity,view to a tenant
	def AssignRole(self,issuer,tenant,obj):
		self.Use(issuer,obj,tenant,'role')
	def AssignActivity(self,issuer,tenant,obj):
		self.Use(issuer,obj,tenant,'activity')
	def AssignView(self,issuer,tenant,obj):
		self.Use(issuer,obj,tenant,'view')
	def AssignContext(self,issuer,tenant,obj):
		self.Use(issuer,obj,tenant,'context')

	#corresponding unassign actions
	def UnassignRole(self,issuer,tenant,identifier):
		self.Unuse(issuer,identifier,tenant,'role')
	def UnassignActivity(self,issuer,tenant,identifier):
		self.Unuse(issuer,identifier,tenant,'activity')
	def UnassignView(self,issuer,tenant,identifier):
		self.Unuse(issuer,identifier,tenant,'view')
	def UnassignContext(self,issuer,tenant,identifier):
		self.Unuse(issuer,identifier,tenant,'context')




	#********************Use an object in a (tenant,view)*******************************
	def Use(self,issuer,obj,tenant,view):
		#insert an object in the collection "view" of a tenant database, used by issuer
		self.itp.insertObject(tenant,view,obj['_id'],obj['attr'],issuer)
	#Action to unuse an object in a (tenant,view)
	def Unuse(self,issuer,identifier,tenant,view):
		#delete the object with _id=identifier in the collection "view" of a tenant database
		self.itp.deleteObject(tenant,view,identifier)


	#********************************Empower a subject in a (tenant,role)**********************************
	def Empower(self,issuer,subject,tenant,role):
		#verify if such role exists in tenant
		flag=self.itp.hasObject(tenant,'role',{'_id':role})
		if flag==True:
			self.Use(issuer,{'_id':'_'.join([subject,role]),'attr':{'subject':subject,'role':role}},tenant,'role_assignment')
		else:
			print "error: no such role in the tenant"

	def Unempower(self,issuer,subject,tenant,role):
		self.Unuse(issuer,'_'.join([subject,role]),tenant,'role_assignment')

	#********************************Consider an action in a (tenant,activity)****************************
	def Consider(self,issuer,action,tenant,activity):
		flag=self.itp.hasObject(tenant,'activity',{'_id':activity})
		if flag==True:
			self.Use(issuer,{'_id':'_'.join([action,activity]),'attr':{'action':action,'activity':activity}},tenant,'activity_assignment')
		else:
			print "error: no such activity in the tenant"

	def Unconsider(self,issuer,action,tenant,activity):
		self.Unuse(issuer,'_'.join([action,activity]),tenant,'activity_assignment')

        #*******************************************Tenant Creation and Hierarchy*************
	#create a tenant and assign it to a hierarchy
	def CreateTenant(self,issuer,tenantName):
		self.Use(issuer,{'_id':tenantName,'attr':{}},'TenantDB','tenant')
	def TenantHierarchy(self,issuer,tenantA,tenantB):
		flag=self.itp.hasObject('TenantDB','tenant',{'_id':tenantA}) and self.itp.hasObject('TenantDB','tenant',{'_id':tenantB})
		if flag==True:
			self.Use(issuer,{'_id':'_'.join([tenantA,tenantB]),'attr':{'parent':tenantA,'child':tenantB}},'TenantDB','tenant_hierarchy')
		else:
			print "Tenant A or Tenant B does not exist"

	#delete a tenant and remove it from an hierarchy
	def DeleteTenant(self,issuer,tenantName):
		self.UnUse(issuer,tenantName,'TenantDB','tenant')
		#remove from hierarchy not implemented yet
	def UnTenantHierarchy(self,issuer,tenantA,tenantB):
		self.UnUse(issuer,'_'.join([tenantA,tenantB]),'TenantDB','tenant_hierarchy')

	#*******************************************Permission*************************
	def Permission(self,issuer,permission_name,tenant,role,activity,view,context):
		flag=self.itp.hasObject(tenant,'role',{'_id':role}) and self.itp.hasObject(tenant,'activity',{'_id':activity}) and self.itp.hasObject(tenant,'view',{'_id':view}) and self.itp.hasObject(tenant,'context',{'_id':context})
		if flag==True:
			self.Use(issuer,{'_id':permission_name,'attr':{'role':role,'activity':activity,'view':view,'context':context}},tenant,'licence')	
		else:
			print "error: in permission, no role/activity/view or context"

	#permission unassignment
	def Unpermission(self,issuer,tenant,permission_name):
		self.Unuse(issuer,permission_name,tenant,'licence')

	#******************************************Cross Permission: Permission for a role in tenant A to manage a view in tenant B (init_tenant,role) (init_tenant,activity) (target_tenant,view) (init_tenant,context)

	#cross tenant permission, have one additional attribute in the licence, the target_tenant
	def Cross_Permission(self,issuer,permission_name,init_tenant,role,target_tenant,activity,target_view,context):
		flag=self.itp.hasObject(init_tenant,'role',{'_id':role}) and self.itp.hasObject(init_tenant,'context',{'_id':context})
		if flag==True:
			self.Use(issuer,{'_id':permission_name,'attr':{'role':role,'target_tenant':target_tenant,'mgmt_activity':activity,'target_view':target_view,'context':context}},init_tenant,'cross_licence')	
		else:
			print "error: in cross_permission, no init role or context"

	#cross tenant unpermission
	def Cross_Unpermission(self,issuer,tenant,permission_name):
		self.Unuse(issuer,permission_name,tenant,'cross_licence')

        #*******************************************Dominance Evaluation*************
	#evaluate if a tenant is superior than another tenant
	def Dominance(self,tenantA,tenantB):
		#Attention: same tenant relationship is not dominance
		return self.itp.hasObject('TenantDB','tenant_hierarchy',{'attr.parent':tenantA,'attr.child':tenantB})

	#*******************************************Produce Concrete Rules for normal permission in licence view**********************
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
					self.Use(tenant,{'_id':'_'.join([subject_name,action_name,v,context]),'attr':{'subject':subject_name,'action':action_name,'object':v,'context':context}},tenant,'concrete_rules')

					#if the "view" is administrative view, then we do not need to generate concrete rules that allow a subject to manage an object in the administrative view, we only need to specify that the subject can either "insert" or "delete" in this view, we thus skip the next loop that generate concrete rules for each object in the view
					if action_name=='insert' or action_name=='delete':
						pass
					else:
						for va in itp.readObject(tenant,v,{}):
							object_name=va['_id']
							#insert concrete permissions to allow a subject to perform certain action on objects in view
							self.Use(tenant,{'_id':'_'.join([subject_name,action_name,object_name,context]),'attr':{'subject':subject_name,'action':action_name,'object':object_name,'context':context}},tenant,'concrete_rules')

		return 

	#************************************************Check Authority Scope**************************************
	#an object is in the authority scope of a tenant if this object plays some views in the tenant or in its child tenants
	def CheckAuthorityScope(self,tenant,obj,category):
		#get tenant itself and dominated tenants
		tenant_list=[tenant]
		for one_tenant in self.itp.readObject('TenantDB','tenant',{}):
			tenant_name=one_tenant['_id']
			if self.Dominance(tenant,tenant_name):
				tenant_list.append(tenant_name)
		#find if the subject/action/object is comprised in these tenants
		admin_view=None
		if category=="role":
			admin_view="role_assignment"
			for t in tenant_list:
				if self.itp.hasObject(t,admin_view,{'attr.subject':obj}):
					return True
		if category=="activity":
			admin_view="activity_assignment"
			for t in tenant_list:
				if self.itp.hasObject(t,admin_view,{'attr.action':obj}):
					return True

		if category=="view":
			for t in tenant_list:
				view_list=self.itp.readObject(t,'view',{})
				for v in view_list:
					if self.itp.hasObject(t,v['_id'],{'_id':obj}):
						return True
		return False


