import web
import ast
import sys
sys.path.append('/home/qian/Desktop/Jorbac')

from evaluator import evaluator
from interpretor import interpretor



itp=interpretor('127.0.0.1',27017)
eva=evaluator(itp)
urls={

	'/.*','index'
	
}



class index:
	def GET(self):
		return "Hello, world!"
	def POST(self):
		i=web.input()
		result= eva.concrete_evaluate(i.t,i.s,i.a,i.o)
		return str(result)



application = web.application(urls,globals()).wsgifunc()
