from django.contrib import admin
from .models import CategoryModel, BookModel, ReviewModel, BorrowModel

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ['name', 'slug']

admin.site.register(CategoryModel, CategoryAdmin)

admin.site.register(BookModel)
admin.site.register(ReviewModel)
admin.site.register(BorrowModel)
