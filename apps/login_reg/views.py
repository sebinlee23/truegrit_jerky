from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    if 'fname' not in request.session:
        request.session['fname'] = ""
    if 'lname' not in request.session:
        request.session['lname'] = ""
    if 'email' not in request.session:
        request.session['email'] = ""
    if 'login_email' not in request.session:
        request.session['login_email'] = ""
    return render(request, "login_reg/index.html")

def username(request):
    import re
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    found = False
    if not EMAIL_REGEX.match(request.POST['email']):
        found = 2
    users = User.objects.filter(email = request.POST['email'])
    if len(users) > 0:
        found = True
    context = {
        "found": found
    }
    return render(request, 'login_reg/partials/username.html', context)

def password(request):
    import re
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    found = False
    if len(request.POST['password']) < 8:
        found = 2
    context = {
        "found": found
    }
    return render(request, 'login_reg/partials/password.html', context)

def register(request):
    import bcrypt
    if request.method == "POST":
        request.session['fname'] = request.POST['fname']
        request.session['lname'] = request.POST['lname']
        request.session['email'] = request.POST['email']
        errors = User.objects.validate(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = 'register')
            return redirect('/register')
        else: 
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            the_user = User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'], password = hashed_pw)
            request.session['user_id'] = the_user.id
            messages.success(request, 'Registered successfully!', extra_tags = 'success')
            return redirect('/profile')

def login(request):
    import bcrypt
    if request.method == "POST":
        request.session['login_email'] = request.POST['login_email']
        errors_2 = User.objects.login_validate(request.POST)
        if len(errors_2) > 0:
            for key, value in errors_2.items():
                messages.error(request, value, extra_tags = 'login')
            return redirect('/register')
        this_user = User.objects.get(email=request.POST['login_email'])
        if bcrypt.checkpw(request.POST['login_password'].encode(), this_user.password.encode()):
            request.session['user_id'] = this_user.id
            if this_user.program != None:
                request.session['sub_id'] = this_user.program.id
            messages.success(request, 'Signed in successfully!', extra_tags = 'success')
            return redirect('/profile')
        else:
            messages.error(request, 'Login information invalid', extra_tags = 'login')
            return redirect('/register')

def profile(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to view that page', extra_tags = 'not_logged_in')
        return redirect('/register')
    this_user = User.objects.get(id = request.session['user_id'])
    flavors = Flavors.objects.all()
    preferences = this_user.prefer_flavor.all()
    order = this_user.order.all()
    context = {
        'user': this_user,
        'flavor': flavors,
        'preference':preferences,
        'orders': order
    }
    return render(request, "login_reg/profile.html", context)

def edit(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to view that page', extra_tags = 'not_logged_in')
        return redirect('/register')
    this_user = User.objects.get(id = request.session['user_id'])
    context = {
        'user': this_user,
    }
    return render(request, "login_reg/edit.html", context)

def edit_profile(request):
    if request.method == "POST":
        import re
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        this_user = User.objects.get(id = request.session['user_id'])
        errors_3 = {}
        if len(request.POST['fname']) == 0 or len(request.POST['lname']) == 0 or len(request.POST['email']) == 0:
            errors_3['no_input'] = 'All fields are required'
        if not EMAIL_REGEX.match(request.POST['email']) and len(request.POST['email']) != 0:
            errors_3['invalid_email'] = 'Your email is invalid'
        if len(request.POST['fname']) < 2 and len(request.POST['fname']) != 0:
            errors_3['short_fname'] = 'First name should be at least 2 charactes long'
        if len(request.POST['lname']) < 2 and len(request.POST['lname']) != 0:
            errors_3['short_lname'] = 'Last name should be at least 2 charactes long'
        email = User.objects.exclude(email = this_user.email)
        for this_email in email:
            if request.POST['email'] == this_email.email:
                errors_3['same_email'] = 'That email already exists in our database'
        if len(errors_3) > 0:
            for key, value in errors_3.items():
                messages.error(request, value)
            return redirect('/edit')
        else:
            update_account = User.objects.get(id = request.session['user_id'])
            update_account.first_name = request.POST['fname']
            update_account.last_name = request.POST['lname']
            update_account.email = request.POST['email']
            update_account.save()
            messages.success(request, 'Account updated successfully', extra_tags = 'success')
            return redirect('/profile')


def clear_reg(request):
    if request.method == "POST":
        del request.session['fname']
        del request.session['lname']
        del request.session['email']
        del request.session['login_email']
    return redirect('/')

def log_out(request):
    del request.session['user_id']
    if 'sub_id' in request.session:
        del request.session['sub_id']
    messages.success(request, 'Logged out successfully!', extra_tags = 'not_logged_in')
    return redirect('/register')

def add_sheriff(request):
    if request.method == "POST":
        this_user = User.objects.get(id = request.session['user_id'])
        program = Programs.objects.get(id = 1)
        this_user.program = program
        this_user.save()
        this_user = User.objects.get(id = request.session['user_id'])
        request.session['sub_id'] = this_user.program.id
        return redirect('/profile')
def add_cowboy(request):
    if request.method == "POST":
        this_user = User.objects.get(id = request.session['user_id'])
        program = Programs.objects.get(id = 2)
        this_user.program = program
        this_user.save()
        this_user = User.objects.get(id = request.session['user_id'])
        request.session['sub_id'] = this_user.program.id
        return redirect('/profile')
def add_outlaw(request):
    if request.method == "POST":
        this_user = User.objects.get(id = request.session['user_id'])
        program = Programs.objects.get(id = 3)
        this_user.program = program
        this_user.save()
        this_user = User.objects.get(id = request.session['user_id'])
        request.session['sub_id'] = this_user.program.id
        return redirect('/profile')


def like(request, flavor_id):
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to view that page', extra_tags = 'not_logged_in')
        return redirect('/register')
    id = request.session['user_id']
    this_user = User.objects.get(id = id)
    flavor_to_update = Flavors.objects.get(id = flavor_id)
    if len(this_user.prefer_flavor.filter(id = flavor_id)) > 0:
        print('Already Liked')
        messages.error(request, 'That flavor is already in your preference', extra_tags = 'already')
        return redirect("/profile")
    elif 'sub_id' not in request.session:
        messages.error(request, 'You have to enroll in our program first', extra_tags = 'already')
        return redirect("/profile")
    else:
        flavor_to_update.favorite.add(this_user)
        return redirect("/profile")

def unlike(request, flavor_id):
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to view that page', extra_tags = 'not_logged_in')
        return redirect('/register')
    id = request.session['user_id']
    this_user = User.objects.get(id = id)
    flavor_to_update = Flavors.objects.get(id = flavor_id)
    flavor_to_update.favorite.remove(this_user)
    return redirect("/profile")

def update_sub(request):
    if request.method == "POST":
        if request.POST.get('program') == str(4):
            print('hello')
            this_user = User.objects.get(id = request.session['user_id'])
            this_user.program = None
            this_user.save()
            del request.session['sub_id']
            this_user.prefer_flavor.clear()
            return redirect('/profile')
        else: 
            print('Update Please!!')
            pro = request.POST.get('program')
            print(pro)
            this_user = User.objects.get(id = request.session['user_id'])
            program = Programs.objects.get(id = pro)
            this_user.program = program
            this_user.save()
            # this_user = User.objects.get(id = request.session['user_id'])
            request.session['sub_id'] = this_user.program.id
            return redirect('/profile')


