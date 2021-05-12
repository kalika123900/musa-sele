from django.utils.translation import gettext_lazy as _

from django.db import models

# Create your models here.
class Brands(models.Model):
    class STATUS(models.TextChoices):
        VERIFIED = '1' , _('Active')
        UNVERIFIED = '0' , _('Inactive')
    
    search_key = models.CharField(max_length=255,null=True)
    search_via = models.CharField(max_length=30,null=True)
    search_cr  = models.CharField(max_length=30,null=True)
    search_cr_url = models.CharField(max_length=255,null=True)
    search_verified = models.CharField(max_length=1,
        choices=STATUS.choices,
        default=STATUS.UNVERIFIED,)
    objects = models.Manager()    