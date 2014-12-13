from django.forms import (
    Form, CharField, Textarea, PasswordInput, ChoiceField, DateField,
    ImageField, ValidationError
)
from django.contrib.auth.models import User

from fb.models import UserProfile


class UserPostForm(Form):
    text = CharField(widget=Textarea(
        attrs={
            'rows': 1, 'cols': 40,
            'class': 'form-control',
            'placeholder': "What's on your mind?"
        })
    )


class UserPostCommentForm(Form):
    text = CharField(widget=Textarea(
        attrs={
            'rows': 1, 'cols': 50,
            'class': 'form-control',
            'placeholder': "Write a comment..."
        })
    )


class UserLogin(Form):
    username = CharField(max_length=30)
    password = CharField(widget=PasswordInput)


class UserRegisterForm(Form):
    username = CharField(max_length=30)
    password = CharField(widget=PasswordInput)
    password_confirmation = CharField(widget=PasswordInput)

    def save(self):
        user = User(username=self.cleaned_data["username"])
        user.set_password(self.cleaned_data["password"])
        user.save()

    def clean_username(self):
        data = self.cleaned_data["username"]
        user = User.objects.filter(username=data)
        if user:
            raise ValidationError("There is another user with this username")
        return data

    def clean_password_confirmation(self):
        if (self.cleaned_data["password"] !=
            self.cleaned_data["password_confirmation"]):
            raise ValidationError("The passwords don't match")
        return self.cleaned_data["password_confirmation"]


class UserProfileForm(Form):
    first_name = CharField(max_length=100, required=False)
    last_name = CharField(max_length=100, required=False)
    gender = ChoiceField(choices=UserProfile.GENDERS, required=False)
    date_of_birth = DateField(required=False)
    avatar = ImageField(required=False)


class UserGiftForm(Form):
    message = CharField(widget=Textarea(
        attrs={
            'rows': 1, 'cols': 40, 'class': 'form-control',
            'placeholder': "Write something from your heart"
        })
    )
    snapshot = ImageField(required=False)
