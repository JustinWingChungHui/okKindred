
class RelationName():

    def __init__(self, cantonese, cantonese_pronounciation, mandarin, mandarin_pronounciation):

        if isinstance(cantonese, list):
            self.cantonese = cantonese
        else:
            self.cantonese = [cantonese]

        if isinstance(cantonese_pronounciation, list):
            self.cantonese_pronounciation = cantonese_pronounciation
        else:
            self.cantonese_pronounciation = [cantonese_pronounciation]

        if isinstance(mandarin, list):
            self.mandarin = mandarin
        else:
            self.mandarin = [mandarin]

        if isinstance(mandarin_pronounciation, list):
            self.mandarin_pronounciation = mandarin_pronounciation
        else:
            self.mandarin_pronounciation = [mandarin_pronounciation]

'''
https://omniglot.com/language/kinship/cantonese.htm
https://en.wikipedia.org/wiki/Chinese_kinship
https://www.oakton.edu/user/4/billtong/chinaclass/chinesekin.htm
https://www.italki.com/article/183/complete-list-of-titles-for-family-members-in-chinese?hl=en
'''
relation_names = {
    # 1 relation apart
    'Mother':   RelationName(['母親', '媽媽', '阿媽', '媽咪', '老母'],
                            ['mou5 can1','maa4 maa1', 'aa3 maa1', 'maa1 mi4', 'lou5 mou2'],
                            '妈妈',
                            'māmā'),

    'Father':   RelationName(['父親', '爸爸', '阿爸'],
                            ['fu6 can1', 'baa4 baa1', 'aa3 baa1'],
                            '爸爸',
                            'bàba'),

    'Daughter': RelationName('女', 'neoi5', ['女儿', '闺女'], ["nǚ'ér", "guī nǚ"]),

    'Son':      RelationName('仔', 'zai2', '儿子', 'érzi'),

    'Wife':     RelationName(['太太','妻子','老婆'],
                            ['taai3 taai2', 'cai1 zi2', 'lou5 po4'],
                            '老婆', 'lǎopó'),

    'Husband':  RelationName(['先生','丈夫','老公'],
                            ['sin1 saang1', 'zoeng6 fu1', 'lou5 gung1'],
                            '老公', 'lǎogōng'),

    # Grandparents
    'Maternal Grandmother': RelationName(['婆婆', '外婆', '阿婆'],
                                        ['po4 po2', 'ngoi6 po4', 'aa3 po4'],
                                        '姥姥',  'lǎolao'),

    'Maternal Grandfather': RelationName(['公公', '外公', '阿公'],
                                        ['gung1 gung1', 'ngoi6 gung1', 'aa3 gung1'],
                                        '姥爷',  'lǎoyé'),

    'Paternal Grandmother': RelationName(['嫲嫲', '阿嫲'],
                                        ['maa4 maa4', 'aa3 maa4'],
                                        '奶奶',  'nǎinai'),

    'Paternal Grandfather': RelationName(['爺爺', '阿爺'],
                                        ['je4 je4', 'aa3 je4'],
                                        '爷爷',  'yéye'),

    # Stepparents
    # Same as Mother
    'Stepmother':   RelationName(['母親', '媽媽', '阿媽', '媽咪', '老母'],
                            ['mou5 can1','maa4 maa1', 'aa3 maa1', 'maa1 mi4', 'lou5 mou2'],
                            '妈妈',
                            'māmā'),

    # Same as Father
    'Stepfather':   RelationName(['父親', '爸爸', '阿爸'],
                            ['fu6 can1', 'baa4 baa1', 'aa3 baa1'],
                            '爸爸',
                            'bàba'),

    # Siblings
    'Elder Sister':     RelationName(['家姐', '姐姐'],
                                ['gaa1 ze2', 'ze2 ze2'],
                                ['姊姊', '姐姐'],
                                ['zǐzi', 'jiějie']),

    'Younger Sister':   RelationName(['家姐', '姐姐'],
                                ['mui6 mui6', 'sai3 mui6'],
                                '妹妹',
                                'mèimèi'),

    'Elder Brother':    RelationName(['哥哥', '大佬'],
                                ['go1 go1', 'daai6 lou2'],
                                '哥哥',
                                'gēge'),

    'Younger Brother':  RelationName(['弟弟', '細佬'],
                                ['dai6 dai6', 'sai3 lou2'],
                                '弟弟',
                                'dìdi'),

    # Parents in Law
    "Wife's Mother":    RelationName(['外母', '岳母'],
                                ['ngoi6 mou5', 'ngok6 mou5'],
                                ['丈母', '外母'],
                                ['zhàng mǔ', 'wài mǔ']),

    "Wife's Father":    RelationName(['外父', '岳父'],
                                ['ngoi6 fu6', 'ngok6 fu6'],
                                ['岳丈', '外父'],
                                ['yuè zhàng', 'wài fù']),

    "Husband's Mother": RelationName(['奶奶', '家婆'],
                                ['naai5 naai5', 'gaa1 po4' ],
                                ['家姑', '家婆', '奶奶'],
                                ['jiā gū', 'jiā pó', 'nǎi nai']),

    # Stepchildren
    # same as children
    'Stepdaughter': RelationName('女', 'neoi5', ['女儿', '闺女'], ["nǚ'ér", "guī nǚ"]),

    'Stepson':      RelationName('仔', 'zai2', '儿子', 'érzi'),

    # Children In Law
    "Daughter In Law":  RelationName('新抱', 'san1 pou5', '媳婦', 'xí fù'),

    "Son In Law":  RelationName('女婿', 'neoi5 sai3', '女婿', 'nǚ xu'),

    # Grandchildren
    "Granddaughter Daughter's Side":    RelationName('外孫女', 'ngoi6 syun1 neoi5', '外孫女', 'wài sūn nǚ'),
    "Grandson Daughter's Side":         RelationName('外孫', 'ngoi6 syun', '外孫仔', 'wài sūn zǎi'),
    "Granddaughter Son's Side":         RelationName('孫女', 'syun1 neoi5', '孫女', 'sūn nǚ'),
    "Grandson Son's Side":              RelationName('孫', 'syun', '孫兒', 'sūn ér'),

    # Great Grandparents
    'Maternal Great Grandmother': RelationName('太婆', 'taai3 po2', '太姥姥',  'tài lǎo lao'),
    'Maternal Great Grandfather': RelationName('太公', 'taai3 gung1', '太姥爷',  'tài lǎo ye'),
    "Paternal Great Grandmother": RelationName('太嫲', 'taai3 maa4', '太太', 'tài tai'),
    "Paternal Great Grandfather": RelationName('太爺', 'taai3 je4', '太爷', 'tài yé'),

    # Aunts and Uncles
    "Mother's Elder Sister":    RelationName('姨媽', 'ji4 maa1', '姨妈', 'yímā'),
    "Mother's Younger Sister":  RelationName('阿姨', 'aa3 ji4', '阿姨', 'āyí'),
    "Mother's Sister":          RelationName('姨姨', 'ji4 ji4', '姨', 'yí'),
    "Mother's Brother":         RelationName('舅父', 'kau5 fu6', '舅舅', 'jiùjiu'),
    "Father's Elder Sister":    RelationName('姑媽', 'gu1 maa1', '姑妈', 'gūmā'),
    "Father's Younger Sister":    RelationName('姑姐', 'gu1 ze2 ', '', ''),
    "Father's Sister":    RelationName('阿姑', 'aa3 gu1', '姑姑', 'gūgu'),
}









