from django.contrib import admin

from .models import Question
#Add access to questions from admin page
admin.site.register(Question)