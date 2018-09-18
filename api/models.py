from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

STATUS_CHOICES = [('backlog', 'Backlog'), ('selected for development', 'Selected for Development'),
                  ('in progress', 'In progress'), ('ready for release', 'Ready for release'),
                  ('done', 'Done')]

TYPE_CHOICES = [('trivial', 'Trivial'), ('minor', 'Minor'), ('major', 'Major'),
                ('critical', 'Critical'), ('blocker', 'Blocker')]

CATEGORY_CHOICES = [('task', 'Task'), ('bug', 'Bug'), ('story', 'Story'), ('enhancement', 'Enhancement')]


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reporter')
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignee', null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='backlog')
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default='trivial')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.title)


class Tag(models.Model):
    tag = models.CharField(max_length=50)
    ticket = models.ManyToManyField(Ticket)

    def __str__(self):
        return "{}".format(self.tag)
