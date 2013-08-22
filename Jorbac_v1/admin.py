from evaluator import evaluator
from configurer import configurer


"""Admin class is an additional layer on configurer class so that every administrative action is first checked and then executed by configurer"""
class admin:
	def __init__(self,eva,config):
		self.eva=eva
		self.config=config


	#*****************************************************This function checks if an administrative action is allowed or not*******
	#Admin action can only be:   insert or delete
	#action issuer can be a dominating tenant or itself
	#Authorization is to allow admin_subject to perform an admin action on a view of a tenant
	#also need to check if "obj" fulfills constraint (present in the tenant)
	def AllowAction(self,issuer,admin_subject,action,tenant,view,obj):

		flag=False
		#intra-Tenant scenario
		if issuer==tenant:
			flag=self.eva.abstract_evaluate(tenant,admin_subject,action,view)
		
		#inter-Tenant scenario
		if issuer!=tenant:
			flag=self.config.Dominance(issuer,tenant) and self.eva.cross_abstract_evaluate(issuer,admin_subject,action,tenant,view)
		
		if flag==False:
			print "tenant relation or permission not fulfilled"
			return False

		#need then to check if the constraint is fulfilled, that is: if a subject/action/object is in the authority scope of the issuer tenant
		#an object is in the authority scope of a tenant if this object plays some views in the tenant or in its child tenants
		if view=='role_assignment':
			flag=self.config.CheckAuthorityScope(issuer,obj,"role")
		elif view=='activity_assignment':
			flag=self.config.CheckAuthorityScope(issuer,obj,"activity")
		elif view=='role' or view=='activity' or view=='view' or view=='context' or view=="licence" or view=="cross_licence":
			flag=True
		else:
			flag=self.config.CheckAuthorityScope(issuer,obj,"view")
		if flag==False:
			print "out of scope"
			return False	
		return flag

	#************************************************************Use and Unuse**************************************
	def Use(self,issuer,admin_subject,obj,tenant,view):
		
		flag=self.AllowAction(issuer,admin_subject,'insert',tenant,view,obj['_id'])
		if flag:
			self.config.Use(issuer,obj,tenant,view)
		else:
			message="User "+ admin_subject+ "is not able to perform action insert into view "+ view
			print message
			return message
		print "success"
		return "success"

	#Admin Action to unuse an object in a view
	def Unuse(self,issuer,admin_subject,identifier,tenant,view):
		#need to check if issuer is superior than target tenant, if yes, then ableToUse is temporary true (need to also check parent tenant's policy 
		flag=self.AllowAction(issuer,admin_subject,'delete',tenant,view,identifier)
	
		if flag:
			self.config.Unuse(issuer,tenant,view,identifier)
		else:
			message="User "+ admin_subject+ "is not able to perform action insert into view "+ view
			print message
			return message
		print "success"
		return "success"

	#********************************************************Assign and Unassign Role,Activity,View,Context****************
	#Admin action to assign role,activity,view to a tenant, will be checked by AdOrBAC
	def AssignRole(self,issuer,admin_subject,obj,tenant):
		self.Use(issuer,admin_subject,obj,tenant,'role')
	def AssignActivity(self,issuer,admin_subject,obj,tenant):
		self.Use(issuer,admin_subject,obj,tenant,'activity')
	def AssignView(self,issuer,admin_subject,obj,tenant):
		self.Use(issuer,admin_subject,obj,tenant,'view')
	def AssignContext(self,issuer,admin_subject,obj,tenant):
		self.Use(issuer,admin_subject,obj,tenant,'context')
		#need to create a collection for it?
	#corresponding unassign actions
	def UnassignRole(self,issuer,admin_subject,identifier,tenant):
		self.Unuse(issuer,admin_subject,identifier,tenant,'role')
	def UnassignActivity(self,issuer,admin_subject,identifier,tenant):
		self.Unuse(issuer,admin_subject,identifier,tenant,'activity')
	def UnassignView(self,issuer,admin_subject,identifier,tenant):
		self.Unuse(issuer,admin_subject,identifier,tenant,'view')
	def UnassignContext(self,issuer,admin_subject,identifier,tenant):
		self.Unuse(issuer,admin_subject,identifier,tenant,'context')


	#************************************************Empower and Unempower*****************************************************
	def Empower(self,issuer,admin_subject,subject,tenant,role):
		#need to check if the admin of issuer can perform such action
		flag=self.AllowAction(issuer,admin_subject,'insert',tenant,'role_assignment',subject)
		if flag:
			self.config.Empower(issuer,subject,tenant,role)
		else:
			message="User "+ admin_subject+ "is not able to perform action empower a subject into a role "
			print message
			return message
		print "success"
		return "success"
	#corresponding admin role unassignment
	def Unempower(self,issuer,admin_subject,subject,tenant,role):
		#need to check if the admin of issuer can perform such action
		flag=self.AllowAction(issuer,admin_subject,'delete',tenant,'role_assignment',subject)
		if flag:
			self.config.Unempower(issuer,subject,tenant,role)
		else:
			message="User "+ admin_subject+ "is not able to perform action delete into role_assignment "
			print message
			return message
		print "success"
		return "success"
	#************************************************Consider and Unconsider*****************************************************
	def Consider(self,issuer,admin_subject,action,tenant,activity):
		#need to check if the admin of issuer can perform such action
		flag=self.AllowAction(issuer,admin_subject,'insert',tenant,'activity_assignment',action)
		if flag:
			self.config.Consider(issuer,action,tenant,activity)
		else:
			message="User "+ admin_subject+ "is not able to perform action consider"
			print message
			return message
		print "success"
		return "success"
	#corresponding admin consider unassignment
	def Unconsider(self,issuer,admin_subject,action,tenant,activity):
		#need to check if the admin of issuer can perform such action
		flag=self.AllowAction(issuer,admin_subject,'delete',tenant,'activity_assignment',action)
		if flag:
			self.config.Unconsider(issuer,action,tenant,activity)
		else:
			message="User "+ admin_subject+ "is not able to perform action delete into activity_assignment "
			print message
			return message
		print "success"
		return "success"

	#************************************************Permission and Unpermission*****************************************************
	def Permission(self,issuer,admin_subject,permission_name,tenant,role,activity,view,context):
		#need to check if the admin of issuer can perform such action
		flag=self.AllowAction(issuer,admin_subject,'insert',tenant,'licence',None)
		if flag:
			self.config.Permission(issuer,permission_name,tenant,role,activity,view,context)
			print "success"
			return "success"
		else:
			message="User "+ admin_subject+ "is not able to perform action insert into licence "
			print message
			return message


	#permission unassignment
	def Unpermission(self,issuer,admin_subject,tenant,permission_name):
		#need to check if the admin of issuer can perform such action
		flag=self.AllowAction(issuer,admin_subject,'delete',tenant,'licence',None)
		if flag:
			self.config.Unpermission(issuer,tenant,permission_name)
			print "success"
			return "success"
		else:
			message="User "+ admin_subject+ "is not able to perform action delete into licence "
			print message
			return message


	#admin cross permission assignment, for now we do not use multi-grainularity licence
	def Cross_Permission(self,issuer,issuer_admin,permission_name,init_tenant,role,target_tenant,activity,target_view,context):
		#need to check if the admin of issuer can perform such action
		flag=self.AllowAction(issuer,issuer_admin,'insert',init_tenant,'cross_licence',None)
		if flag:
			self.config.Cross_Permission(issuer,permission_name,init_tenant,role,target_tenant,activity,target_view,context)
			print "success"
			return "success"
		else:
			message=issuer+ "User "+ issuer_admin+ "is not able to perform action insert into cross licence of "+init_tenant
			print message
			return message


	#cross permission unassignment
	def Cross_Unpermission(self,issuer,issuer_admin,tenant,permission_name):
		#need to check if the admin of issuer can perform such action
		flag=self.AllowAction(issuer,issuer_admin,'delete',tenant,'cross_licence',None)
		if flag:
			self.config.Cross_Unpermission(issuer,tenant,permission_name)
			print "success"
			return "success"
		else:
			message=issuer+ "User "+ issuer_admin+ "is not able to perform action delete into cross licence of "+tenant
			print message
			return message


