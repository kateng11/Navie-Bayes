import collections
from django.http import JsonResponse
from rest_framework.views import APIView
from snownlp import SnowNLP
from database import models


class CiYunData(APIView):

    def get(self, request):
        data = {}
        try:
            find_obj = models.ReqeustsData.objects.order_by("id")
            res_text = ""
            for obj in find_obj:
                res_text = res_text + obj.name + "," + obj.comment + ","

            # 词云
            ciyun_list = []
            for keys, values in self.word_counts_action(res_text, 100):
                json_data = {}
                json_data['name'] = str(keys)
                json_data['value'] = values
                ciyun_list.append(json_data)
            data['res_list'] = ciyun_list
            data['code'] = 200
            return JsonResponse(data)

        except Exception as e:
            print(e)
            data['code'] = 444
            return JsonResponse(data)

    # 词频
    def word_counts_action(self, text, top_number):
        """
            :param text:  统计的文本
            :param top_number:   输出词频前几
            :return: [('非常', 36), ('很', 31), ('手机', 23), ('也', 18)]
        """
        # 文本预处理
        with open('file/stop_words.txt', 'r', encoding='utf-8') as file:
            remove_words = file.read().splitlines()
        object_list = []

        # remove_words = [u'的', u'，', u'和', u'是', u'随着', u'对于', u'对', u'等', u'能', u'都', u'。', u'！', u'你',
        #                 u'|', u'一', u'不', u'！,', u'了', u'（', u'我', u'看', u'题'
        #     , u' ', u'、', u'中', u'在', u'】', u',【', u'但', u',', u'通常', u'如果', u'我们', u'需要', u'： ', u'）, ',
        #                 u'：', u'）,', u'｜', u'？', u'-', u'【', u'）', u',：','？,','22'
        #     , u'个', u'语', u'最', u'这', u'讲', u'年', u'+', u'人', u'/', u'如果', u'我们', u'需要', u'： ', u'）, ',
        #                 u'：', u'）,', u'｜', u'？', u'-', u'【', u'）', u',：'
        #                 ]  # 自定义去除词库
        seg_list_exact = SnowNLP(text).words  # 每一个数组评论分词
        for word in seg_list_exact:  # 循环读出每个分词
            if word not in remove_words:  # 如果不在去除词库中
                object_list.append(word)  # 分词追加到列表
        word_counts = collections.Counter(object_list)  # 对分词做词频统计
        word_top_number = word_counts.most_common(top_number)  # 获取前10最高频的词
        return word_top_number
