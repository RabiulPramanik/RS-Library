from django.shortcuts import render, redirect
from .models import BookModel
from .models import BorrowModel, ReviewModel
from decimal import Decimal
from accounts.views import send_email
from django.views.generic import DetailView
from .form import ReviewForm

def BookDetails(request, id):
    book = BookModel.objects.get(pk = id)
    return render(request, "details.html", {"book":book})

class book_detailsView(DetailView):
    model = BookModel
    template_name = "details.html"
    pk_url_kwarg = 'id'
    context_object_name = 'book'
    

    def post(self, request, *args, **kwargs):
        form = ReviewForm(data=self.request.POST)
        book = self.get_object()
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.book = book
            new_comment.user = self.request.user
            new_comment.save()
            return self.get(request, *args, **kwargs)
        else:
            return redirect("bookDetails", id = book.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ReviewForm()
        context["Reviews"] = ReviewModel.objects.filter(book = self.get_object())
        context["borrow"] = BorrowModel.objects.filter(book = self.get_object(), user = self.request.user)
        return context

def BorrowBook(request, id):
    book = BookModel.objects.get(pk = id)
    account = request.user.account
    if book.borrowingPrice <= account.balance:
        account.balance = account.balance - Decimal(book.borrowingPrice)
        account.save(
            update_fields = [
                'balance'
            ]
        )
        BorrowModel.objects.create(
                book = book,
                user = request.user,
                ammount = book.borrowingPrice
            )
        send_email(request.user, book.borrowingPrice, "Book Borrow", "gmail.html", "Book Borrow")
        return redirect("profile")
    return redirect("bookDetails", id = book.id)

def returnBook(request, id):
    borrow = BorrowModel.objects.get(pk = id)
    borrow.type = True
    borrow.save()
    account = request.user.account
    account.balance = account.balance + Decimal(borrow.book.borrowingPrice)
    account.save(
        update_fields = [
            'balance'
        ]
    )
    send_email(request.user, borrow.book.borrowingPrice, "Book Return", "gmail.html", "Book Return")
    return redirect("profile")

