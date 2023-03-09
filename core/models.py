from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_resized import ResizedImageField
from django.conf import settings

# Create your models here.

"""
User extra data(contacts) i am using english name variables
and on verbose name i am using Portuguese
First Name, Last Name and e-mail are included on User Model
The funds field is the monetary is the value that user has
put on the app
"""
class Profile(models.Model):
    user     = models.OneToOneField(User, null=False, blank=False, verbose_name="Utilizador", 
                                on_delete=models.CASCADE)
    address  = models.CharField(max_length=150, null=True, blank=True, 
                                verbose_name="Morada")
    zip_code = models.CharField(max_length=12, null=True, blank=True, 
                                verbose_name="Código Postal")
    location = models.CharField(max_length=120, null=True, blank=True, 
                                verbose_name="Localização")
    phone    = models.IntegerField(null=True, blank=True, 
                                   verbose_name="Número de contato")
    funds    = models.FloatField(null=True, blank=True, verbose_name="Fundos")

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name        = 'Perfil'
        verbose_name_plural = 'Perfis' 


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

"""
Bike models, here we have the values of the electric bikes,
like serial numbers, date that was bought, status of bike
"""
class Bike(models.Model):
    serie_number = models.CharField(max_length=500, null=False, blank=False, 
                                   verbose_name="Número de série", unique=True)
    date_bought  = models.DateField(null=False, blank=False, 
                                    verbose_name="Data de Compra")
    status       = models.CharField(max_length=100, null=False, blank=False, 
                                    verbose_name="Estado")
    notes        = models.TextField(null=True, blank=True, verbose_name="Notas")

    def __str__(self):
        return self.serie_number
    
    class Meta:
        verbose_name        = 'Bicicleta'
        verbose_name_plural = 'Bicicletas' 


"""
Packages for user to be able to walk on the bike, this is only controlled
by the entity that owes the bike
"""
class UnlockPackage(models.Model):
    name  = models.CharField(max_length=100, null=False, verbose_name="Nome")
    hours = models.FloatField(null=False, blank=False, verbose_name="Horas")
    price = models.FloatField(null=False, blank=False, verbose_name="Preço")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name        = 'Pacote'
        verbose_name_plural = 'Pacotes'


"""
Purchase models, this will have the user purchase values
"""
class Purchase(models.Model):
    user    = models.ForeignKey(User, null=False, blank=False, 
                             verbose_name="Utilizador", on_delete=models.CASCADE)
    bike    = models.ForeignKey(Bike, null=False, blank=False, 
                             verbose_name="Bicicleta", on_delete=models.CASCADE)
    package = models.ForeignKey(UnlockPackage, null=False, blank=False,
                                verbose_name="Pacote", on_delete=models.CASCADE)
    date    = models.DateTimeField(null=False, blank=False, 
                                   verbose_name="Data e Hora")
    
    class Meta:
        verbose_name        = 'Compra do Utilizador'
        verbose_name_plural = 'Compras do utilizador'

"""
Model for island information
"""
class Island(models.Model):
    name            = models.CharField(max_length=150, null=False, blank=False, 
                            verbose_name="Ilha")
    description_pt  = models.TextField(null=True, blank=True, 
                                    verbose_name="Descrição da Ilha(Português)")
    description_eb  = models.TextField(null=True, blank=True, 
                                    verbose_name="Descrição da Ilha(Inglês)")
    image           =  ResizedImageField(size=[200, 200], upload_to='island', 
                                         force_format='WEBP', quality=90,
                                         keep_meta=False, null=True, blank=True)
    
    @property
    def image_url(self):
        return "{0}{1}".format(settings.SITE_URL, self.image.url)

    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name        = 'Ilha'
        verbose_name_plural = 'Ilhas'

