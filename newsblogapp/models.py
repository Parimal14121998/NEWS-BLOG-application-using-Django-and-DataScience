from django.db import models

# Create your models here.
class newsblogmodel(models.Model):
	email=models.EmailField(primary_key=True)
	name=models.TextField()
	genre=models.TextField()
	crdt=models.DateTimeField(auto_now_add=True)

	def __str__(self):	
		return self.email