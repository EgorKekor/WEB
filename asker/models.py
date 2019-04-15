from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    upload = models.ImageField(upload_to='')
    rating = models.IntegerField(default=0)


class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name=u"Заголовок ярлыка")

    def __str__(self):
        return self.title


class Like(models.Model):
    TYPES = [
        (1, 'LIKE'),
        (-1, 'DISLIKE')
    ]
    rate = models.SmallIntegerField(choices=TYPES)
    author = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
    )


class QuestionManager(models.Manager):
    def get_hot(self):
        return self.filter(is_active=True).order_by('-raiting').prefetch_related()

    def get_by_tag(self, tag_title):
        return self.filter(is_active=True).filter(tags__title=tag_title).prefetch_related()

    def get_new(self):
        return self.all().order_by('-create_date').prefetch_related()

    def update_raiting(self):
        self.all()


class Question(models.Model):
    objects = QuestionManager()
    author = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
    )
    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(verbose_name=u"Полное описание вопроса")
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")
    tags = models.ManyToManyField(
        Tag,
        blank=True
    )
    raiting = models.IntegerField(null=True, blank=True, default=0, verbose_name='raiting')
    likes = models.ManyToManyField(
        Like,
        blank=True
    )

    # def answer_count(self):
    #     return self.answer_set.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']


class Answer(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
    )
    text = models.TextField(verbose_name=u'Тест ответа')
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время ответа")
    question = models.ForeignKey(
        'Question',
        on_delete=models.PROTECT,
    )
    raiting = models.IntegerField(null=True, blank=True, default=0)
    likes = models.ManyToManyField(
        Like,
        blank=True
    )

    def __unicode__(self):
        return self.question.title

    class Meta:
        ordering = ['-create_date']
