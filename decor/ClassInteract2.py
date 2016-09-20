def iget_no_of_instance(ins_obj):
    return ins_obj.__class__.no_inst
 
class Kls(object):
    no_inst = 0
 
    def __init__(self):
        Kls.no_inst = Kls.no_inst + 1
 
ik1 = Kls()
ik2 = Kls()
print iget_no_of_instance(ik1)