from family_tree.models.person import FEMALE, MALE
from chinese_relation_name.node import Node
from chinese_relation_name.path import Path


def get_name(path):
    # Mother, Father, Parent, Son, Daughter, Child
    if len(path.titles) == 1:
        return path.titles

    # 2 relations apart
    if len(path.titles) == 2:

        if path.steps[0].generation == -1:
            # Parent route

            if path.steps[1].generation == -1:
                # Grandparents
                return get_grandparent_titles(path)

            elif path.steps[1].generation == 0:
                # Step Parents
                return get_stepparents_titles(path)

            else: # path.steps[1].generation == 1
                # Siblings
                return get_sibling_titles()



        elif path.steps[0].generation == 0:
            # Partner route

            if path.steps[1].generation == -1:
                # Parents in law
                return get_parents_in_law(path)

            elif path.steps[1].generation == 0:
                # Partner's Partner
                pass

            else: # path.steps[1].generation == 1
                # Step childred
                pass

        else: # path.steps[1].generation == 1
            # Child route

            if path.steps[1].generation == -1:
                # Children's parent
                pass

            elif path.steps[1].generation == 0:
                # Child in law
                pass

            else: # path.steps[1].generation == 1
                # Granchildren
                pass

    # 3 relations apart
    if len(path.titles) == 3:

        # Great grandparents
        if path.generation == -3:
            pass

        # Brain melt


def get_parents_in_law(path):

    # Wife's side
    if path.titles[0] == 'Wife':
        if path.goal.gender == FEMALE:
            return ["Wife's Mother"]
        elif path.goal.gender == MALE:
            return ["Wife's Father"]
        else:
            return ["Wife's Mother", "Wife's Father"]

    # Husband's side
    elif path.titles[0] == 'Husband':
        if path.goal.gender == FEMALE:
            return ["Husband's Mother"]
        elif path.goal.gender == MALE:
            return ["Husband's Father"]
        else:
            return ["Husband's Mother", "Husband's Father"]

    else:
        if path.goal.gender == FEMALE:
            return ["Wife's Mother", "Husband's Mother"]
        elif path.goal.gender == MALE:
            return ["Wife's Father", "Husband's Father"]
        else:
            return ["Wife's Mother", "Wife's Father",
                        "Husband's Mother", "Husband's Father"]


def get_stepparents_titles(path):

    # parents in law
    if path.goal.gender == FEMALE:
        return ['Stepmother']
    elif path.goal.gender == MALE:
        return ['Stepfather']
    else:
        return ['Stepmother', 'Stepfather']



def get_grandparent_titles(path):

    # Mother's side
    if path.titles[0] == 'Mother':
        if path.titles[1] == 'Mother':
            return ['Maternal Grandmother']
        elif path.titles[1] == 'Father':
            return ['Maternal Grandfather']
        else:
            return ['Maternal Grandmother', 'Maternal Grandfather']

    # Father's side
    elif path.titles[0] == 'Father':
        if path.titles[1] == 'Mother':
            return ['Paternal Grandmother']
        elif path.titles[1] == 'Father':
            return ['Paternal Grandfather']
        else:
            return ['Paternal Grandmother', 'Paternal Grandfather']

    else:
        if path.titles[1] == 'Mother':
            return ['Maternal Grandmother', 'Paternal Grandmother']
        elif path.titles[1] == 'Father':
            return ['Paternal Grandmother', 'Paternal Grandfather']
        else:
            return ['Maternal Grandmother', 'Maternal Grandfather',
                    'Paternal Grandmother', 'Paternal Grandfather']


def get_sibling_titles(path):
     # Sister
    if path.goal.gender == FEMALE:
        if path.age_diff > 1:
            return ["Elder Sister"]
        elif path.age_diff > 1:
            return ["Younger Sister"]
        else:
            return ["Sister", "Elder Sister", "Younger Sister"]

    # Brother
    elif path.goal.gender == MALE:
        if path.age_diff > 1:
            return ["Elder Brother"]
        elif path.age_diff > 1:
            return ["Younger Brother"]
        else:
            return ["Brother", "Elder Brother", "Younger Brother"]

    # Unknown
    else:
        if path.age_diff > 1:
            return ["Elder Sister", "Elder Brother"]
        elif path.age_diff > 1:
            return ["Younger Sister", "Younger Brother"]
        else:
            return ["Sister", "Brother", "Elder Sister",
                        "Elder Brother", "Younger Sister", "Younger Brother"]