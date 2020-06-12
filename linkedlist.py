class node:

    def __init__(self, val, block = False, prev = None, next = None):
        self.val = val
        self.next = next
        self.prev = prev
        self.block = block

    def setvalue(self, val):
        self.val = val

    def setnext(self, next):
        self.next = next

    def setprev(self, prev):
        self.prev = prev

    def setblock(self, block):
        self.block = block

    def getnext(self):
        return self.next

    def getprev(self):
        return self.prev

    def getblock(self):
        return self.block

    def getvalue(self):
        return self.val
