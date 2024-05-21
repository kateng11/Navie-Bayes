from django.db import models
from django.utils.html import format_html


# Create your models here.
class List(models.Model):
    sentences = models.CharField(verbose_name="语料", max_length=255, null=True, blank=True)
    options = (
        ("正面情绪", "正面情绪"),
        ("负面情绪", "负面情绪"),
    )
    labels = models.CharField(verbose_name="情绪", max_length=10, choices=options, null=True, blank=True)

    class Meta:
        verbose_name = "训练集"
        verbose_name_plural = verbose_name
        db_table = 'List'


class Douyin(models.Model):
    vedioname = models.CharField(verbose_name="视频标题", max_length=255, null=True, blank=True)
    username = models.CharField(verbose_name="评论用户", max_length=255, null=True, blank=True)
    comment = models.CharField(verbose_name="评论内容", max_length=255, null=True, blank=True)
    labels = models.CharField(verbose_name="情绪标识", max_length=255, null=True, blank=True)
    url = models.CharField(verbose_name="内容详情", max_length=255, null=True, blank=True)
    keyword =models.CharField(verbose_name="关键字",max_length=255,null=True,blank=True)

    def __str__(self):
        return self.username

    def href_link(self):
        path = self.url
        button_html = "<a  href='{}'  target='_blank' >视频地址</a>".format(path)
        return format_html(button_html)

    href_link.short_description = format_html(
        """<a  href='#' style="position: relative;left: -12px; target='_blank'  ">跳转查看</a>""")

    class Meta:
        verbose_name = "抖音MSG"
        verbose_name_plural = verbose_name
        db_table = 'Douyin'


# Create your models here.
class ReqeustsData(models.Model):
    name = models.CharField(verbose_name="贴吧标题", max_length=255, null=True, blank=True)
    url = models.CharField(verbose_name="内容详情", max_length=255, null=True, blank=True)
    author = models.CharField(verbose_name="发帖用户", max_length=255, null=True, blank=True)
    reviewer = models.CharField(verbose_name="审核人", max_length=255, null=True, blank=True)
    last_comment_time = models.CharField(verbose_name="最新评论时间", max_length=255, null=True, blank=True)
    comment = models.TextField(verbose_name="最新评论内容", max_length=255, null=True, blank=True)
    labels = models.CharField(verbose_name="情绪标识", max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def href_link(self):
        path = self.url
        button_html = "<a  href='{}'  target='_blank' >帖子详情</a>".format(path)
        return format_html(button_html)

    href_link.short_description = format_html(
        """<a  href='#' style="position: relative;left: -12px; target='_blank'  ">跳转查看</a>""")

    def collection(self):
        button_html = "<a  href='/api/collection?name={}&url={}'  >点击收藏</a>".format(self.name, self.url)
        return format_html(button_html)

    collection.short_description = format_html("""<a  href='#' style="position: relative;left: -12px;">收藏</a>""")

    class Meta:
        verbose_name = "贴吧MSG"
        verbose_name_plural = verbose_name
        db_table = 'ReqeustsData'


class Colect(models.Model):
    co_title = models.CharField(verbose_name="收藏", max_length=255, null=True, blank=True)
    co_down_link = models.CharField(verbose_name="收藏地址", max_length=255, null=True, blank=True)

    def __str__(self):
        return self.co_title

    def href_link(self):
        path = self.co_down_link
        button_html = "<a  href='{}'  >帖子详情</a>".format(path)
        return format_html(button_html)

    href_link.short_description = format_html(
        """<a  href='#' style="position: relative;left: -12px; target='_blank'  ">跳转查看</a>""")

    class Meta:
        verbose_name = "收藏列表"
        verbose_name_plural = verbose_name
        db_table = 'Colect'
