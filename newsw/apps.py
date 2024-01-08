from django.apps import AppConfig
from .management.commands.runapsheduler import *

class NewswConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsw'

    def ready(self):
        #import mynews.newsw.signals

        #from management.commands.runapsheduler import my_mails
        print("+", "start task", my_mails())





