import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WEB.settings')

import django
django.setup()

from faker import Factory
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from asker.models import Question, Profile, Tag, Like, Answer
from random import choice, randint
import urllib.request as request
import random
from django.core.files import File


class Command(BaseCommand):
    help = 'Fills database with fake data'
    faker = Factory.create()

    USERS_COUNT = 100
    QUESTIONS_COUNT = 100
    TAGS_COUNT = 2
    MIN_ANSWERS = 0
    MAX_ANSWERS = 5

    def add_arguments(self, parser):
        pass


    def create_users(self):
        for i in range(0, self.USERS_COUNT):
            profile = self.faker.simple_profile()

            u = Profile()
            u.username = profile['username']
            u.first_name = self.faker.first_name()
            u.last_name = self.faker.last_name()
            u.email = profile['mail']
            u.password = make_password('web')
            u.is_active = True
            u.is_superuser = False
            print(u.id)
            image_url = 'https://robohash.org/%d.png' % random.randint(0, 10000)
            content = request.urlretrieve(image_url)
            u.upload.save('%s.png' % u.username, File(open(content[0], 'rb')), save=True)
            u.save()
            self.stdout.write('[%d] added user %s' % (u.id, u.username))


    def create_questions(self):
        users = Profile.objects.all()

        for i in range(0, self.QUESTIONS_COUNT):
            q = Question()

            q.title = self.faker.sentence(nb_words=randint(4, 6), variable_nb_words=True)
            q.text = self.faker.paragraph(nb_sentences=randint(4, 13), variable_nb_sentences=True),

            q.author = choice(users)
            q.save()
            self.stdout.write('added question [%d]' % q.id)

    def create_answers(self):
        users = Profile.objects.all()
        questions = Question.objects.all()

        for question in questions:
            for i in range(0, randint(self.MIN_ANSWERS, self.MAX_ANSWERS)):
                a = Answer()
                a.author = choice(users)
                a.text = self.faker.paragraph(nb_sentences=randint(2, 10), variable_nb_sentences=True),
                a.question = question
                a.save()
                self.stdout.write('added answer [%d]' % a.id)

    def create_likes(self):
        users = Profile.objects.all()
        questions = Question.objects.all()
        answers = Answer.objects.all()

        for question in questions:
            start = randint(0, self.USERS_COUNT - 21)
            end = randint(start, start + randint(0, 11))
            for i in range(start, end):
                like = Like()
                like.author = users[i]
                like.rate = choice([-1, 1])
                self.stdout.write('liked question [%d]' % question.id)
                like.save()
                question.likes.add(like)
                question.raiting += like.rate
                question.save()

        for answer in answers:
            start = randint(0, self.USERS_COUNT - 21)
            end = randint(start, start + randint(0, 20))
            for i in range(start, end):
                like = Like()
                like.author = users[i]
                like.rate = choice([-1, 1])
                self.stdout.write('liked answer [%d]' % answer.id)
                like.save()
                answer.likes.add(like)
                answer.raiting += like.rate
                answer.save()


    def create_tags(self):
        tags = [
            'JavaScript', 'Java', 'C#', 'PHP', 'Android', 'JQuery', 'Python',
            'HTML', 'CSS', 'C++', 'iOS', 'MySQL', 'Objective-C',
            'SQL', '.net', 'RUBY', 'Swift', 'Vue', '1C'
        ]
        for tag in tags:
            t = Tag()
            t.title = tag
            t.save()

        tags = Tag.objects.all()
        questions = Question.objects.all()
        for question in questions:
            for i in range(0, self.TAGS_COUNT):
                t = choice(tags)
                if t not in question.tags.all():
                    question.tags.add(t)

            self.stdout.write('tagged question [%d]' % question.id)


    def handle(self, *args, **options):
        # self.create_users()
        # self.create_questions()
        # self.create_answers()
        self.create_likes()
        self.create_tags()


test = Command()
test.handle()
print("work")