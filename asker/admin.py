from django.contrib import admin

from asker.models import Question, Profile, Tag, Like, Answer

admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Answer)