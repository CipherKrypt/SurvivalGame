from Environment import *

wild=Location('wild',1,0,10,50,50,10,0,20,0,40,0,5,40)
print(wild.__str__())
wild2=wild
try:
    wild.decrease_attribute('z')
except NotAnAttribute:
    print('Error')
    wild.decrease_attribute('all')
    print('decreased')

print(wild.__str__())
print(wild2.__str__())

