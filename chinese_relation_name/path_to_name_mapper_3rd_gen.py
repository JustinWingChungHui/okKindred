from family_tree.models.person import FEMALE, MALE
from chinese_relation_name.node import Node
from chinese_relation_name.path import Path


def get_3rd_gen_name(path):

    # Parent
    if path.steps[0].generation == -1:

        # Grandparent
        if path.steps[1].generation == -1:

            # Great grandparents
            if path.steps[2].generation == -1:
                return get_great_grandparents(path)

            # Step Grandparent
            elif path.steps[2].generation == 0:
                return []

            # Aunt/ Uncle
            else: #-1
                return get_aunt_uncle(path)

        # Step Parent
        elif path.steps[1].generation == 0:

            # Step grandparents
            if path.steps[2].generation == -1:
                pass

            # Step-Step Parent
            elif path.steps[2].generation == 0:
                pass

            # Step sibling
            else: #-1
                pass

        # Sibling
        elif path.steps[1].generation == 1:

            # Step Parent
            if path.steps[2].generation == -1:
                pass

            # Sibling in law
            elif path.steps[2].generation == 0:
                pass

            # Niece/Nephew
            else: #-1
                pass

    # Partner
    elif path.steps[0].generation == 0:

         # Parents in law
        if path.steps[1].generation == -1:

            # Grandparents in law
            if path.steps[2].generation == -1:
                pass

            # Step parents in law
            elif path.steps[2].generation == 0:
                pass

            # Sibling in law
            else: #-1
                pass

        # Partner's ex
        elif path.steps[1].generation == 0:
            # Partner's ex's parents / ex / child
            return []



        # Step children
        elif path.steps[1].generation == 1:

            # Step Children's Parent
            if path.steps[2].generation == -1:
                pass

            # Step Child's Partner
            elif path.steps[2].generation == 0:
                pass

            # Step Grandchildren
            else: #-1
                pass

    # Child
    elif path.steps[0].generation == 1:

         # Ex-Partner
        if path.steps[1].generation == -1:

            # Ex-Partner's Parents
            if path.steps[2].generation == -1:
                pass

            # Ex-Partner's Partner
            elif path.steps[2].generation == 0:
                return []

            # Step children
            else: #-1
                pass

        # Son/Daughter in law
        elif path.steps[1].generation == 0:

            # Son/Daughter in law's parents
            if path.steps[2].generation == -1:
                pass

            # Son/Daughter in law's partner
            elif path.steps[2].generation == 0:
                pass

            # Step Grandchild (Son/Daughter in law's child)
            else: #-1
                pass

        # Grandchild
        elif path.steps[1].generation == 1:

            # Grandchild's Other Parent
            if path.steps[2].generation == -1:
                pass

            # Grandchild in law
            elif path.steps[2].generation == 0:
                pass

            # Great Grandchildren
            else: #-1
                pass

def get_great_grandparents(path):

    # Mother's side
    if path.titles[0] == 'Mother':
        if path.titles[2] == 'Mother':
            return ['Maternal Great Grandmother']
        elif path.titles[2] == 'Father':
            return ['Maternal Great Grandfather']
        else:
            return ['Maternal Great Grandmother', 'Maternal Great Grandfather']

    # Father's side
    elif path.titles[0] == 'Father':
        if path.titles[2] == 'Mother':
            return ['Paternal Great Grandmother']
        elif path.titles[2] == 'Father':
            return ['Paternal Great Grandfather']
        else:
            return ['Paternal Great Grandmother', 'Paternal Great Grandfather']

    else:
        if path.titles[2] == 'Mother':
            return ['Maternal Great Grandmother', 'Paternal Great Grandmother']
        elif path.titles[2] == 'Father':
            return ['Maternal Great Grandfather', 'Paternal Great Grandfather']
        else:
            return ['Maternal Great Grandmother', 'Maternal Great Grandfather',
                    'Paternal Great Grandmother', 'Paternal Great Grandfather']


