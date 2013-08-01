from interpretor import interpretor

class evaluator:
	def __init__(self,itp):
		self.itp=itp

	#it evaluates if a subject is able to access an object using certain actions. The evaluation is based on concrete rules produced by abstracted rules
	def concrete_evaluate(self,tenant,s,a,o):
		#get concrete permissions
		permission_list=self.itp.readObject(tenant,'concrete_rules',{'attr.subject':s,'attr.action':a,'attr.object':o})
		for permission in permission_list:
			context=permission['attr']['context']
			contextObject=self.itp.readOneObject(tenant,'context',{'_id':context})
			#need to evaluate context here,but currently not implemented
			return True
		return False

	def cross_concrete_evaluate(self,tenant,s,a,target,view):
		#get cross account administration action and concrete permissions
		permission_list=self.itp.readObject(tenant,'cross_concrete_rules',{'attr.subject':s,'attr.action':a,'attr.target':target,'attr.object':view})
		for permission in permission_list:
			context=permission['attr']['context']
			contextObject=self.itp.readOneObject(tenant,'context',{'_id':context})
			#need to evaluate context here,but currently not implemented
			return True
		return False


		



