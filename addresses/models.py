from django.db import models
from billing.models import BillingProfile

class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    company = models.CharField(max_length=120, blank=True, null=True)
    address_1 = models.CharField(max_length=120)
    address_2 = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    post_code = models.CharField(max_length=120)
    phone = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return str("email: {0}, {1} {2} {3}".format(self.billing_profile, self.address_1, self.city, self.post_code))