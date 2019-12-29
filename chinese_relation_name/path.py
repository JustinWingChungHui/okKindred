from family_tree.models.relation import RAISED, RAISED_BY, PARTNERED
from family_tree.models.person import FEMALE, MALE

'''
Represents a path from one node to a next
'''
class Path():

    def __init__(self, start, goal):
        self.steps = []
        self.nodes = {}
        self.nodes[start.id] = start
        self.start = start
        self.goal = goal
        self.success = False
        self.titles = []
        self.generation = 0
        self.age_diff = 0

    def __str__(self):
        steps = [str(step) for step in self.steps]
        return " || ".join(steps)

    def add_node(self, node, relation_type):
        '''
        Adds a node to the path
        '''

        if node.id in self.nodes:
            raise ValueError('node already exists in path')


        if len(self.steps) == 0:
            last_node = self.start
        else:
            last_node = self.steps[-1].to_node

        step = PathStep(last_node, node, relation_type)

        self.steps.append(step)

        self.nodes[node.id] = node

        if node.id == self.goal.id:
            self.set_success_properties()


    def duplicate(self):
        duplicate = Path(self.start, self.goal)
        duplicate.nodes = self.nodes.copy()
        duplicate.steps = self.steps.copy()
        duplicate.success = self.success

        return duplicate


    def create_next_level_paths(self):
        last_node = self.steps[-1].to_node
        paths = []

        for relation_type, relation in last_node.relations:
            if not relation.id in self.nodes:
                path = self.duplicate()
                path.add_node(relation, relation_type)

                if path.success:
                    return [path]

                paths.append(path)

        return paths


    def set_success_properties(self):
        self.success = True
        for step in self.steps:
            step.set_step_code()
            self.titles.append(step.step_title())
            self.generation += step.generation

        self.age_diff = self.start.compare_ages(self.goal)





class PathStep():

    def __init__(self, from_node, to_node, relation_type):
        self.from_node = from_node
        self.to_node = to_node
        self.relation_type = relation_type
        self.generation = 0
        self.code = ''



    def __str__(self):
        return "{0} -> {1}".format(self.from_node.name, self.to_node.name)


    def step_title(self):

        if self.relation_type == PARTNERED:

            self.generation = 0

            if self.to_node.gender == FEMALE:
                return "Wife"
            elif self.to_node.gender == MALE:
                return "Husband"
            else:
                return "Partner"


        elif self.relation_type == RAISED_BY:

            self.generation = -1

            if self.to_node.gender == FEMALE:
                return "Mother"
            elif self.to_node.gender == MALE:
                return "Father"
            else:
                return "Parent"


        elif self.relation_type == RAISED:

            self.generation = 1

            if self.to_node.gender == FEMALE:
                return "Daughter"
            elif self.to_node.gender == MALE:
                return "Son"
            else:
                return "Child"


        else:
            raise ValueError("unknown relation type")


    def set_step_code(self):

        if self.relation_type == PARTNERED:

            self.generation = 0
            gen_code = '='

        elif self.relation_type == RAISED_BY:

            self.generation = -1
            gen_code = '-'


        elif self.relation_type == RAISED:

            self.generation = 1
            gen_code = '+'


        else:
            raise ValueError("unknown relation type")

        if self.to_node.gender == FEMALE:
            self.code = gen_code + 'F'
        elif self.to_node.gender == MALE:
            self.code = gen_code + 'M'
        else:
            self.code = gen_code + 'O'











