from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import CustomSignUpForm, CustomAuthenticationForm, CustomPasswordChangeForm, CustomSetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
class SignUpCustomView(View):
    view_name = "sign_up"
    def get(self, request):
        form = CustomSignUpForm()
        context = {
            'form' : form
        }
        return render(request, 'register_app/sign_up.html', context)

    def post(self, request):
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            form.save()
        context = {
            'success_msg': "User Successfully Registered"
        }
        return render(request, 'register_app/sign_up.html', context)


class LogInCustomView(View):
    view_name = "log_in"
    def get(self, request):
        if not request.user.is_authenticated:
            form = CustomAuthenticationForm()
            context = {
                'button_value': "LogIn",
                'form' : form
            }
            return render(request, 'register_app/user_generic_login_changepass.html', context)

        # User Logged ovostha ee takhe taile amra "Profile" Page ee niye jabo
        else:
            return HttpResponseRedirect("/register/profile")

    def post(self, request):
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upassword = form.cleaned_data['password']
            user = authenticate(username=uname, password=upassword)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/register/profile")
            else:
                context = {
                    'button_value': "LogIn",
                    'msg': "User couldn't LogIn"
                }
                return render(request, 'register_app/user_generic_login_changepass.html', context)
        else:
            context = {
                'button_value': "LogIn",
                'msg': form.error_messages
            }
            return render(request, 'register_app/user_generic_login_changepass.html', context)

class UserProfileCustomView(View):
    view_name = "user_profile"
    def get(self, request):
        # current SESSION er User jodi Logged-In ovostha ee takhe taile amra ei `request.user.is_authenticated` theke pabo
        if request.user.is_authenticated:
            context = {
                'username' : request.user # USERNAME amra pabo "request.user" eikan theke
            }
            return render(request, 'register_app/user_profile.html', context)

        # User Logged In nah takle abra "Login" Page ee niye jabo
        else:
            return HttpResponseRedirect("/register/login")

class UserLogOutCustomView(View):
    view_name = "user_logout"
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/register/login")



# Change Password with Old Password
class UserChangePasswordCustomView(View):
    view_name = "user_changepass"

    # `dispatch` method decide kore REQUEST jei Object ta ashtese sheita kon TYPE(get, post, delete) er method ke Call dibe
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):  # In Django's class-based views, the dispatch() method is responsible for handling incoming requests and deciding which HTTP method to call. It is the entry point for processing requests in a class-based view.
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        form = CustomPasswordChangeForm(user=request.user)
        context = {
            'button_value': "Change Password",
            'form': form
        }
        return render(request, 'register_app/user_generic_login_changepass.html', context)

    def post(self, request):
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Password Change er Por... automatic SESSION "LOGOUT" hoye jay... ei Behavior Prevent korar jonno amra ei `update_session_auth_hash` er use korbo
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect("/register/profile")
        else:
            context = {
                'button_value': "Change Password",
                'msg': form.error_messages
            }
            return render(request, 'register_app/user_generic_login_changepass.html', context)



# OLD Password "NOT" Needed
@method_decorator(login_required, name='dispatch')  #2nd way --> jate kore LOGIN nah takle amra LOGIN View te niye jabo... eikane `dispatch` hocce "View" Class er ekta Method
class UserForgetPassword(View):
    view_name = "user_changepass_without_oldpass"
    def get(self, request):
        form = CustomSetPasswordForm(user=request.user)
        context = {
            'button_value': "Set Password without Old Passoword",
            'form': form
        }
        return render(request, 'register_app/user_generic_login_changepass.html', context)

    def post(self, request):
        form = CustomSetPasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/register/login")
        else:
            context = {
                'button_value': "Set Password without Old Passoword",
                'msg': form.error_messages
            }
            return render(request, 'register_app/user_generic_login_changepass.html', context)