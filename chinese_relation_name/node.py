
'''
Node represents a navigal point on family tree
'''
class Node():

    def __init__(self, person):
        self.id = person.id
        self.name = person.name
        self.gender = person.gender
        self.birth_year = person.birth_year

        self.relations = []




