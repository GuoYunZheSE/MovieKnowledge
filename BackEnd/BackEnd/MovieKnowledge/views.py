from django.shortcuts import render

# Create your views here.
import os

from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .QA import endpoint,question2sparql

file_path = os.path.split(os.path.realpath(__file__))[0]
endpoint_url = settings.ENDPOINT_URL
extern_data = settings.EXTERN_DATA

SPARQL_PREXIX = u"""
    PREFIX : <http://www.movieknowledge.com#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""


SPARQL_SELECT_TEM = '''
            {prefix}
            SELECT DISTINCT {select} WHERE {{
                {expression}
                {filter}
            }}
            {pagination}
'''
SPARQL_COUNT_TEM = u"{prefix}\n" + \
             u"SELECT COUNT({select}) WHERE {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

SPARQL_ASK_TEM = u"{prefix}\n" + \
             u"ASK {{\n" + \
             u"{expression}\n" + \
             u"}}\n"

class QAInterface:
    def __init__(self):
        # TODO 连接Fuseki服务器。
        self.fuseki = endpoint.JenaFuseki(endpoint_url)
        # TODO 初始化自然语言到SPARQL查询的模块，参数是外部词典列表。
        self.q2s = question2sparql.Question2Sparql(extern_data)

    def answer(self, question: str):
        my_query = self.q2s.get_sparql(question)
        if my_query is not None:
            result = self.fuseki.get_sparql_result(my_query)
            value = self.fuseki.get_sparql_result_value(result)
            print(F"SPARQL:{my_query}")
            # TODO 判断结果是否是布尔值，是布尔值则提问类型是"ASK"，回答“是”或者“不知道”。
            if isinstance(value, bool):
                if value is True:
                    ans = "Yes"
                else:
                    ans = "I don't know this question's answer yet."
            else:
                # TODO 查询结果为空，根据OWA，回答“不知道”
                if len(value) == 0:
                    ans = "I don't know this question's answer yet."
                elif len(value) == 1:
                    ans = value[0]
                else:
                    output = ''
                    for v in value:
                        output += v + u'、'
                    ans = output[0:-1]

        else:
            # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
            ans = "I can not understand what you said"

        return ans


qa_interface = QAInterface()


class Answer(APIView):
    def post(self, request):
        res = {
            "code": 200,
        }
        try:
            ques = request.data.get('message', None)
            print(ques)
            ans = qa_interface.answer(ques)
            if not ans:
                ans = "I don't know this question's answer yet."
            res['answer'] = ans
        except Exception as e:
            res["code"] = -1
            res["mesg"] = f"回答失败, {e}"
        return Response(res)

class QueryActor(APIView):
    def get(self, request):
        personEnglishName = request.query_params.get('personEnglishName', None)

        expression = '''
        ?x :personEnglishName ?personEnglishName .\n
        optional
        {
        ?x :PersonBirthDay ?PersonBirthDay.
        ?x :personDeathDay ?personDeathDay.
        ?x :personBiography ?personBiography.
        ?x :personBirthPlace ?personBirthPlace.
        }
        '''
        ordering = request.query_params.get('sort')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', -1)
        if ordering and page and limit:
            if ordering[0]=="-":
                pagination = f"ORDER BY DESC(?{ordering[1:]}) LIMIT {limit} OFFSET {(int(page) - 1) * int(limit)}"
            else:
                pagination = f"ORDER BY ?{ordering[1:]} LIMIT {limit} OFFSET {(int(page) - 1) * int(limit)}"
        else:
            pagination = ""

        filter = ""
        if personEnglishName:
            filter = f"FILTER (?personEnglishName ='{personEnglishName}')\n"


        query_total = SPARQL_SELECT_TEM.format(select="*",prefix=SPARQL_PREXIX,expression=expression,pagination="",filter=filter)
        query = SPARQL_SELECT_TEM.format(select="*",prefix=SPARQL_PREXIX,expression=expression,pagination=pagination,filter=filter)
        print(query)
        default_params = ["personEnglishName","PersonBirthDay","personDeathDay","personBiography","personBirthPlace"]

        all_result = qa_interface.fuseki.get_sparql_result(query_total)["results"]
        count = len(all_result["bindings"])

        fuseki_results = qa_interface.fuseki.get_sparql_result(query)["results"]
        items = []
        id = 1
        for each in fuseki_results["bindings"]:
            # "personEnglishName": {
            #     "type": "literal",
            #     "value": "Justin Pierce"
            # },
            # "PersonBirthDay": {
            #     "type": "literal",
            #     "value": "1975-03-21"
            # },
            item_dic = {}
            item_dic.setdefault("id",(int(page) - 1) * int(limit) + id)
            id += 1
            for param in default_params:
                if each.__contains__(param):
                    item_dic.setdefault(param,each[param]["value"])
                else:
                    item_dic.setdefault(param, "None")
            items.append(item_dic)
        res = {
            "code": 200,
            "items":items,
            "total":count
        }
        return Response(res)

class QueryMovie(APIView):
    def get(self, request):
        genre = request.query_params.get('genre', None)
        movieTitle = request.query_params.get('movieTitle', None)
        if genre:
            expression = f" ?x :movieTitle ?movieTitle .\n " \
                         f" ?x :hasGenre ?g. \n" \
                         f" ?g :genreName '{genre}'. \n"
        else:
            expression = f" ?x :movieTitle ?movieTitle .\n "
        optional = '''
          optional
          {
            ?x :movieReleaseDate ?movieReleaseDate.
            ?x :movieRating ?movieRating.
            ?x :movieIntroduction ?movieIntroduction.
          }
        '''
        expression += optional
        ordering = request.query_params.get('sort')
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', -1)
        if ordering and page and limit:
            if ordering[0]=="-":
                pagination = f"ORDER BY DESC(?{ordering[1:]}) LIMIT {limit} OFFSET {(int(page) - 1) * int(limit)}"
            else:
                pagination = f"ORDER BY ?{ordering[1:]} LIMIT {limit} OFFSET {(int(page) - 1) * int(limit)}"
        else:
            pagination = ""

        filter = ""
        if movieTitle:
            filter = f"FILTER (?movieTitle ='{movieTitle}')\n"
        query_total = SPARQL_SELECT_TEM.format(select="*",prefix=SPARQL_PREXIX,expression=expression,pagination="",filter=filter)
        query = SPARQL_SELECT_TEM.format(select="*",prefix=SPARQL_PREXIX,expression=expression,pagination=pagination,filter=filter)
        print(query)
        default_params = ["movieTitle","movieReleaseDate","movieRating","movieIntroduction"]

        all_result = qa_interface.fuseki.get_sparql_result(query_total)["results"]
        count = len(all_result["bindings"])

        fuseki_results = qa_interface.fuseki.get_sparql_result(query)["results"]
        items = []
        id = 1
        for each in fuseki_results["bindings"]:
            item_dic = {}
            item_dic.setdefault("id",(int(page) - 1) * int(limit) + id)
            id += 1
            for param in default_params:
                if each.__contains__(param):
                    if param == 'movieRating':
                        item_dic.setdefault(param,each[param]["value"][0:3])
                    else:
                        item_dic.setdefault(param, each[param]["value"])
                else:
                    item_dic.setdefault(param, "None")
            items.append(item_dic)
        res = {
            "code": 200,
            "items":items,
            "total":count
        }
        return Response(res)

if __name__ == '__main__':
    while True:
        question = input(">> 请输入问题：")
        ans = qa_interface.answer(question)
        print(ans)
        print('#' * 100)
