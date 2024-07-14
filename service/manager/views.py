from django.views.generic.list import ListView
from django.views.generic import FormView, TemplateView, UpdateView
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout

from manager.forms import CustomUserCreationForm

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth.models import User

from manager.forms import CustomUserCreationForm, UserUpdateForm

from django.http import HttpResponseForbidden


class AdminRequiredMixin:
    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_superuser:
            return HttpResponseForbidden()
        return super().dispatch(*args, **kwargs)


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'manager/base.html'
    login_url = reverse_lazy('log')


class ProfilesView(AdminRequiredMixin, ListView):
    queryset = User.objects.all()
    template_name = 'manager/profiles_list.html'


class ProfileView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'manager/profile.html'

    def get_object(self):
        return User.objects.get(id=self.kwargs['profile_id'])
    
    def get_initial(self):
        user = self.object
        initial = super().get_initial()
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email
        return initial
    
    def get_context_data(self):
        context = super().get_context_data()
        context['profile'] = self.object
        return context
    
    def get_success_url(self):
        return self.request.path
    

class ProfileCreateView(AdminRequiredMixin, FormView):
    form_class = CustomUserCreationForm
    template_name = 'manager/profile_create.html'
    success_url = reverse_lazy('profiles')
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

@staff_member_required
def delete_user(request, profile_id=None):
    user = User.objects.get(id=profile_id)
    if user:
        user.delete()
        return HttpResponseRedirect(reverse_lazy('profiles'))
    return HttpResponseRedirect(reverse_lazy('base'))


class UserCreateView(FormView):
    form_class = CustomUserCreationForm
    template_name = 'manager/reg.html'
    success_url = reverse_lazy('base')
    
    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
        login(self.request, user)
        return super().form_valid(form)
    

class CustomLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'manager/login.html'

    def get_success_url(self):
        return reverse_lazy('base')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('base'))


