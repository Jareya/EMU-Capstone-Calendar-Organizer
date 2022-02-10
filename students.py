class Student:
    
    def __init__(self, first, last, available):
        self.first = first
        self.last = last
        self.available = available
        self.email = first + '.' + last + '@emu.edu'

    def fullname(self):
        return '{} {}'.format(self.first, self.last)