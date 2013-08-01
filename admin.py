from evaluator import evaluator
from configurer import configurer


class admin:
	def __init__(self,eva,config):
		self.eva=eva
		self.config=config

	#Admin class add an additional layer on configurer class so that every administrative action is first checked and then executed by configurer
	def Use(self,issuer,tenant,admin,obj,view):
		
		#need to check if issuer is superior than target tenant, if yes, then ableToUse is temporary true (need to also check parent tenant's policy 
		ableToUse=self.AllowAction(issuer,tenant,admin,'insert',view)
		if ableToUse:
			self.config.Use(issuer,tenant,obj,view)
		else:
			message="User "+ admin+ "is not able to perform action insert into view "+ view
			print message
			return message
		print "success"
		return "success"

	#Admin Action to unuse an object in a view
	def Unuse(self,issuer,tenant,admin,identifier,view):
		#need to check if issuer is superior than target tenant, if yes, then ableToUse is temporary true (need to also check parent tenant's policy 
		ableToUse=self.AllowAction(issuer,tenant,admin,'delete',view)
	
		if ableToUse:
			self.config.Unuse(issuer,tenant,view,identifier)
		else:
			message="User "+ admin+ "is not able to perform action insert into view "+ view
			print message
			return message
		print "success"
		return "success"

	#This function use evaluator to decide if certain action can be performed
	def AllowAction(self,issuer,tenant,admin,action,view):
		ableToUse=False
		#need to check if issuer is superior than target tenant, if yes, then ableToUse is temporary true (need to also check parent tenant's policy )
		if self.config.Dominance(issuer,tenant):
			ableToUse=True
		else:
			print issuer+" cannot dominant "+tenant+", operation failed"
			return ableToUse

		#if issuer dominate tenant, then the able to use is decided by the administrative policy of issuer
		if ableToUse and issuer!=tenant:
			ableToUse=self.eva.cross_concrete_evaluate(issuer,admin,action,tenant,view)
		if ableToUse and issuer==tenant:
			ableToUse=self.eva.concrete_evaluate(tenant,admin,action,view)
		return ableToUse
		



	#Admin action to assign subject,action,object,role,activity,view to a tenant, will be checked by AdOrBAC
	def AssignSubject(self,issuer,tenant,admin,obj):
		self.Use(issuer,tenant,admin,obj,'subject')
	def AssignAction(self,issuer,tenant,admin,obj):
		self.Use(issuer,tenant,admin,obj,'action')
	def AssignObject(self,issuer,tenant,admin,obj):
		self.Use(issuer,tenant,admin,obj,'object')
	def AssignRole(self,issuer,tenant,admin,obj):
		self.Use(issuer,tenant,admin,obj,'role')
	def AssignActivity(self,issuer,tenant,admin,obj):
		self.Use(issuer,tenant,admin,obj,'activity')
	def AssignView(self,issuer,tenant,admin,obj):
		self.Use(issuer,tenant,admin,obj,'view')
	def AssignContext(self,issuer,tenant,admin,obj):
		self.Use(issuer,tenant,admin,obj,'context')
		#need to create a collection for it?
	#corresponding unassign actions
	def UnassignSubject(self,issuer,tenant,admin,identifier):
		self.Unuse(issuer,tenant,admin,identifier,'subject')
	def UnassignAction(self,issuer,tenant,admin,identifier):
		self.Unuse(issuer,tenant,admin,identifier,'action')
	def UnassignObject(self,issuer,tenant,admin,identifier):
		self.Unuse(issuer,tenant,admin,identifier,'object')
	def UnassignRole(self,issuer,tenant,admin,identifier):
		self.Unuse(issuer,tenant,admin,identifier,'role')
	def UnassignActivity(self,issuer,tenant,admin,identifier):
		self.Unuse(issuer,tenant,admin,identifier,'activity')
	def UnassignView(self,issuer,tenant,admin,identifier):
		self.Unuse(issuer,tenant,admin,identifier,'view')
	def UnassignContext(self,issuer,tenant,admin,identifier):
		self.Unuse(issuer,tenant,admin,identifier,'context')

	#role,activity assignment
	def Empower(self,issuer,tenant,admin,subject,role):
		#need to check if the admin of issuer can perform such action
		ableToUse=self.AllowAction(issuer,tenant,admin,'insert','role_assignment')
		if ableToUse:
			self.config.Empower(issuer,tenant,subject,role)
		else:
			message="User "+ admin+ "is not able to perform action empower a subject into a role "
			print message
			return message
		print "success"
		return "success"



	def Consider(self,issuer,tenant,admin,action,activity):
		#need to check if the admin of issuer can perform such action
		ableToUse=self.AllowAction(issuer,tenant,admin,'insert','activity_assignment')
		if ableToUse:
			self.config.Consider(issuer,tenant,action,activity)
		else:
			message="User "+ admin+ "is not able to perform action consider an action into an activity "
			print message
			return message
		print "success"
		return "success"

	#corresponding admin role,activity unassignment
	def Unempower(self,issuer,tenant,admin,subject,role):
		#need to check if the admin of issuer can perform such action
		ableToUnUse=self.AllowAction(issuer,tenant,admin,'delete','role_assignment')
		if ableToUnUse:
			self.config.Unempower(issuer,tenant,subject,role)
		else:
			message="User "+ admin+ "is not able to perform action delete into role_assignment "
			print message
			return message
		print "success"
		return "success"

	def Unconsider(self,issuer,tenant,admin,action,activity):
		#need to check if the admin of issuer can perform such action
		ableToUnUse=self.AllowAction(issuer,tenant,admin,'delete','activity_assignment')
		if ableToUnUse:
			self.config.Unconsider(issuer,tenant,action,activity)
		else:
			message="User "+ admin+ "is not able to perform action delete into activity_assignment "
			print message
			return message
		print "success"
		return "success"



	#admin permission assignment, for now we do not use multi-grainularity licence
	def Permission(self,issuer,permission_name,tenant,admin,role,activity,view,context):
		#need to check if the admin of issuer can perform such action
		ableToUse=self.AllowAction(issuer,tenant,admin,'insert','licence')
		if ableToUse:
			self.config.Permission(issuer,permission_name,tenant,role,activity,view,context)
		else:
			message="User "+ admin+ "is not able to perform action insert into licence "
			print message
			return message
		print "success"
		return "success"

	#permission unassignment
	def Unpermission(self,issuer,tenant,admin,permission_name):
		#need to check if the admin of issuer can perform such action
		ableToUnUse=self.AllowAction(issuer,tenant,admin,'delete','licence')
		if ableToUnUse:
			self.config.Unpermission(issuer,tenant,permission_name)
		else:
			message="User "+ admin+ "is not able to perform action delete into licence "
			print message
			return message
		print "success"
		return "success"

	#admin cross permission assignment, for now we do not use multi-grainularity licence
	def Cross_Permission(self,issuer,issuer_admin,permission_name,init_tenant,role,target_tenant,activity,target_view,context):
		#need to check if the admin of issuer can perform such action
		ableToUse=self.AllowAction(issuer,init_tenant,issuer_admin,'insert','cross_licence')
		if ableToUse:
			self.config.Cross_Permission(issuer,permission_name,init_tenant,role,target_tenant,activity,target_view,context)
		else:
			message=issuer+ "User "+ issuer_admin+ "is not able to perform action insert into cross licence of "+init_tenant
			print message
			return message
		print "success"
		return "success"

	#cross permission unassignment
	def Cross_Unpermission(self,issuer,issuer_admin,tenant,permission_name):
		#need to check if the admin of issuer can perform such action
		ableToUnUse=self.AllowAction(issuer,tenant,issuer_admin,'delete','cross_licence')
		if ableToUnUse:
			self.config.Cross_Unpermission(issuer,tenant,permission_name)
		else:
			message=issuer+ "User "+ issuer_admin+ "is not able to perform action delete into cross licence of "+tenant
			print message
			return message
		print "success"
		return "success"










