IND = 'ON'
 
def checkind():
    return (IND == 'ON')
 
class Kls(object):
    def __init__(self,data):
        self.data = data
 
    def do_reset(self):
        if checkind():
            print('Reset done for:', self.data)
     
    def set_db(self):
        if checkind():
            self.db = 'new db connection'
            print('DB connection made for:',self.data)
 
ik1 = Kls(12)
ik1.do_reset()
ik1.set_db()