
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



relation_names = {
    'Mother':   RelationName(['母親', '媽媽', '阿媽', '媽咪', '老母'],
                            ['mou5 can1','maa4 maa1', 'aa3 maa1', 'maa1 mi4', 'lou5 mou2'],
                            ['妈妈'],
                            ['māmā']),

    'Father':   RelationName(['父親', '爸爸', '阿爸'],
                            ['fu6 can1', 'baa4 baa1', 'aa3 baa1'],
                            ['爸爸'],
                            ['bàba']),

    'Daughter': RelationName('女', 'neoi5', ['女儿', '闺女'], ["nǚ'ér", "guī nǚ"]),

    'Son':      RelationName('仔', 'zai2', '儿子', 'érzi'),

    'Wife':     RelationName(['太太','妻子','老婆'],
                            ['taai3 taai2', 'cai1 zi2', 'lou5 po4'],
                            '老婆', 'lǎopó'),

    'Husband':  RelationName(['先生','丈夫','老公'],
                            ['sin1 saang1', 'zoeng6 fu1', 'lou5 gung1'],
                            '老公', 'lǎogōng'),
}









