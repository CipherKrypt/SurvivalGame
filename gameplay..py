'''from AccessObjects import *

u= user('Sandro','sandro','Hello','Allowed',5)
print(u.__str__())
u.pass_hash()
if u.check_pass('Hello'):
    print('correct')'''

from Environment import *

wild=Location('wild',1,0,10,50,50,10,0,20,0,40,0,5,40)
print(wild.__str__())
for i in range(10):
    print(wild.search())
