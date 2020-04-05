
#python class
class Employee:
	#pass
	def __init__(self,first,last,pay):
		self.first=first
		self.last=last
		self.pay=pay
		self.email=first+'.'+last+'@company.com'
	def fullname(self):
		self.test='test'
		return '{} {}'.format(self.first,self.last)
emp_1=Employee('Corey','Schafer',50000);
emp_2=Employee('Test','Test',60000);


'''
print(emp_1)
print(emp_2)

emp_1.first='Corey'
emp_1.last='Schafer'
emp_1.email=emp_1.first+emp_1.last+'@company.com'
emp_1.pay=50000


emp_2.first='Test'
emp_2.last='Test'
emp_2.email=emp_2.first+emp_2.last+'@company.com'
emp_2.pay=50000

print(emp_1.email)
print(emp_2.email)
'''
print(Employee.fullname(emp_1))
#print(emp_1.fullname())
print(emp_1.test)
