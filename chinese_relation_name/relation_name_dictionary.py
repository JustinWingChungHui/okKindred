from json import JSONEncoder

class RelationName():

    def __init__(self, name, cantonese, cantonese_pronounciation, mandarin, mandarin_pronounciation):

        self.name = name

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


class RelationNameEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, RelationName):
            return obj.__dict__
        #Let the base class handle the problem.
        return JSONEncoder.default(self, obj)


'''
https://omniglot.com/language/kinship/cantonese.htm
https://en.wikipedia.org/wiki/Chinese_kinship
https://www.oakton.edu/user/4/billtong/chinaclass/chinesekin.htm
https://www.italki.com/article/183/complete-list-of-titles-for-family-members-in-chinese?hl=en
'''
relation_names = [
    # 1 relation apart
    RelationName('Mother',
                ['母親', '媽媽', '阿媽', '媽咪', '老母'],
                ['mou5 can1','maa4 maa1', 'aa3 maa1', 'maa1 mi4', 'lou5 mou2'],
                '妈妈',
                'māmā'),

    RelationName('Father',
                ['父親', '爸爸', '阿爸'],
                ['fu6 can1', 'baa4 baa1', 'aa3 baa1'],
                '爸爸',
                'bàba'),

    RelationName('Daughter', '女', 'neoi5', ['女儿', '闺女'], ["nǚ'ér", "guī nǚ"]),

    RelationName('Son', '仔', 'zai2', '儿子', 'érzi'),

    RelationName('Wife',
                ['太太','妻子','老婆'],
                ['taai3 taai2', 'cai1 zi2', 'lou5 po4'],
                '老婆', 'lǎopó'),

    RelationName('Husband',
                ['先生','丈夫','老公'],
                ['sin1 saang1', 'zoeng6 fu1', 'lou5 gung1'],
                '老公', 'lǎogōng'),

    # Grandparents
    RelationName('Maternal Grandmother',
                ['婆婆', '外婆', '阿婆'],
                ['po4 po2', 'ngoi6 po4', 'aa3 po4'],
                '姥姥',  'lǎolao'),

    RelationName('Maternal Grandfather',
                ['公公', '外公', '阿公'],
                ['gung1 gung1', 'ngoi6 gung1', 'aa3 gung1'],
                '姥爷',  'lǎoyé'),

    RelationName('Paternal Grandmother',
                ['嫲嫲', '阿嫲'],
                ['maa4 maa4', 'aa3 maa4'],
                '奶奶',  'nǎinai'),

    RelationName('Paternal Grandfather',
                ['爺爺', '阿爺'],
                ['je4 je4', 'aa3 je4'],
                '爷爷',  'yéye'),

    # Stepparents
    # Same as Mother
    RelationName('Stepmother',
                ['母親', '媽媽', '阿媽', '媽咪', '老母'],
                ['mou5 can1','maa4 maa1', 'aa3 maa1', 'maa1 mi4', 'lou5 mou2'],
                '妈妈',
                'māmā'),

    # Same as Father
    RelationName('Stepfather',
                ['父親', '爸爸', '阿爸'],
                ['fu6 can1', 'baa4 baa1', 'aa3 baa1'],
                '爸爸',
                'bàba'),

    # Siblings
    RelationName('Elder Sister',
                ['家姐', '姐姐'],
                ['gaa1 ze2', 'ze2 ze2'],
                ['姊姊', '姐姐'],
                ['zǐzi', 'jiějie']),

    RelationName('Younger Sister',
                ['家姐', '姐姐'],
                ['mui6 mui6', 'sai3 mui6'],
                '妹妹',
                'mèimèi'),

    RelationName('Elder Brother',
                ['哥哥', '大佬'],
                ['go1 go1', 'daai6 lou2'],
                '哥哥',
                'gēge'),

    RelationName('Younger Brother',
                ['弟弟', '細佬'],
                ['dai6 dai6', 'sai3 lou2'],
                '弟弟',
                'dìdi'),

    # Parents in Law
    RelationName("Wife's Mother",
                ['外母', '岳母'],
                ['ngoi6 mou5', 'ngok6 mou5'],
                ['丈母', '外母'],
                ['zhàng mǔ', 'wài mǔ']),

    RelationName("Wife's Father",
                ['外父', '岳父'],
                ['ngoi6 fu6', 'ngok6 fu6'],
                ['岳丈', '外父'],
                ['yuè zhàng', 'wài fù']),

    RelationName("Husband's Mother",
                ['奶奶', '家婆'],
                ['naai5 naai5', 'gaa1 po4' ],
                ['家姑', '家婆', '奶奶'],
                ['jiā gū', 'jiā pó', 'nǎi nai']),

    RelationName("Husband's Father",
                '老爺',
                'lou5 je4 ',
                ['家公', '老爺'],
                ['jiā gōng', 'lǎo yé']),

    # Stepchildren
    # same as children
    RelationName('Stepdaughter', '女', 'neoi5', ['女儿', '闺女'], ["nǚ'ér", "guī nǚ"]),
    RelationName('Stepson', '仔', 'zai2', '儿子', 'érzi'),

    # Children In Law
    RelationName("Daughter In Law", '新抱', 'san1 pou5', '媳婦', 'xí fù'),
    RelationName("Son In Law", '女婿', 'neoi5 sai3', '女婿', 'nǚ xu'),

    # Grandchildren
    RelationName("Granddaughter Daughter's Side", '外孫女', 'ngoi6 syun1 neoi5', '外孫女', 'wài sūn nǚ'),
    RelationName("Grandson Daughter's Side", '外孫', 'ngoi6 syun', '外孫仔', 'wài sūn zǎi'),
    RelationName("Granddaughter Son's Side", '孫女', 'syun1 neoi5', '孫女', 'sūn nǚ'),
    RelationName("Grandson Son's Side", '孫', 'syun1', '孫兒', 'sūn ér'),

    # Great Grandparents
    RelationName('Maternal Great Grandmother', '太婆', 'taai3 po2', '太姥姥',  'tài lǎo lao'),
    RelationName('Maternal Great Grandfather', '太公', 'taai3 gung1', '太姥爷',  'tài lǎo ye'),
    RelationName("Paternal Great Grandmother", '太嫲', 'taai3 maa4', '太太', 'tài tai'),
    RelationName("Paternal Great Grandfather", '太爺', 'taai3 je4', '太爷', 'tài yé'),

    # Aunts and Uncles
    RelationName("Mother's Elder Sister", '姨媽', 'ji4 maa1', '姨妈', 'yímā'),
    RelationName("Mother's Younger Sister", '阿姨', 'aa3 ji4', '阿姨', 'āyí'),
    RelationName("Mother's Sister", '姨姨', 'ji4 ji4', '姨', 'yí'),
    RelationName("Mother's Brother", '舅父', 'kau5 fu6', '舅舅', 'jiùjiu'),


    RelationName("Father's Elder Sister", '姑媽', 'gu1 maa1', '姑妈', 'gūmā'),
    RelationName("Father's Younger Sister", '姑姐', 'gu1 ze2 ', '', ''),
    RelationName("Father's Sister", '阿姑', 'aa3 gu1', '姑姑', 'gūgu'),
    RelationName("Father's Elder Brother", ['阿伯','伯父'], ['aa3 baak3','baak3 fu6'] , '伯伯', 'bóbo'),
    RelationName("Father's Younger Brother", ['阿叔','叔父'], ['aa3 suk1','suk1 fu6'], '叔叔', 'shūshu'),


    # Sibling's partner
    RelationName("Elder Sibling's Wife", '阿嫂', 'aa3 sou2', '嫂', 'sǎo'),
    RelationName("Younger Sibling's Wife", '姑奶', 'gu1 naai5', '弟婦', 'dì fù'),
    RelationName("Elder Sibling's Husband", '姐夫', 'ze2 fu1', '姐夫', 'jiě fu'),
    RelationName("Younger Sibling's Husband", '妹夫', 'mui6 fu1', '姐夫', 'mèi fu'),

    # Nieces/ Nephews
    RelationName("Sister's Daughter", '外甥女', 'ngoi6 saang1 neoi5', '外甥女', 'wài sheng nǚ'),
    RelationName("Sister's Son", '外甥', 'ngoi6 saang1', '外甥女', 'wài shēng'),
    RelationName("Brother's Daughter", '侄女', 'zat6 neoi5', '姪女', 'zhí nǚ'),
    RelationName("Brother's Son", '侄', 'zat6', '姪仔', 'zhí zǎi'),


    # Brother/Sister in Law
    RelationName("Wife's Elder Sister", '大姨', 'daai6 ji4', '大姨', 'dà yí'),
    RelationName("Wife's Younger Sister", '姨仔', 'ji4 zai2', '小姨', 'xiǎo yí'),
    RelationName("Wife's Elder Brother", '大舅', 'daai6 kau5', '大舅', 'dà jiù'),
    RelationName("Wife's Younger Brother", '舅仔', 'kau5 zai2', '小舅', 'xiǎo jiù'),
    RelationName("Husband's Elder Sister", '姑奶', 'gu1 naai5', '大姑', 'dà gū'),
    RelationName("Husband's Younger Sister", '姑仔', 'gu1 zai2', '小姑', 'xiǎo gū'),
    RelationName("Husband's Elder Brother", '大伯', 'daai6 baa3', '大伯', 'dà bó'),
    RelationName("Husband's Younger Brother", '叔仔', 'suk1 zai2', '小叔', 'xiǎo shū'),

    # 1st Cousins
    RelationName("Maternal Elder Female Cousin", '表姐', 'biu2 ze2', '表姐', 'biǎojiě'),
    RelationName("Maternal Younger Female Cousin", '表妹', 'biu2 mui6', '表妹', 'biǎomèi'),
    RelationName("Maternal Elder Male Cousin", '表哥', 'biu2 go1', '表哥', 'biǎogē'),
    RelationName("Maternal Younger Male Cousin", '表弟', 'biu2 dai6', '表弟', 'biǎodì'),
    RelationName("Paternal Elder Female Cousin", '堂家姐', 'tong4 gaa1 ze2', ['堂姊', '堂姐'], ['tángzǐ', 'tángjiě']),
    RelationName("Paternal Younger Female Cousin", '堂細妹', 'tong4 sai3 mui6', '堂妹', 'tángmèi'),
    RelationName("Paternal Elder Male Cousin", '堂阿哥', 'tong4 aa3 go1', ['堂兄', '堂哥'], ['tángxiōng', 'tánggē']),
    RelationName("Paternal Younger Male Cousin", '堂細佬', 'tong4 sai3 lou2', '堂弟', 'tángdì'),
]


def get_relation_names_by_name():
    result = {}
    for r in relation_names:
        result[r.name] = r

    return result

def get_relation_names(names):
    results = []

    for r in relation_names:
        if r.name in names:
            results.append(r)

    return results




