# ORM外部配置
import os

from snownlp import SnowNLP


def orm_standby():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IntelligentHome.settings")  # manage.py文件中有同样的环境配置
    import django
    django.setup()

if __name__ == '__main__':
    orm_standby()
    from database import models

    find_obj = models.ReqeustsData.objects.order_by("id")
    res_text = ""
    for obj in find_obj:
        res_text = res_text + obj.name + "," + obj.comment + ","
    res_text = res_text.replace(",,","").replace("22","").replace("23","")


    # 关键词提取
    good_key = []
    bad_key = []
    keyword_list = []
    for keyword in SnowNLP(res_text).keywords(100):
        if len(keyword) >= 2:
            keyword_list.append(keyword)
            if SnowNLP(keyword).sentiments >= 0.5:
                good_key.append(keyword)
            else:
                bad_key.append(keyword)
    print(good_key)
    print(bad_key)
    print(keyword_list)
