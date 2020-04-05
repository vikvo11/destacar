
#python class
class Employee:
	num_of_empls=0
	raise_amount=1.04
	#pass
	def __init__(self,first,last,pay):
		self.first=first
		self.last=last
		self.pay=pay
		#self.email=first+'.'+last+'@company.com'
		Employee.num_of_empls +=1
	def copy(self,other):
		other.first=self.first
		other.last=self.last
		other.pay=self.pay
	@property
	def email(self):
		#self.test='test'
		return '{}.{}@company.com'.format(self.first,self.last)
	@property
	def fullname(self):
		#self.test='test'
		return '{} {}'.format(self.first,self.last)
	@fullname.setter
	def fullname(self,name):
		first,last=name.split(' ')
		self.first=first
		self.last=last
	@fullname.deleter
	def fullname(self):
		print('Delete Name')
		self.first=None
		self.last=None
	def apply_raise(self):
		#self.pay=int(self.pay*Employee.raise_amount) #переменная класа
		self.pay=int(self.pay*self.raise_amount) #переменная инстанса

	def __repr__(self):
		return "Employee('{},'{}','{}')".format(self.first,self.last,self.pay)
	def __str__(self):
		return '{} - {}'.format(self.fullname,self.email)
	def __add__(self,other):
		return self.pay+other.pay
	@classmethod
	def set_raise_amt(cls,amount):
		cls.raise_amount=amount
	@classmethod
	def from_string(cls,emp_str):
		first,last,pay=emp_str.split('-')
		return cls(first,last,pay)
	@staticmethod
	def is_workday(day):
		if day.weekday() == 5 or day.weekday() ==6:
			return False
		return True

class Developer(Employee):
	raise_amount=1.10
	def __init__(self,first,last,pay,prog_lang):
		super().__init__(first,last,pay)
		#Employee.__init__(self,first,last,pay)
		self.prog_lang=prog_lang

class Manager(Employee):
	def __init__(self,first,last,pay,employees=None):
		super().__init__(first,last,pay)
		#Employee.__init__(self,first,last,pay)
		if employees is None:
			self.employees=[]
		else:
			self.employees=employees

	def add_emp(self,emp):
		if emp not in self.employees:
			self.employees.append(emp)

	def remove_emp(self,emp):
		if emp in self.employees:
			self.employees.remove(emp)
	def print_emps(self):
		for emp in self.employees:
			print('--->',emp.fullname)

dev_1=Developer('Corey','Schafer',50000,'python');
dev_2=Developer('Test','Test',60000,'java');

mgr_1=Manager('Sue','Smith',9000,[dev_1])
print(mgr_1.email)
mgr_1.add_emp(dev_2)
mgr_1.remove_emp(dev_1)
mgr_1.print_emps()
#print(help(Developer))

#print(dev_2.email)

print(dev_1.pay)
dev_1.apply_raise()
print(dev_1.pay)

print(dev_1.prog_lang)
print(dev_2.prog_lang)
emp_1=Employee('Corey','Schafer',50000);
emp_2=Employee('Test','Test',60000);
emp_3=Employee.from_string('Test-Test-60000');
#print(emp_1.__dict__)
#print(Employee.__dict__)

#Employee.raise_amount=1.05
#emp_1.raise_amount=1.05
Employee.set_raise_amt(1.05)
#print(Employee.raise_amount)
#print(emp_1.raise_amount)
#print(emp_2.raise_amount)
#print(Employee.num_of_empls)
#emp_1.apply_raise()
#print(emp_1.pay)
print(emp_3.__dict__)

import datetime
my_date=datetime.date(2016,7,11)
print(Employee.is_workday(my_date))


print(isinstance(mgr_1,Employee))
print(issubclass(Developer,Employee))

print(emp_1)
print (repr(emp_1))
print (str(emp_1))
print(emp_1+emp_2)
print (repr(my_date))
emp_1.first='Viktor'
print(emp_1.email)

emp_1.fullname='Test Test'
print(emp_1.fullname)
del emp_1.fullname

emp_3=Employee('Test','Tessst','111')
emp_3=Employee('123','123','123')
emp_3=Employee(None,None,None)
#del emp_3
print(emp_3)
emp_4=Employee(emp_2.first,emp_2.last,emp_2.pay)
#emp_4=Employee('1','2','3')
#emp_2.copy(emp_4)
print(emp_2.__dict__)
print(emp_4.__dict__)
