from evaluator import evaluator
from configurer import configurer


class admin:
	def __init__(self,eva,config):
		self.eva=eva
		self.config=config

	#Admin class add an additional layer on configurer class so that every administrative action is first checked and then executed by configurer

	def Use(self,issuer,tenant,admin,obj,view):
		ableToUse=False
		#the feature of cross-tenant management is not added yet

		if issuer==tenant:
			ableToUse=self.eva.concrete_evaluate(tenant,admin,'insert',view)
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
		ableToUnUse=False


		#the feature of cross-tenant management is not added yet

		if issuer==tenant:
			ableToUnUse=self.eva.concrete_evaluate(tenant,admin,'delete',view)
		if ableToUnUse:
			self.config.Unuse(issuer,tenant,view,identifier)
		else:
			message="User "+ admin+ "is not able to perform action delete into view "+ view
			print message
			return message
		print "success"
		return "success"


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
		ableToUse=False
		#the feature of cross-tenant management is not added yet

		if issuer==tenant:
			ableToUse=self.eva.concrete_evaluate(tenant,admin,'insert','role_assignment')
		if ableToUse:
			self.config.Empower(issuer,tenant,subject,role)
		else:
			message="User "+ admin+ "is not able to perform action empower a subject into a role "
			print message
			return message
		print "success"
		return "success"



	def Consider(self,issuer,tenant,admin,action,activity):
		ableToUse=False
		#the feature of cross-tenant management is not added yet

		if issuer==tenant:
			ableToUse=self.eva.concrete_evaluate(tenant,admin,'insert','activity_assignment')
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
		ableToUnUse=False
		#the feature of cross-tenant management is not added yet
		if issuer==tenant:
			ableToUnUse=self.eva.concrete_evaluate(tenant,admin,'delete','role_assignment')
		if ableToUnUse:
			self.config.Unempower(issuer,tenant,subject,role)
		else:
			message="User "+ admin+ "is not able to perform action delete into role_assignment "
			print message
			return message
		print "success"
		return "success"

	def Unconsider(self,issuer,tenant,admin,action,activity):
		ableToUnUse=False
		#the feature of cross-tenant management is not added yet
		if issuer==tenant:
			ableToUnUse=self.eva.concrete_evaluate(tenant,admin,'delete','activity_assignment')
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
		ableToUse=False
		#the feature of cross-tenant management is not added yet
		if issuer==tenant:
			ableToUse=self.eva.concrete_evaluate(tenant,admin,'insert','licence')
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
		ableToUnUse=False
		#the feature of cross-tenant management is not added yet
		if issuer==tenant:
			ableToUnUse=self.eva.concrete_evaluate(tenant,admin,'delete','licence')
		if ableToUnUse:
			self.config.Unpermission(issuer,tenant,permission_name)
		else:
			message="User "+ admin+ "is not able to perform action delete into licence "
			print message
			return message
		print "success"
		return "success"










