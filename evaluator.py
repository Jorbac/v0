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
	#evaluate in abstract level
	def abstract_evaluate(self,tenant,s,a,o):
		#get abstract role,activity and view
		role_list=self.itp.readObject(tenant,'role_assignment',{'attr.subject':s})
		activity_list=self.itp.readObject(tenant,'activity_assignment',{'attr.action':a})
		all_view=self.itp.readObject(tenant,'view',{})
		view_list=[]
		for v in all_view:
			if self.itp.hasObject(tenant,v['_id'],{'_id':o}):
				view_list.append(v)
		for r in role_list:
			for a in activity_list:
				for v in view_list:
					#print r['attr']['role']+"        "
					#print a['attr']['activity']+"     "
					#print v['_id']+"      "
					#print "\n"
					if self.itp.hasObject(tenant,'licence',{'attr.role':r['attr']['role'],'attr.activity':a['attr']['activity'],'attr.view':v['_id']}):
						return True
		return False		
		



