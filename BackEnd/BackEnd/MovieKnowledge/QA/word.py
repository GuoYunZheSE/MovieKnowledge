# @Date    : 00:18 01/28/2022
# @Author  : ClassicalPi
# @FileName: word.py
# @Software: PyCharm
import spacy
import json

from spacy.pipeline import EntityRuler


class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos


class Tagger:
    def __init__(self, train:bool, extern_data:list):
        self.nlp = spacy.load("en_core_web_sm")
        if train:
            for data in extern_data:
                file = data["Path"]
                label = data["Label"]
                pattern = data["Pattern"]
                self.train_ER(file,label,pattern)

    def train_ER(self, file_path: str, entity_type: str, entity_pattern):
        # 创建一个ruler，它将被加到模型上
        ruler = EntityRuler(self.nlp, overwrite_ents=True)
        jsonData = None
        with open(file_path) as f:
            jsonData = json.load(f)
        # 定义一个查找模式并加入ruler
        patterns = [{"label": entity_type, "pattern": each[entity_pattern]} for each in jsonData]
        ruler.add_patterns(patterns)
        ruler.name = f"{entity_type}_ruler"
        self.nlp.add_pipe(ruler)
    def get_word_objects(self, sentence):
        # type: (str) -> list
        """
        把自然语言转为Word对象
        :param sentence:
        :return:
        """
        res = []
        doc = self.nlp(sentence)
        res.extend([Word(ent.text, ent.label_) for ent in doc.ents])
        used = set()
        for ent in doc.ents:
            for each in ent.text.split(" "):
                used.add(each)
        # res.extend([Word(nc.text, "Noun Chunk") for nc in doc.noun_chunks])
        res.extend([Word(token.text, token.pos_) for token in doc if token.text not in used])
        return res


# TODO 用于测试
if __name__ == '__main__':
    EXTERN_DATA = [
        {
            "Path": "/Users/lucas/Projects/Pycharm/MovieKnowledge/Data/MovieKnowledge_person.json",
            "Label": "Person",
            "Pattern": "person_english_name"
        },
        {
            "Path": "/Users/lucas/Projects/Pycharm/MovieKnowledge/Data/MovieKnowledge_movie.json",
            "Label": "Film",
            "Pattern": "movie_title"
        }
    ]
    tagger = Tagger(True,EXTERN_DATA)
    while True:
        s = input('>>')
        for i in tagger.get_word_objects(s):
            print(i.token, i.pos)
