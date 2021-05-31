from django.db import models


# Create your models here.
class Trophy(models.Model):
    name = models.CharField(max_length=64, unique=True, null=True)
    amount = models.CharField(max_length=64, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Club(models.Model):
    name = models.CharField(max_length=64, unique=True)
    created = models.DateField()
    country = models.CharField(max_length=64)
    league = models.CharField(max_length=64)
    logo = models.ImageField(null=True, blank=True)
    trophy = models.ManyToManyField(Trophy)


    def __str__(self):
        return self.name



class Staff(models.Model):
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)
    birthday = models.DateField()
    age = models.IntegerField()
    role= models.CharField(max_length=64)
    club = models.ForeignKey(Club, on_delete=models.PROTECT)
    logo = models.ImageField(null=True, blank=True)


    def __str__(self):
        return self.first_name


class Stadium(models.Model):
    name=models.CharField(max_length=64, unique=True)
    location=models.CharField(max_length=64)
    capacity=models.IntegerField()
    created = models.DateField()
    club = models.ForeignKey(Club, on_delete=models.PROTECT)
    logo = models.ImageField(upload_to='', null=True, blank=True)

    
    def __str__(self):
        return self.name
