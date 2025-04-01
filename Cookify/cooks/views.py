from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.models import User
from django.db.utils import IntegrityError, OperationalError
from django.core.exceptions import ValidationError
from themes.models import WebSetting
from .models import Cook, KitchenBook

# Helper functions
def handle_error(request, message:str, show_msg:str):
    created_user_id = request.session.pop('created_user_id', None)
    if created_user_id:
        created_user = User.objects.get(pk=created_user_id)
        created_user.delete()
    messages.error(request, message, extra_tags=show_msg)
    return redirect('../login')

# Create your views here.
def login(request):
    if not request.POST:
        context = {'websetting': WebSetting.objects.last()}
        # Check whether the error message should be shown in the signup panel and add it to the context
        context['show_err_on_signup'] = any('on_signup' in message.tags 
                                            for message in messages.get_messages(request))
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
            return redirect('../home')
        
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
            return redirect('../home')

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