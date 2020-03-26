from django.shortcuts import render,HttpResponse
from .models import Posts,Authors,UsersUser
from django import forms
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime

class LoginForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'maxlength': '254', 'placeholder': ' ', 'autocomplete': 'off'}))

    password = forms.CharField(
        min_length=8,
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    class Meta:
        model = UsersUser
        fields = ['email', 'password']
    
    def clean(self, *args, **kwargs):
        email=self.cleaned_data.get('email')
        password=self.cleaned_data.get('password')
        if(UsersUser.objects.filter(email=email).exists()):
            obj=UsersUser.objects.filter(email=email).first()
            if(obj.password==password):
                self.cleaned_data['obj']=obj
                return super(UsersUser, self).clean(*args, **kwargs)
        raise forms.ValidationError("invalid credintials")


class Login(CreateView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = '/login/'


    def form_valid(self, form):
        obj = form.cleaned_data.get('obj')
        login(self.request,obj)

class RegisterForm(UserCreationForm):
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'type': 'text', 'placeholder': ' '}), required=True)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'type': 'email', 'maxlength': '254', 'placeholder': ' ', 'autocomplete': 'off'}))

    password1 = forms.CharField(
        min_length=8,
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    password2 = forms.CharField(
        label=("Confirm Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': ' '}),
    )
    birthdate =  forms.DateField(widget=forms.DateInput(attrs={'type': "date", 'placeholder': ' '}),required=True)

    class Meta:
        model = UsersUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'birthdate']

    def clean_first_name(self):
        _dict = super(RegisterForm, self).clean()
        return _dict['first_name'].capitalize()

    def clean_last_name(self):
        _dict = super(RegisterForm, self).clean()
        return _dict['last_name'].capitalize()

    def clean_email(self):
        if UsersUser.objects.filter(email__iexact=self.data['email']).exists():
            raise forms.ValidationError('This email is already registered')
        return self.data['email']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['icon_name'] = "fa fa-envelope"
        self.fields['first_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['last_name'].widget.attrs['icon_name'] = "fa fa-user"
        self.fields['password1'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['password2'].widget.attrs['icon_name'] = "fa fa-lock"
        self.fields['birthdate'].widget.attrs['icon_name'] = "fa fa-calender"


class RegisterForm2(UserCreationForm):
    class Meta:
        model = UsersUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'birthdate',
         'is_superuser', 'is_staff', 'is_active', 'date_joined']



class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/auth/login/'

    def form_valid(self, form):
        data = self.request.POST.copy()
        data['is_superuser']=0
        data['is_staff']=0
        data['is_active']=0
        data['date_joined']=datetime.today().date()
        form = RegisterForm2(data)
        
        user = form.save()
        messages.success(self.request, 'Hi %s,' % user.first_name)
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

@login_required(login_url='/auth/login/')
def no_posts(request,id):
    #id = request.GET.get('id')
    if(Authors.objects.filter(id=id).exists()):
     author=Authors.objects.filter(id=id)[0]
     posts=Posts.objects.filter(author_id=id)
     number=posts.count()
     return render(request, 'display.html', {'author': author, 'number': number})
    else: 
     return HttpResponse("No author found")

@login_required(login_url='/auth/login/')
def posts(request,id):
    #id = request.GET.get('id')
    if(Posts.objects.filter(id=id).exists()):
     post=Posts.objects.filter(id=id)[0]
     author=Authors.objects.filter(id=post.author_id)[0]
     return render(request, 'display2.html', {'post': post, 'author' : author})
    else: 
     return HttpResponse("No post found")

@login_required(login_url='/auth/login/')
def all_posts(request):
    posts=Posts.objects.all().order_by('id')
    data=[]
    for i in posts:
      author=Authors.objects.filter(id=i.author_id)[0]  
      data.append(author)
    number=posts.count()
    return render(request, 'display3.html', {'data': data, 'number': number})