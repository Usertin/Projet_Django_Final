from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=50, default='')
    prenom = models.CharField(max_length=50, default='')
    image = models.ImageField(upload_to='images/')
    telephone = models.CharField(max_length=20)

class Post(models.Model):
    POST_TYPES = (
        ('Stage', 'Stage'),
        ('Logement', 'Logement'),
        ('Transport', 'Transport'),
        ('Recommandation', 'Recommandation'),
        ('Evenement', 'Evenement'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    post_type = models.CharField(max_length=50, choices=POST_TYPES)
    date = models.DateField()
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.post_type+" "+self.user.username

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = timezone.now().date()

        if self.post_type == 'Evenement':
            if not hasattr(self, 'evenement'):
                # Create an associated Evenement object
                evenement = Evenement.objects.create()
                self.evenement = evenement

        super().save(*args, **kwargs)
        
    
class Recommandation(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    text = models.TextField()

class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    like = models.BooleanField(default=False)

class Evenement(Post):
    intitule = models.CharField(max_length=100)
    description = models.TextField()
    lieu = models.CharField(max_length=100)
    contact_info = models.CharField(max_length=100)

    EVENT_SUBTYPES = (
        ('EvenClub', 'EvenClub'),
        ('EventSocial', 'EventSocial'),
    )

    subtype = models.CharField(max_length=50, choices=EVENT_SUBTYPES, null=True, default=None)


class Stage(Post):
    typeStg = models.IntegerField()
    societe = models.CharField(max_length=100)
    duree = models.IntegerField()
    subject = models.CharField(max_length=255 , default='')
    contactInfo = models.CharField(max_length=100)

class Logement(models.Model):
    localisation = models.CharField(max_length=100)
    description = models.TextField()
    contactInfo = models.CharField(max_length=100)
    post = models.OneToOneField(Post, on_delete=models.CASCADE , default='')

class Transport(models.Model):
    depart = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    heure_dep = models.TimeField()
    nbreSieges = models.IntegerField()
    contactInfo = models.CharField(max_length=100)
    post = models.OneToOneField(Post, on_delete=models.CASCADE , default='')


class EvenClub(models.Model):
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    club = models.CharField(max_length=100)

class EventSocial(models.Model):
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE)
    prix = models.FloatField()


class TransportRequest(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)