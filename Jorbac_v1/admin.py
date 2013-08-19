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
			flag=self.config.Dominance(issuer,tenant) and self.config.cross_abstract_evaluate(issuer,admin_subject,action,tenant,view)
		
		if flag==False:
			print "tenant relation or permission not fulfilled"
			return False

		#need then to check if the constraint is fulfilled, that is: if a subject/action/object is in the authority scope of the issuer tenant
		#an object is in the authority scope of a tenant if this object plays some views in the tenant or in its child tenants
		if view=='role_assignment':
			flag=self.config.CheckAuthorityScope(issuer,obj,"role")
		elif view=='activity_assignment':
			flag=self.config.CheckAuthorityScope(issuer,obj,"activity")
		else:
			flag=self.config.CheckAuthorityScope(issuer,obj,"view")
		if flag==False:
			print "out of scope"
			return False	
		return flag
