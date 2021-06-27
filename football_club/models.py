from django.db import models
from django.urls import reverse


# Create your models here.
class Trophy(models.Model):
    name = models.CharField(max_length=64, unique=True, null=True)
    logo = models.ImageField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст", null=True)
    created = models.DateField(null=True)
    winers = models.TextField(blank=True, verbose_name="Список обладателей", null=True)
    actual_owner = models.CharField(max_length=64, unique=True, null=True)
    recordsman = models.CharField(max_length=64, unique=True, null=True)



    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('football_club:trophy', kwargs={'trophy_slug': self.slug})
    
    class Meta:
        ordering = ['name']


class Club(models.Model):
    name = models.CharField(max_length=64, unique=True)
    created = models.DateField()
    country = models.CharField(max_length=64)
    league = models.CharField(max_length=64)
    logo = models.ImageField(null=True, blank=True)
    trophy = models.ManyToManyField(Trophy, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст", null=True)
    trophylist = models.TextField(blank=True, verbose_name="Достижения", null=True)
    teams_photo = models.ImageField(null=True, blank=True)





    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('football_club:club', kwargs={'club_slug': self.slug})

    class Meta:
       ordering = ['name']




class Staff(models.Model):
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)
    birthday = models.DateField()
    age = models.IntegerField()
    role= models.CharField(max_length=64)
    club = models.ForeignKey(Club, on_delete=models.PROTECT)
    logo = models.ImageField(null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст", null=True)
    trophylist = models.TextField(blank=True, verbose_name="Достижения", null=True)




    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse('football_club:staff', kwargs={'staff_slug': self.slug})
    
    class Meta:
           ordering = ['second_name']

class Stadium(models.Model):
    name=models.CharField(max_length=64, unique=True)
    location=models.CharField(max_length=64)
    capacity=models.IntegerField()
    created = models.DateField()
    club = models.ForeignKey(Club, on_delete=models.PROTECT)
    logo = models.ImageField(upload_to='', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст", null=True)
    bestgames = models.TextField(blank=True, verbose_name="Лучшие матчи", null=True)



    
    def __str__(self):
        return self.name
    
    
    def get_absolute_url(self):
        return reverse('football_club:stadium', kwargs={'stadium_slug': self.slug})

    
    class Meta:
           ordering = ['name']