def get_aunt_uncle(path):

    parent = path.steps[0].to_node

    # Mother's side
    if path.titles[0] == 'Mother':

        # Aunt
        if path.goal.gender == FEMALE:

            # Elder
            if parent.compare_ages(path.goal) == -1:
                return ["Mother's Elder Sister", "Mother's Sister"]

             # Younger
            elif parent.compare_ages(path.goal) == 1:
                return ["Mother's Younger Sister", "Mother's Sister"]

            # Unknown Age
            else:
                return ["Mother's Elder Sister", "Mother's Younger Sister", "Mother's Sister"]

        # Uncle
        elif path.goal.gender == MALE:

            # Elder
            if parent.compare_ages(path.goal) == -1:
                return ["Mother's Elder Brother", "Mother's Brother"]

             # Younger
            elif parent.compare_ages(path.goal) == 1:
                return ["Mother's Younger Brother", "Mother's Brother"]

            # Unknown Age
            else:
                return ["Mother's Elder Brother", "Mother's Younger Brother", "Mother's Brother"]

        # Either gender
        else:

            # Elder
            if parent.compare_ages(path.goal) == 1:
                return ["Mother's Elder Sister", "Mother's Sister",
                        "Mother's Elder Brother", "Mother's Brother"]

             # Younger
            elif parent.compare_ages(path.goal) == -1:
                return ["Mother's Younger Sister", "Mother's Sister",
                        "Mother's Younger Brother", "Mother's Brother"]

            # Unknown Age
            else:
                return ["Mother's Elder Sister", "Mother's Younger Sister", "Mother's Sister",
                        "Mother's Elder Brother", "Mother's Younger Brother", "Mother's Brother"]

    # Father's side
    elif path.titles[0] == 'Father':

        # Aunt
        if path.goal.gender == FEMALE:

            # Elder
            if parent.compare_ages(path.goal) == -1:
                return ["Father's Elder Sister", "Father's Sister"]

             # Younger
            elif parent.compare_ages(path.goal) == 1:
                return ["Father's Younger Sister", "Father's Sister"]

            # Unknown Age
            else:
                return ["Father's Elder Sister", "Father's Younger Sister", "Father's Sister"]

        # Uncle
        elif path.goal.gender == MALE:

            # Elder
            if parent.compare_ages(path.goal) == -1:
                return ["Father's Elder Brother", "Father's Brother"]

             # Younger
            elif parent.compare_ages(path.goal) == 1:
                return ["Father's Younger Brother", "Father's Brother"]

            # Unknown Age
            else:
                return ["Father's Elder Brother", "Father's Younger Brother", "Father's Brother"]

        # Either gender
        else:

            # Elder
            if parent.compare_ages(path.goal) == -1:
                return ["Father's Elder Sister", "Father's Sister",
                        "Father's Elder Brother", "Father's Brother"]

             # Younger
            elif parent.compare_ages(path.goal) == 1:
                return ["Father's Younger Sister", "Father's Sister",
                        "Father's Younger Brother", "Father's Brother"]

            # Unknown Age
            else:
                return ["Father's Elder Sister", "Father's Younger Sister", "Father's Sister",
                        "Father's Elder Brother", "Father's Younger Brother", "Father's Brother"]

    # Parent gender not specified
    else:
        # Aunt
        if path.goal.gender == FEMALE:

            # Elder
            if parent.compare_ages(path.goal) == -1:
                return ["Mother's Elder Sister", "Mother's Sister",
                        "Father's Elder Sister", "Father's Sister"]

             # Younger
            elif parent.compare_ages(path.goal) == 1:
                return ["Mother's Younger Sister", "Mother's Sister",
                        "Father's Younger Sister", "Father's Sister"]

            # Unknown Age
            else:
                return ["Mother's Elder Sister", "Mother's Younger Sister", "Mother's Sister",
                        "Father's Elder Sister", "Father's Younger Sister", "Father's Sister"]

        # Uncle
        elif path.goal.gender == MALE:

            # Elder
            if parent.compare_ages(path.goal) == -1:
                return ["Mother's Elder Brother", "Mother's Brother",
                        "Father's Elder Brother", "Father's Brother"]

             # Younger
            elif parent.compare_ages(path.goal) == 1:
                return ["Mother's Younger Brother", "Mother's Brother",
                        "Father's Younger Brother", "Father's Brother"]

            # Unknown Age
            else:
                return ["Mother's Elder Brother", "Mother's Younger Brother", "Mother's Brother",
                        "Father's Elder Brother", "Father's Younger Brother", "Father's Brother"]

        # Either gender
        else:

            # Elder
            if parent.compare_ages(path.goal) == 1:
                return ["Mother's Elder Sister", "Mother's Sister",
                        "Mother's Elder Brother", "Mother's Brother",
                        "Father's Elder Sister", "Father's Sister",
                        "Father's Elder Brother", "Father's Brother"]

             # Younger
            elif parent.compare_ages(path.goal) == -1:
                return ["Mother's Younger Sister", "Mother's Sister",
                        "Mother's Younger Brother", "Mother's Brother",
                        "Father's Younger Sister", "Father's Sister",
                        "Father's Younger Brother", "Father's Brother"]

            # Unknown Age
            else:
                return ["Mother's Elder Sister", "Mother's Younger Sister", "Mother's Sister",
                        "Mother's Elder Brother", "Mother's Younger Brother", "Mother's Brother",
                        "Father's Elder Sister", "Father's Younger Sister", "Father's Sister",
                        "Father's Elder Brother", "Father's Younger Brother", "Father's Brother"]

