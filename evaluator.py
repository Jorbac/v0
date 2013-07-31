from interpretor import interpretor

class evaluator:
	def __init__(self,itp):
		self.itp=itp
	def concrete_evaluate(self,tenant,s,a,o):
		#get concrete permissions
		permission_list=self.itp.readObject(tenant,'concrete_rules',{'attr.subject':s,'attr.action':a,'attr.object':o})
		for permission in permission_list:
			context=permission['attr']['context']
			contextObject=self.itp.readOneObject(tenant,'context',{'_id':context})
			#need to evaluate context here,but currently not implemented
			return True
		return False




