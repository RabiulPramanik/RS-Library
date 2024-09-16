from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from .form import UserRegisterForm, DepositeForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from decimal import Decimal
from books.models import BorrowModel
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string

def send_email(user, amount, mail_subject, mail_template, title):
    message = render_to_string(mail_template, {
        'user': user,
        'amount': amount,
        'title':title,
    })
    to_Email = user.email
    send_Email = EmailMultiAlternatives(mail_subject, '', to=[to_Email])
    send_Email.attach_alternative(message, "text/html")
    send_Email.send()

class UserRegister(FormView):
    template_name = 'createForm.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('home')

# class UserLogoutView(LogoutView):
#     print("up")
#     def get_success_url(self):
#         print("mup")
#         if self.request.user.is_authenticated:
#             logout(self.request)
#             print("robiul")
#         return reverse_lazy('home')
class logoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")

def depositeView(request):
    if request.method == 'POST':
        Form = DepositeForm(request.POST)
        if Form.is_valid():
            amount = request.POST.get('amount')
            account = request.user.account
            account.balance = account.balance + Decimal(amount)
            account.save(
                update_fields = [
                    'balance'
                ]
            )
            send_email(request.user, amount, "Deposit Money", "email.html", "Deposit")
            return redirect("profile")
    else:
        Form = DepositeForm
    return render(request, "deposite.html", {'form':Form})

def profile(request):
    borrows =  BorrowModel.objects.filter(user = request.user)
    return render(request, "profile.html", {"borrows": borrows})
