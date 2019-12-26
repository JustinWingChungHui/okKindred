from family_tree.models.person import FEMALE, MALE
from chinese_relation_name.path_to_name_mapper_3rd_gen import get_3rd_gen_name


def get_name(path):
    # Mother, Father, Parent, Son, Daughter, Child
    if len(path.titles) == 1:
        return path.titles

    # 2 relations apart
    if len(path.titles) == 2:

        # Parent
        if path.steps[0].generation == -1:

            # Grandparents
            if path.steps[1].generation == -1:
                return get_grandparent_titles(path)

            # Step Parents
            elif path.steps[1].generation == 0:
                return get_stepparents_titles(path)

            # Siblings
            else: # path.steps[1].generation == 1

                return get_sibling_titles(path)


        # Parent
        elif path.steps[0].generation == 0:

            # Parents in law
            if path.steps[1].generation == -1:
                return get_parents_in_law(path)

            # Partner's Partner
            elif path.steps[1].generation == 0:
                return ["Partner's Partner"]

            # Step children
            else: # path.steps[1].generation == 1
                return get_stepchildren(path)


        # Child route
        else: # path.steps[1].generation == 1

            # Children's parent / ex-partner
            if path.steps[1].generation == -1:
                return ["Child's Parent / ex-Partner"]

            # son/daughter in law
            elif path.steps[1].generation == 0:
                return get_child_in_law(path)

            # Granchildren
            else: # path.steps[1].generation == 1
                return get_grandchildren(path)

    # 3 relations apart
    if len(path.titles) == 3:
        return get_3rd_gen_name(path)



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


def get_stepchildren(path):
    # step childred
    if path.goal.gender == FEMALE:
        return ['Stepdaughter']
    elif path.goal.gender == MALE:
        return ['Stepson']
    else:
        return ['Stepdaughter', 'Stepson']

def get_child_in_law(path):
    # children in law
    if path.goal.gender == FEMALE:
        return ['Daughter In Law']
    elif path.goal.gender == MALE:
        return ['Son In Law']
    else:
        return ['Daughter In Law', 'Son In Law']

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
        if path.age_diff < 0:
            return ["Elder Sister"]
        elif path.age_diff > 0:
            return ["Younger Sister"]
        else:
            return ["Sister", "Elder Sister", "Younger Sister"]

    # Brother
    elif path.goal.gender == MALE:
        if path.age_diff < 0:
            return ["Elder Brother"]
        elif path.age_diff > 0:
            return ["Younger Brother"]
        else:
            return ["Brother", "Elder Brother", "Younger Brother"]

    # Unknown
    else:
        if path.age_diff < 0:
            return ["Elder Sister", "Elder Brother"]
        elif path.age_diff > 0:
            return ["Younger Sister", "Younger Brother"]
        else:
            return ["Sister", "Brother", "Elder Sister",
                        "Elder Brother", "Younger Sister", "Younger Brother"]


def get_grandchildren(path):
    # Daughter's side
    if path.titles[0] == 'Daughter':
        if path.goal.gender == FEMALE:
            return ["Grandaughter Daughter's Side"]
        elif path.goal.gender == MALE:
            return ["Grandson Daughter's Side"]
        else:
            return ["Grandaughter Daughter's Side", "Grandson Daughter's Side"]

    # Son's side
    elif path.titles[0] == 'Son':
        if path.goal.gender == FEMALE:
            return ["Grandaughter Son's Side"]
        elif path.goal.gender == MALE:
            return ["Grandson Son's Side"]
        else:
            return ["Grandaughter Son's Side", "Grandson Son's Side"]

    # Child gender not specified
    else:
        if path.goal.gender == FEMALE:
            return ["Grandaughter Daughter's Side", "Grandaughter Son's Side"]
        elif path.goal.gender == MALE:
            return ["Grandson Daughter's Side", "Grandson Son's Side"]
        else:
            return ["Grandaughter Daughter's Side", "Grandson Daughter's Side",
            "Grandaughter Son's Side", "Grandson Son's Side"]