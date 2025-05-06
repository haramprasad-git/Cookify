import os
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import authenticate, update_session_auth_hash, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.utils import IntegrityError, OperationalError
from django.core.exceptions import ValidationError
from .models import Cook, KitchenBook, delete_image_from_file_system

# Helper functions
def handle_error(request, message:str, show_msg:str, redirect_view_name='login'):
    if redirect_view_name == 'login':
        django_logout(request)
    created_user_id = request.session.pop('created_user_id', None)
    if created_user_id:
        created_user = User.objects.get(pk=created_user_id)
        created_user.delete()
    messages.error(request, message, extra_tags=show_msg)
    return redirect(reverse(redirect_view_name))

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
            if not url_has_allowed_host_and_scheme(next_url, allowed_hosts=request.get_host()):
                next_url = ""
                print("Redirecting to home")
            return redirect(f"../../{next_url}")
    
def logout(request):
    django_logout(request)
    return redirect(reverse('home'))
        
def signup(request):
    if not request.POST:
        return redirect(login)
    else:   
        name = request.POST.get('name')
        profile_pic = request.FILES.get('profile_pic', 'profile_pictures/default.png')
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
                profile_picture=profile_pic
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
            print(e)
            return handle_error(request, 'Sorry, Unexpected Error occured !', 'on_signup')

@login_required
def edit_profile(request):
    if not request.POST:
        # Check whether the error message should be shown in the signup panel and add it to the context
        context = {'show_err_on_password': any('on_password' in message.tags 
                                            for message in messages.get_messages(request))
        } 
        return render(request, 'cook/edit-profile.html', context)
    
    name = request.POST.get('name')
    profile_pic = request.FILES.get('profilePic')
    remove_profile_pic = request.POST.get('removeProfilePic')
    instagram = request.POST.get('instagram')
    facebook = request.POST.get('facebook')
    x = request.POST.get('x')
    threads = request.POST.get('threads')

    if not name:
        return handle_error(request, "Please fill all required fields !", 'on_general', redirect_view_name='edit_profile')
    
    try:
        cook: Cook = request.user.cook
        if remove_profile_pic:
            profile_pic = "profile_pictures/default.png"
            delete_image_from_file_system(None, instance=cook)
            
        cook.name = name
        if profile_pic:
            old_profile_picture = cook.profile_picture
            cook.profile_picture = profile_pic
        cook.instagram = instagram
        cook.facebook = facebook
        cook.x = x
        cook.threads = threads
        cook.save()
        cook.full_clean()
        if profile_pic:
            os.remove(old_profile_picture)
        return redirect(reverse('cook_profile', args=[cook.id]))
    
    except ValidationError as e:
        delete_image_from_file_system(None, instance=cook)
        return handle_error(request, e.messages[0], 'on_general', redirect_view_name='edit_profile')
    except Exception as e:
        print(e)
        return handle_error(request, "Sorry, Unexcpected Error occured !", 'on_general', redirect_view_name='edit_profile')

@login_required
def change_password(request):
    if not request.POST:
        return redirect(reverse('edit_profile'))
    
    current_password = request.POST.get("currentPassword")
    new_email = request.POST.get("email")
    new_password = request.POST.get("newPassword")

    if not (current_password or new_email):
        return handle_error(request, "Please fill all required fields !", 'on_password', redirect_view_name='edi_profile')
    
    user = authenticate(username=request.user.username, password=current_password)
    if not user:
        return handle_error(request, "Incorrect password !", 'on_password', redirect_view_name='edit_profile')

    try:
        user.username = new_email
        if new_password:
            user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return redirect(reverse('edit_profile'))
    except IntegrityError:
        return handle_error(request, "Email is already registered !", 'on_password', redirect_view_name='edit_profile')
    
    except ValueError:
        return handle_error(request, 'Invalid Data !', 'on_password', redirect_view_name='edit_profile')    
    
    except OperationalError:
        return handle_error(request, 'Sorry, Password changing Failed !', 'on_password', redirect_view_name='edit_profile')
    
    # except Exception:
    #     return handle_error(request, 'Sorry, Unexpected error occured !', 'on_password', redirect_view_name='edit_profile')
    
        
def show_profile(request, id):
    cook = get_object_or_404(Cook, id=id)    
    return render(request, 'cook/profile-page.html', {'cook': cook})

@login_required
def follow_or_unfollow(request, target):
    if target == request.user.cook.id:
        # Prevent Self Following
        messages.info(request, "You can't follow yourself")
        return redirect(reverse('cook_profile', args=[target]))
    
    kitchen_book: KitchenBook = request.user.cook.kitchen_book
    target_cook = get_object_or_404(Cook, id=target)

    if not kitchen_book.followed_cooks.contains(target_cook):
        # Follow
        kitchen_book.followed_cooks.add(target_cook)
    else:
        # Unfollow
        kitchen_book.followed_cooks.remove(target_cook)
    
    return redirect(reverse('cook_profile', args=[target]))

@login_required
def show_kitchen_book(request):
    kitchenbook = request.user.cook.kitchen_book
    return render(request, 'cook/kitchen-book.html', {'kitchenbook': kitchenbook})