from django import forms
from blog.models import Comment
from django.contrib.auth.models import User

class EmailShareForm(forms.Form):
    name = forms.CharField(label='Name')
    to = forms.EmailField(label = 'Email')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class SignUp(forms.ModelForm):
    class Meta:
        model = User
        fields=['username','password','email','first_name','last_name']
