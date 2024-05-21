import random
from django.http import JsonResponse
from rest_framework.views import  APIView
from snownlp import SnowNLP

from database import models






class ApiBar(APIView):

    def get(self, request):

        data = {}
        try:
            find_obj = models.ReqeustsData.objects.order_by("id")
            res_text = ""
            for obj in find_obj:
                res_text = res_text + obj.name + "," + obj.comment + ","
            # 词性分析
            cixing_list = []
            for key, item in self.dict_speech(res_text).items():
                if item:
                    dict = {}
                    dict['name'] = key
                    dict['value'] = len(item)
                    cixing_list.append(dict)
            data['res_list'] = cixing_list

            data['code'] = 200
            return JsonResponse(data)

        except Exception as e:
            # print(e)
            data['code'] = 444
            return JsonResponse(data)


    # 词性
    def dict_speech(self,text):
        cixing_table = {
            "名词": [],
            "时间词": [],
            "处所词": [],
            "方位词": [],
            "动词": [],
            "形容词": [],
            "区别词": [],
            "状态词": [],
            "数词": [],
            "量词": [],
            "副词": [],
            "介词": [],
            "连词": [],
            "助词": [],
            "叹词": [],
            "语气词": [],
            "拟声词": [],
        }
        res_text = SnowNLP(text)
        for tuples in res_text.tags:
            if "n" in tuples[1]:
                cixing_table['名词'].append(tuples[0])
            if "t" in tuples[1]:
                cixing_table['时间词'].append(tuples[0])
            if "s" in tuples[1]:
                cixing_table['处所词'].append(tuples[0])
            if "f" in tuples[1]:
                cixing_table['方位词'].append(tuples[0])
            if "v" in tuples[1]:
                cixing_table['动词'].append(tuples[0])
            if "a" in tuples[1]:
                cixing_table['形容词'].append(tuples[0])
            if "b" in tuples[1]:
                cixing_table['区别词'].append(tuples[0])
            if "z" in tuples[1]:
                cixing_table['状态词'].append(tuples[0])
            if "m" in tuples[1]:
                cixing_table['数词'].append(tuples[0])
            if "q" in tuples[1]:
                cixing_table['量词'].append(tuples[0])
            if "d" in tuples[1]:
                cixing_table['副词'].append(tuples[0])
            if "p" in tuples[1]:
                cixing_table['介词'].append(tuples[0])
            if "c" in tuples[1]:
                cixing_table['连词'].append(tuples[0])
            if "u" in tuples[1]:
                cixing_table['助词'].append(tuples[0])
            if "e" in tuples[1]:
                cixing_table['叹词'].append(tuples[0])
            if "y" in tuples[1]:
                cixing_table['语气词'].append(tuples[0])
            if "o" in tuples[1]:
                cixing_table['拟声词'].append(tuples[0])
        return cixing_table

