from django.db import models

# Create your models here.
class Charge(models.Model):
    full_name = models.CharField(max_length=50, blank=False)
    phone_number = models.CharField(max_length=20, blank=False)
    country = models.CharField(max_length=40, blank=False)
    postcode = models.CharField(max_length=20, blank=True)
    town_or_city = models.CharField(max_length=40, blank=False)
    street_address1 = models.CharField(max_length=40, blank=False)
    street_address2 = models.CharField(max_length=40, blank=False)
    date = models.DateField()

    def __str__(self):
        return "{0}-{1}-{2}".format(self.id, self.date, self.full_name)
        
class Transaction(models.Model):
    
    status_options = [
        ('pending', "Pending"),
        ('approved', "Approved"),
        ('rejected', "Rejected"),
        ('shipping', 'Shipping'),
        ('delivered', 'Delivered'),
        ('lost', 'Lost')
    ]
    
    charge = models.ForeignKey('Charge', on_delete=models.CASCADE)
    status = models.CharField(blank=False, choices=status_options, max_length=50)
    
    def __str__(self):
        return str(self.id)