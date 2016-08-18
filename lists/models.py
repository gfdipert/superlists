from django.db import models

# Create your models here.
#To give our Item class a save method, and to make it into a real Django model, we make it inherit from the Model class:
class List(models.Model):
	pass

class Item(models.Model):
	text = models.TextField(default='')
	list = models.ForeignKey(List, default=None)