from family_tree.models.person import FEMALE, MALE
from chinese_relation_name.path_to_name_mapper_3rd_gen import get_3rd_gen_name

'''
Map codes
- Parent
+ Offspring
= Partner
F Female
M Male
O Other
* Gender Wildcard
'''
map_codes = {
    # == 1 relation apart ==
    '-F': (lambda path: ['Mother']),
    '-M': (lambda path: ['Father']),
    '-O': (lambda path: ['Mother', 'Father']),
    '+F': (lambda path: ['Daughter']),
    '+M': (lambda path: ['Son']),
    '+O': (lambda path: ['Daughter', 'Son']),
    '=F': (lambda path: ['Wife']),
    '=M': (lambda path: ['Husband']),
    '=O': (lambda path: ['Wife', 'Husband']),

    # == 2 relations apart ==

    # Grandparents
    '-F,-F': (lambda path: ['Maternal Grandmother']),
    '-F,-M': (lambda path: ['Maternal Grandfather']),
    '-F,-O': (lambda path: ['Maternal Grandmother', 'Maternal Grandfather']),
    '-M,-F': (lambda path: ['Paternal Grandmother']),
    '-M,-M': (lambda path: ['Paternal Grandfather']),
    '-M,-O': (lambda path: ['Paternal Grandmother', 'Paternal Grandfather']),
    '-O,-F': (lambda path: ['Maternal Grandmother', 'Paternal Grandmother']),
    '-O,-M': (lambda path: ['Maternal Grandfather', 'Paternal Grandfather']),
    '-O,-O': (lambda path: ['Maternal Grandmother', 'Maternal Grandfather', 'Paternal Grandmother', 'Paternal Grandfather']),

    # Steparents
    '-*,=F': (lambda path: ['Stepmother']),
    '-*,=M': (lambda path: ['Stepfather']),
    '-*,=O': (lambda path: ['Stepmother', 'Stepfather']),


    # Siblings
    '-*,+F': (lambda path: get_sister(path)),
    '-*,+M': (lambda path: get_brother(path)),
    '-*,+O': (lambda path: get_sister(path) + get_brother(path)),

    # Parents in law
    '=F,-F': (lambda path: ["Wife's Mother"]),
    '=F,-M': (lambda path: ["Wife's Father"]),
    '=F,-O': (lambda path: ["Wife's Mother", "Wife's Father"]),
    '=M,-F': (lambda path: ["Husband's Mother"]),
    '=M,-M': (lambda path: ["Husband's Father"]),
    '=M,-O': (lambda path: ["Husband's Mother", "Husband's Father"]),
    '=O,-F': (lambda path: ["Wife's Mother","Husband's Mother"]),
    '=O,-M': (lambda path: ["Wife's Father","Husband's Father"]),
    '=O,-O': (lambda path: ["Wife's Mother", "Wife's Father", "Husband's Mother", "Husband's Father"]),

    # Partner's Partner
    '=*,=*': (lambda path: ["Partner's Partner"]),

    # Step Children
    '=*,+F': (lambda path: ["Stepdaughter"]),
    '=*,+M': (lambda path: ["Stepson"]),
    '=*,+O': (lambda path: ["Stepdaughter", "Stepson"]),

    # Child's parent / ex-partner
    '+*,-*': (lambda path: ["Child's Parent/ex-Partner"]),

    # Son/Daughter in law (do we have different terms for same sex relationships? e.g. +F,=F)
    '+*,=F': (lambda path: ["Daughter In Law"]),
    '+*,=M': (lambda path: ["Son In Law"]),
    '+*,=O': (lambda path: ["Daughter In Law", "Son in Law"]),

    # Grandchildren
    '+F,+F': (lambda path: ["Grandaughter Daughter's Side"]),
    '+F,+M': (lambda path: ["Grandson Daughter's Side"]),
    '+F,+O': (lambda path: ["Grandaughter Daughter's Side", "Grandson Daughter's Side"]),
    '+M,+F': (lambda path: ["Grandaughter Son's Side"]),
    '+M,+M': (lambda path: ["Grandson Son's Side"]),
    '+M,+O': (lambda path: ["Grandaughter Son's Side", "Grandson Son's Side"]),
    '+O,+F': (lambda path: ["Grandaughter Daughter's Side", "Grandaughter Son's Side"]),
    '+O,+M': (lambda path: ["Grandson Daughter's Side", "Grandson Son's Side"]),
    '+O,+O': (lambda path: ["Grandaughter Daughter's Side", "Grandson Daughter's Side",
                                "Grandaughter Son's Side", "Grandson Son's Side"]),
}


def replace_wildcards():

    max_key_length = max(map(len, map_codes))
    return replace_wildcard_iteration(0, map_codes, max_key_length)



def replace_wildcard_iteration(n, rel_map, max_key_length):

    if max_key_length < n:
        return rel_map

    new_rel_map = {}

    for key in rel_map:
        if n < len(key) and key[n] == '*':
            f_key = key.replace('*', 'F', 1)
            m_key = key.replace('*', 'M', 1)
            o_key = key.replace('*', 'O', 1)

            new_rel_map[f_key] = rel_map[key]
            new_rel_map[m_key] = rel_map[key]
            new_rel_map[o_key] = rel_map[key]

        else:
            new_rel_map[key] = rel_map[key]

    return replace_wildcard_iteration(n + 1, new_rel_map, max_key_length)


def get_name(path):

    path_key = ','.join(s.code for s in path.steps)
    full_map = replace_wildcards()

    # import pprint
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(full_map)

    # Mother, Father, Parent, Son, Daughter, Child
    if len(path.titles) == 1:

        path_formatter = full_map[path_key]
        return path_formatter(path)

    # 2 relations apart
    if len(path.titles) == 2:

        # Parent
        if path.steps[0].generation == -1:

            path_formatter = full_map[path_key]
            return path_formatter(path)


        # Parent
        elif path.steps[0].generation == 0:

            path_formatter = full_map[path_key]
            return path_formatter(path)


        # Child route
        else: # path.steps[1].generation == 1

            path_formatter = full_map[path_key]
            return path_formatter(path)

    # 3 relations apart
    if len(path.titles) == 3:
        return get_3rd_gen_name(path)



def get_stepchildren(path):
    # step childred
    if path.goal.gender == FEMALE:
        return ['Stepdaughter']
    elif path.goal.gender == MALE:
        return ['Stepson']
    else:
        return ['Stepdaughter', 'Stepson']


def get_sister(path):
    if path.age_diff < 0:
        return ["Elder Sister"]
    elif path.age_diff > 0:
        return ["Younger Sister"]
    else:
        return ["Sister", "Elder Sister", "Younger Sister"]


def get_brother(path):
    if path.age_diff < 0:
        return ["Elder Brother"]
    elif path.age_diff > 0:
        return ["Younger Brother"]
    else:
        return ["Brother", "Elder Brother", "Younger Brother"]


