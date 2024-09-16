from django.urls import path
from . import views


urlpatterns = [
    # path('ditals/<int:id>', views.BookDetails, name="bookDetails"),
    path('ditals/<int:id>', views.book_detailsView.as_view(), name="bookDetails"),
    path('borrow/<int:id>', views.BorrowBook, name="borrowBook"),
    path('returnBook/<int:id>', views.returnBook, name="returnBook"),
]