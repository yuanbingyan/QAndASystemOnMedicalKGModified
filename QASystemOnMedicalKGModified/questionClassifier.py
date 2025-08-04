import os
import ahocorasick # This module's name is pyahocorasick

'''
class PathManager:
    def __init__(self, cur_dir, config_file):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)

        self.paths = {name: os.path.join(cur_dir, path) for name, path in config['paths'].items()}

    def get_path(self, feature_name):
        return self.paths.get(feature_name)
'''

class QuestionClassifier:
    def __init__(self):
        # Gain the current absolute path of the script
        '''
            __file__ is a special variable, represents current
            script's path;
            os.path.abspath(__file__) gains current script's absolute
            path;
            .split('/') splits the path string into a list by '/';
            '/'.join(...) joins the slice list into a string, i.e., the path.
        '''
        # cur_dir = '/'.join(os.path.abspath(__file__).split('/'))

        '''
            In windows operation system, the path split character is '\', so the
            code above could encounter question.(In fact, it doesn't encounter a 
            problem). To make sure cross-platform compatibility, we could use os.path.dirname
            instead.
        '''
        # gain the absolute path of the current script
        # script_path = os.path.abspath(__file__)

        # gain the directory path
        # cur_dir = os.path.dirname(script_path)

        # The path of characteristic words
        # config_file = 'D:\document\internship\SoftwareCenterOfTheChineseAcademyOfSciences\QASystemOnMedicalKGReproduction\characteristicWordPath.yaml'
        # path_manager = PathManager(cur_dir, config_file)
        # disease_path = path_manager.get_path('disease')

        # debug
        # print(disease_path)
        # debug
        # print("currentDirectory: ", cur_dir)

        # load the characteristic word's path
        cur_dir = '/'.join(os.path.abspath(__file__).split('/')[:-1])

        # The characteristic words' path
        self.disease_path = os.path.join(cur_dir, 'dict/disease.txt')
        self.department_path = os.path.join(cur_dir, 'dict/department.txt')
        self.check_path = os.path.join(cur_dir, 'dict/check.txt')
        self.drug_path = os.path.join(cur_dir, 'dict/drug.txt')
        self.food_path = os.path.join(cur_dir, 'dict/food.txt')
        self.producer_path = os.path.join(cur_dir, 'dict/producer_path.txt')
        self.symptom_path = os.path.join(cur_dir, 'dict/symptom.txt')
        self.deny_path = os.path.join(cur_dir, 'dirc/deny.txt')

        # load characteristic words
        # 1. open(self.disease_path, encoding='utf-8')
        # 2. [i.strip() for i in ... if i.strip()]
        self.disease_wds = [i.strip() for i in open(self.disease_path, encoding='utf-8') if i.strip()]
        self.department_wds= [i.strip() for i in open(self.department_path, encoding='utf-8') if i.strip()]
        self.check_wds= [i.strip() for i in open(self.check_path, encoding='utf-8') if i.strip()]
        self.drug_wds= [i.strip() for i in open(self.drug_path, encoding='utf-8') if i.strip()]
        self.food_wds= [i.strip() for i in open(self.food_path, encoding='utf-8') if i.strip()]
        self.producer_wds= [i.strip() for i in open(self.producer_path, encoding='utf-8') if i.strip()]
        self.symptom_wds= [i.strip() for i in open(self.symptom_path, encoding='utf-8') if i.strip()]

        self.region_words = set(self.department_wds + self.disease_wds + self.check_wds + self.drug_wds + self.food_wds + self.producer_wds + self.symptom_wds)

        self.deny_words = [i.strip() for i in open(self.deny_path, encoding='utf-8') if i.strip()]

        # build field actree(Aho-Corasick tree)
        self.region_tree = self.buildActree(list(self.region_words)) # ?

        # build dictionary
        self.wdtype_dict = self.buildWdtypeDict() # ?
        # 这个地方的逻辑还不清楚，需要再返回分析。

        # interrogative words
        self.symptom_qwds = ['症状', '表征', '现象', '症候', '表现']
        self.cause_qwds = ['原因', '成因', '为什么', '怎么会', '怎样才', '咋样才', '怎样会', '如何会', '为啥', '为何',
                           '如何才会', '怎么才会', '会导致', '会造成']
        self.acompany_qwds = ['并发症', '并发', '一起发生', '一并发生', '一起出现', '一并出现', '一同发生', '一同出现',
                              '伴随发生', '伴随', '共现']
        self.food_qwds = ['饮食', '饮用', '吃', '食', '伙食', '膳食', '喝', '菜', '忌口', '补品', '保健品', '食谱',
                          '菜谱', '食用', '食物', '补品']
        self.drug_qwds = ['药', '药品', '用药', '胶囊', '口服液', '炎片']
        self.prevent_qwds = ['预防', '防范', '抵制', '抵御', '防止', '躲避', '逃避', '避开', '免得', '逃开', '避开',
                             '避掉', '躲开', '躲掉', '绕开',
                             '怎样才能不', '怎么才能不', '咋样才能不', '咋才能不', '如何才能不',
                             '怎样才不', '怎么才不', '咋样才不', '咋才不', '如何才不',
                             '怎样才可以不', '怎么才可以不', '咋样才可以不', '咋才可以不', '如何可以不',
                             '怎样才可不', '怎么才可不', '咋样才可不', '咋才可不', '如何可不']
        self.lasttime_qwds = ['周期', '多久', '多长时间', '多少时间', '几天', '几年', '多少天', '多少小时', '几个小时',
                              '多少年']
        self.cureway_qwds = ['怎么治疗', '如何医治', '怎么医治', '怎么治', '怎么医', '如何治', '医治方式', '疗法',
                             '咋治', '怎么办', '咋办', '咋治']
        self.cureprob_qwds = ['多大概率能治好', '多大几率能治好', '治好希望大么', '几率', '几成', '比例', '可能性',
                              '能治', '可治', '可以治', '可以医']
        self.easyget_qwds = ['易感人群', '容易感染', '易发人群', '什么人', '哪些人', '感染', '染上', '得上']
        self.check_qwds = ['检查', '检查项目', '查出', '检查', '测出', '试出']
        self.belong_qwds = ['属于什么科', '属于', '什么科', '科室']
        self.cure_qwds = ['治疗什么', '治啥', '治疗啥', '医治啥', '治愈啥', '主治啥', '主治什么', '有什么用', '有何用',
                          '用处', '用途',
                          '有什么好处', '有什么益处', '有何益处', '用来', '用来做啥', '用来作甚', '需要', '要']

        print('model init finished ...')

        return

    '''
        Classifier main function
    '''
    def classify(self, question):
        data = {}
        medical_dict = self.checkMedical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict

        # collect the class type involved in the question sentence.
        types = []
        for type_ in medical_dict.values():
            types += type_
        question_type = 'others'

        question_types = []

        # symptom
        if self.check_words(self.symptom_qwds, question) and ('disease' in types):
            question_type = 'disease_symptom'
            question_types.append(question_type)

        if self.check_words(self.symptom_qwds, question) and ('symptom' in types):
            question_type = 'symptom_disease'
            question_types.append(question_type)

        # reason
        if self.check_words(self.cause_qwds, question) and ('disease' in types):
            question_type = 'disease_cause'
            question_types.append(question_type)

        # complication
        if self.check_words(self.acompany_qwds, question) and ('disease' in types):
            question_type = 'disease_acompany'
            question_types.append(question_type)

        # recommendation food
        if self.check_words(self.food_qwds, question) and ('disease' in types):
            deny_status = self.check_words(self.deny_words, question)
            if deny_status:
                question_type = 'disease_not_food'
            else:
                question_type = 'disease_do_food'
            question_types.append(question_type)

        # Given the food to find the disease
        if self.check_words(self.food_qwds + self.cure_qwds, question) and ('food' in types):
            deny_status = self.

        '''build the word corresponding type'''
        def buildWdtypeDict(self):
            wdDict = dict()
            for wd in self.region_words:

        '''
            build Actree, accelerate the filtering.
        '''
        def buildActree(self, wordlist):
            actree = ahocorasick.Automaton()
            for index, word in enumerate(wordlist):
                actree.add_word(word, (index, word))
            actree.make_automaton()
            return actree

        '''
            question sentence filtering
        '''
        def checkMedical(self, question):

            region_wds = []
            for i in self.region_tree.iter(question):
                wd = i[1][1]
                region_wds.append(wd)

            stop_wds = []
            for wd1 in region_wds:
                for wd2 in region_wds:
                    if wd1 in wd2 and wd1 != wd2:
                        stop_wds.append(wd1)
            final_wds = [i for i in region_wds if i not in stop_wds]
            final_dict = {i:self.wdtype_dict.get(i) for i in final_wds}

            return final_dict

        '''
            Classify based on the characteristic word.
        '''
        def check_words(self, wds, sent):
            for wd in wds:
                if wd in sent:
                    return True
            return False

if __name__ == '__main__':
    handler = QuestionClassifier()
    while 1:
        question = input('input a question: ')
        data = handler.classify(question)
        print(data)