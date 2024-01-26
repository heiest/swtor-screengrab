class c1:
    @classmethod
    def print_myvar(cls):
        print(cls.myvar)

class c2(c1):
    myvar = 'yyy'

ic2 = c2()
c2.print_myvar()