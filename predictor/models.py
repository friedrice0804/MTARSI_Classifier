from django.db import models

class Rotation_option(models.Model):
    # null = False, blank = False <- These arguments makes sure you
    # don't leave this name field left blank.
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

class data_to_process(models.Model):
    rotationOption = models.ForeignKey(Rotation_option, 
                                  on_delete=models.SET_NULL, 
                                  null=True, blank=True)
    
    img = models.ImageField(null = False, blank=False)