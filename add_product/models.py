from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class ProductAdd(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    info_title = models.CharField(max_length=255)
    info = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    unit = models.CharField(max_length=10, null=True, default='kg')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, null=True, default='EUR')

    def __str__(self):
        return self.name

'''
def get_current_user():
    user_model = get_user_model()
    return get_user_model().objects.get(username='your-username-here')
'''