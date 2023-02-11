class prime:
    def __init__(self, container_type):
        self.a = container_type()
        self.a += container_type([2, 3, 5, 7])

l = prime(list)
print(l.a)

t = prime(tuple)
print(t.a)