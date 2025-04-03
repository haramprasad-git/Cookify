from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.utils import IntegrityError, OperationalError
from django.core.exceptions import ValidationError
from .models import Cook, KitchenBook

# Helper functions
def handle_error(request, message:str, show_msg:str):
    django_logout(request)
    created_user_id = request.session.pop('created_user_id', None)
    if created_user_id:
        created_user = User.objects.get(pk=created_user_id)
        created_user.delete()
    messages.error(request, message, extra_tags=show_msg)
    return redirect(reverse('login'))

# Create your views here.
def login(request):
    if not request.POST:
        # Check whether the error message should be shown in the signup panel and add it to the context
        context = {'show_err_on_signup': any('on_signup' in message.tags 
                                            for message in messages.get_messages(request))
                    }
        return render(request, 'cook/login-signup.html', context)
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not (email and password):
            return handle_error(request, 'Please Fill all required fields !', 'on_login')
        
        user = authenticate(username=email, password=password)
        if user is None:
            messages.error(request, 'Incorrect Username / Password !', extra_tags='on_login')
            return redirect(login)
        else:
            django_login(request, user)
            next_url = request.POST.get('next', '')
            if (not next_url) or (url_has_allowed_host_and_scheme(next_url, allowed_hosts=request.get_host())):
                next_url = "../../"
            return redirect(f"../../{next_url}")
        
def signup(request):
    if not request.POST:
        return redirect(login)
    else:   
        name = request.POST.get('name')
        profile_pic = request.FILES.get('profile_pic')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not (name and email and password):
            return handle_error(request, 'Please Fill all required fields !', 'on_signup')
        try:
            user = User.objects.create_user(username=email, password=password)
            request.session['created_user_id'] = user.pk
            cook = Cook.objects.create(
                name=name,
                core_user=user,
                profile_picture = profile_pic
            )
            cook.full_clean()
            cook.save()
            KitchenBook.objects.create(owner=cook)
            django_login(request, user)
            next_url = request.POST.get('next', '')
            if (not next_url) or (url_has_allowed_host_and_scheme(next_url, allowed_hosts=request.get_host())):
                next_url = "../../"
            return redirect(f"../../{next_url}")

        except IntegrityError:
            return handle_error(request, 'Email already registered !', 'on_signup')
        
        except ValidationError as e:
            return handle_error(request, e.messages[0], 'on_signup')
        
        except ValueError:
            return handle_error(request, 'Invalid Data !', 'on_signup')
        
        except OperationalError:
            return handle_error(request, 'Sorry, Cook Creation Failed !', 'on_signup')
        
        except Exception as e:
            return handle_error(request, 'Sorry, Unexpected Error occured !', 'on_signup')
        
def show_profile(request):
    return render(request, 'cook/profile-page.html')