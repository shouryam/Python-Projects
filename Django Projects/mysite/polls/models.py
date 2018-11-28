from django.db import models

#Create a question model
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    #Record the date and time of when the question was published
    pub_date = models.DateTimeField('date published')
    #Create a function that displaces the text of the question
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    ##Every question can have choice attributes
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    #Define a function to display the text of a choice

    def __str__(self):
        return self.choice_text