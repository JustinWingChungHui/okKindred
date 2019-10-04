import datetime
from django.db import models


class Queue(models.Model):
    '''
    Defines the model for a message queue
    '''

    name = models.CharField(max_length=100, null = False, blank = False, unique=True)
    description = models.CharField(max_length=512, null = True, blank = True)

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self): # __unicode__ on Python 2
        return self.name

class Message(models.Model):
    '''
    Defines the model for a message placed in the queue
    '''
    class Meta:
        indexes = [
                models.Index(fields=['processed']),
                models.Index(fields=['creation_date']),
                models.Index(fields=['queue'])
        ]

    queue = models.ForeignKey(Queue, blank=False, null=False, on_delete=models.CASCADE)
    processed = models.BooleanField(default=False)
    string_data = models.CharField(max_length=512, null = True, blank = True)
    integer_data = models.IntegerField(null=True)
    float_data = models.FloatField(null=True)
    date_data = models.DateTimeField(null=True)

    #Tracking
    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated_date = models.DateTimeField(auto_now=True)

    def __str__(self): # __unicode__ on Python 2
        return str(self.id)



def create_message(queue_name, *args):
    '''
    Creates messages and puts them on the queue
    '''
    queue = Queue.objects.get(name = queue_name)

    message = Message(queue = queue)

    for arg in args:
        if type(arg) is datetime.datetime:
            message.date_data = arg

        elif type(arg) is datetime.date:
            message.date_data = arg

        elif type(arg) is float:
            message.float_data = arg

        elif type(arg) is int:
            message.integer_data = arg

        elif type(arg) is str:
            message.string_data = arg

        else:
            raise ValueError('create_message args not valid')

    message.save()

    return message

