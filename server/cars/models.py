from django.db import models
class CarMake(models.Model):
 name=models.CharField(max_length=100,unique=True)
 description=models.TextField(blank=True)
 def __str__(self): return self.name
class CarModel(models.Model):
 make=models.ForeignKey(CarMake,related_name="models",on_delete=models.CASCADE)
 name=models.CharField(max_length=100)
 year=models.PositiveSmallIntegerField(null=True,blank=True)
 def __str__(self): return f"{self.make} {self.name}"
