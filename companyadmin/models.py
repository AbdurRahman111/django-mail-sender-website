from django.db import models

# Create your models here.

class company_subscription_admin(models.Model):
    class Meta:
        verbose_name_plural = 'Company Subscription Admin'
    User_id = models.CharField(max_length=255)
    company_id = models.CharField(max_length=255)
    subscription_id = models.CharField(max_length=255)

    def __str__(self):
        return self.User_id +" - " + self.company_id + " - " + self.subscription_id
