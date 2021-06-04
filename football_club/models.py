from django.db import models
from django.urls import reverse


# Create your models here.
class Trophy(models.Model):
    name = models.CharField(max_length=64, unique=True, null=True)
    amount = models.CharField(max_length=64, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('trophy', kwargs={'trophy_slug': self.slug})


class Club(models.Model):
    name = models.CharField(max_length=64, unique=True)
    created = models.DateField()
    country = models.CharField(max_length=64)
    league = models.CharField(max_length=64)
    logo = models.ImageField(null=True, blank=True)
    trophy = models.ManyToManyField(Trophy, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('club', kwargs={'club_slug': self.slug})



class Staff(models.Model):
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)
    birthday = models.DateField()
    age = models.IntegerField()
    role= models.CharField(max_length=64)
    club = models.ForeignKey(Club, on_delete=models.PROTECT)
    logo = models.ImageField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")


    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('staff', kwargs={'staff_slug': self.slug})


class Stadium(models.Model):
    name=models.CharField(max_length=64, unique=True)
    location=models.CharField(max_length=64)
    capacity=models.IntegerField()
    created = models.DateField()
    club = models.ForeignKey(Club, on_delete=models.PROTECT)
    logo = models.ImageField(upload_to='', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    
    def __str__(self):
        return self.name
    
    
    def get_absolute_url(self):
        return reverse('stadium', kwargs={'stadium_slug': self.slug})