from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserDetailsModel
from .constants import GENDER_TYPES

class UserRegisterForm(UserCreationForm):
    profile_image = forms.ImageField(required=False)
    birth_date = forms.DateField(widget= forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPES)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    post_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 
                  'last_name', 'email', 'birth_date', 'gender', 'street_address',
                   'city', 'post_code', 'country','profile_image']
    
    def save(self, commit=True):
        # Save the basic User fields
        our_user = super().save(commit=False)
        if commit:
            our_user.save()
            
            # Collect cleaned data for user details
            profile_image = self.cleaned_data.get('profile_image')
            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            post_code = self.cleaned_data.get('post_code')
            country = self.cleaned_data.get('country')

            # Create user details
            user_details = UserDetailsModel.objects.create(
                user=our_user,
                account_no=10000 + our_user.id,  # or generate a more complex account_no
                birth_date=birth_date,
                gender=gender,
                post_code=post_code,
                country=country,
                street_address=street_address,
                city=city
            )
            
            # Handle the optional profile image
            if profile_image:
                user_details.profile_image = profile_image
                user_details.save()

        return our_user

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {
                    'class': (
                        'appearance-none block w-full bg-gray-200 '
                        'text-gray-700 border border-gray-200 rounded '
                        'py-3 px-4 leading-tight focus:outline-none '
                        'focus:bg-white focus:border-gray-500'
                    )
                }
            )

class DepositeForm(forms.Form):
    amount = forms.DecimalField(max_digits=12, decimal_places=2)

    def clean_amount(self):
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(f'You need to deposit at least {min_deposit_amount}$')
        return amount

