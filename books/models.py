from django.db import models
from django.contrib.auth.models import User

class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

class BookModel(models.Model):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    book_image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    borrowingPrice = models.FloatField()
    
    def __str__(self):
        return self.title

class ReviewModel(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"For {self.book.title} by {self.user.username}"

class BorrowModel(models.Model):
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    on_date = models.DateField(auto_now_add=True)
    ammount = models.FloatField()
    type = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.book.title} by {self.user.username}"


    
