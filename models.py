from django.db import models

# Create your models here.


class Visitor(models.Model):
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField()
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    office_designation = models.CharField(max_length=100)
    office_name = models.CharField(max_length=100)
    visiting_purpose = models.CharField(max_length=200)
    
    punch_out_time = models.DateTimeField(null=True, blank=True)
    
    visit_time = models.DateTimeField(auto_now_add=True)
    mobile = models.CharField(max_length=15, blank=True)
    organization = models.CharField(max_length=100, blank=True)
    visit_out_time = models.DateTimeField(null=True, blank=True)
    photo = models.ImageField(upload_to='visitor_photos/', null=True, blank=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.office_name}"

    
