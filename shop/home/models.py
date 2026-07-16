from django.db import models
from django.urls import reverse
from accounts.models import User

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to="products/%Y/%m/%d/")
    description = models.TextField()
    price = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:product_detail' , args=[self.id ,self.slug,])


class Comment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'در انتظار بررسی'
        APPROVED = 'approved', 'تایید شده'
        REJECTED = 'rejected', 'رد شده'


    user = models.ForeignKey(User , on_delete=models.CASCADE , related_name="ucomments")
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="pcomments")
    reply = models.ForeignKey("comment",on_delete=models.CASCADE , related_name="rcomment" , blank=True , null= True)
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.user} , {self.body[:30]}"

    @property
    def approved_replies(self):
        return self.rcomment.filter(status=self.Status.APPROVED)

# Create your models here.
