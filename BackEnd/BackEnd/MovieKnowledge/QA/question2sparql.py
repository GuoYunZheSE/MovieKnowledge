# @Date    : 12:42 01/28/2022
# @Author  : ClassicalPi
# @FileName: question2sparql.py
# @Software: PyCharm
from . import questions, word


class Question2Sparql:
    def __init__(self, dict_paths:list):
        self.tw = word.Tagger(True, dict_paths)
        self.rules = questions.rules

    def get_sparql(self, question):
        """
        进行语义解析，找到匹配的模板，返回对应的SPARQL查询语句
        :param question:
        :return:
        """
        word_objects = self.tw.get_word_objects(question)
        for w in word_objects:
            print(w.token,w.pos)
        queries_dict = dict()

        for rule in self.rules:
            query, num = rule.apply(word_objects)

            if query is not None:
                queries_dict[num] = query

        if len(queries_dict) == 0:
            return None
        elif len(queries_dict) == 1:
            return list(queries_dict.values())[0]
        else:
            # TODO 匹配多个语句，以匹配关键词最多的句子作为返回结果
            sorted_dict = sorted(queries_dict.items(), key=lambda item: item[0], reverse=True)
            return sorted_dict[0][1]