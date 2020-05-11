class Dog:
    kind = 'canine'         # class variable shared by all instances
    def __init__(self, name):
        self.name = name    # instance variable unique to each instance


d = Dog('Fido')
e = Dog('Buddy')

print('d:', d)
print('e:', e)
print('d.kind:', d.kind)
print('e.kind:', e.kind)
print('d.name:', d.name)
print('e.name:', e.name)

# d.kind                  # shared by all dogs'canine'
# e.kind                  # shared by all dogs'canine'
# d.name                  # unique to d'Fido'
# e.name                  # unique to e'Buddy'