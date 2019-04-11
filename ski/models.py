from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.urls import reverse

# Create your models here.
class State(models.Model):
    state_name = models.CharField(max_length=200)
    def __str__(self):
        return self.state_name

class Mountain(models.Model):
    name = models.CharField(max_length=200)
    state_name = models.ForeignKey('State', on_delete=models.CASCADE, null=False)
    url = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    new_snow = models.IntegerField(null=True)
    current_weather = models.CharField(max_length=200)
    snowpack = models.CharField(max_length=100, null=True)
    open_percent = models.CharField(max_length=100, null=True)
    trails = models.CharField(max_length=100, null=True)
    lifts = models.CharField(max_length=100, null=True)
    base = models.CharField(max_length=100, null=True)
    conditions = models.CharField(max_length=100, null=True)

    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL,through='Fav',
                                        related_name='favorite_mountain')

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('mountain', args=[str(self.state_name), str(self.name)])

    def __str__(self):
        return self.name

class Comments(models.Model) :
    text = models.TextField(
        validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")]
    )

    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 15 : return self.text
        return self.text[:11] + ' ...'

class Fav(models.Model):
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('mountain', 'user')

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.mountain.name[:10])

class Geography(models.Model):
    mountain = models.ForeignKey(Mountain, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return '{} ({},{})'.format(self.mountain,self.latitude,self.longitude)
