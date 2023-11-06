from django.db import models

'''
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.user.username
        
class ProductAddFeed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    namefeed = models.CharField(max_length=255)
    textfeed = models.TextField()

    def __str__(self):
        return self.name
'''