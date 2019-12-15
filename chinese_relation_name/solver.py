from family_tree.models.person import Person
from family_tree.models.relation import Relation, PARTNERED, RAISED, RAISED_BY
from chinese_relation_name.node import Node
from chinese_relation_name.path import Path
from chinese_relation_name.path_to_name_mapper import get_name

class Solver():

    def __init__(self):
        self.result = None
        self.nodes = {}

    def solve(self, family_id, from_id, to_id):
        '''
        Gets the relation name
        '''
        self.load_data(family_id)
        self.find_path(from_id, to_id)
        return get_name(self.result)


    def load_data(self, family_id):
        '''
        Loads all relevant family data
        '''

        relations = Relation.objects.filter(from_person__family_id = family_id)
        people = Person.objects.filter(family_id = family_id)


        for person in people:
            node = Node(person)
            self.nodes[node.id] = node


        for relation in relations:
            from_node = self.nodes[relation.from_person_id]
            to_node = self.nodes[relation.to_person_id]

            if relation.relation_type == PARTNERED:
                from_node.relations.append((PARTNERED, to_node))
                to_node.relations.append((PARTNERED, from_node))

            elif relation.relation_type == RAISED:
                from_node.relations.append((RAISED, to_node))
                to_node.relations.append((RAISED_BY, from_node))




    def find_path(self, from_id, to_id):
        '''
        Calculates path from one node to another
        '''

        if from_id == to_id:
            return None

        node = self.nodes[from_id]
        goal_node = self.nodes[to_id]
        paths = []

        for relation_type, relation in node.relations:
            path = Path(node, goal_node)
            paths.append(path)

            path.add_node(relation, relation_type)

            if path.success:

                return path

        self.search_paths(paths)


    def search_paths(self, paths):
        '''
        Recursive path search to connect two family members
        '''
        if self.result:
            return

        new_paths = []

        for path in paths:
            next_level_paths = path.create_next_level_paths()

            if len(next_level_paths) == 1 and next_level_paths[0].success:
                self.result = next_level_paths[0]
                return

            else:
                new_paths.extend(next_level_paths)

        self.search_paths(new_paths)















