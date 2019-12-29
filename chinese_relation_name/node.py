
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



    def compare_ages(self, other_Node):
        if self.birth_year == 0 or other_Node.birth_year == 0:
            return 0

        elif self.birth_year < other_Node.birth_year:
            return 1

        elif self.birth_year > other_Node.birth_year:
            return -1

        else:
            return 0
