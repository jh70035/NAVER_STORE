
class A():
    def __init__(self, li):
        self.li=li
        print(li)
        self.fct()
        print(li)
    def fct(self):
        b=B()
        b.fct(self.li)
    
class B():
    def fct(self,li):
        li.append(3)

if __name__=="__main__":
    a=A([1,2,3])
    