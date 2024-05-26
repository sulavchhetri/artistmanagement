from rest_framework.views import APIView
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from django.db import connection

User = get_user_model()


class ViewUsers(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/user/login/')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * from user_User order by created_at asc")
            users = cursor.fetchall()

        paginator = Paginator(users, 5)  # Show 5 users per page
        try:
            page_number = int(request.GET.get('page'))
        except Exception as e:
            page_number = 1
        page_obj = paginator.get_page(page_number)
        user_details = [(user[6], user[7], user[5], user[-1]) for user in users]
        user_details = user_details[(page_number - 1) * 5:5 * page_number]
        return render(request, 'user/users.html',
                      {'users': user_details, 'page_obj': page_obj, 'active_user': request.user.is_authenticated,
                       'active_email': request.user.email})


class ModifyUser(APIView):
    def get(self, request, pk=None):
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * from user_User where id={pk}")
            user = cursor.fetchone()
        if user:
            _, _, _, _, _, user_id, first_name, last_name, _, phone, dob, address, created_at, updated_at, gender, email = user
            context = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'address': address,
                'dob': dob.strftime('%Y-%m-%d'),
                'gender': gender,
                'modify': True,
                'active_user': request.user.is_authenticated
            }
            return render(request, 'user/register.html', context)

    def post(self, request, pk=None):
        user = User.objects.get(id=pk)
        password = request.POST.get('password')
        email = request.POST.get('email')
        dob = datetime.strptime(request.POST.get('dob'), '%Y-%m-%d').date()

        # Validate the data
        validated, message = validate_credentials(email=email, password=password, dob=dob, check_email=False)
        if not validated:
            return render(request, 'user/register.html', context={'error': message})
        # Update user details
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = email
        if password:
            user.set_password(password)
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.dob = dob
        user.gender = request.POST.get('gender')
        user.updated_at = datetime.now()
        user.save()
        return redirect('/all/')


class DeleteUser(APIView):
    def post(self, request, pk=None):
        user = User.objects.filter(id=pk).first()
        user.delete()
        return redirect('/all/')


class ViewUser(APIView):
    def get(self, request, pk=None):
        if not request.user.is_authenticated:
            return redirect('/user/login/')

        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * from user_User where id={pk}")
            user = cursor.fetchone()
        if user:
            _, _, _, _, _, user_id, first_name, last_name, _, phone, dob, address, created_at, updated_at, gender, email = user
            context = {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'phone': phone,
                'address': address,
                'dob': dob.strftime('%Y-%m-%d'),
                'gender': gender,
                'updated_at': updated_at.strftime('%Y-%m-%d'),
                'created_at': created_at.strftime('%Y-%m-%d'),
                'active_user': request.user.is_authenticated
            }
            return render(request, 'user/user.html', context=context)


def validate_credentials(email, password, dob, check_email=False):
    if '@' not in email or '.' not in email:
        return False, "Invalid Email Address"
    user = User.objects.filter(email=email)
    if check_email:
        if user:
            return False, "Email address already exists"
    if len(password) < 6:
        return False, "Password should be at least 6 characters long"
    if password.isalpha():
        return False, "Password must contain at least one number"
    try:
        if dob > datetime.now().date():
            return False, "Enter correct date of birth"
    except Exception as e:
        return False, "Enter correct date of birth"
    return True, ""


class RegisterView(APIView):
    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        gender = request.POST['gender']
        password = request.POST['password']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['dob']
        dob = datetime.strptime(dob, '%Y-%m-%d').date()
        address = request.POST['address']

        # Validation
        validated, message = validate_credentials(email=email, password=password, dob=dob, check_email=True)

        if not validated:
            return render(request, 'user/register.html',
                          context={'error': message, 'active_user': request.user.is_authenticated})
        user = User.objects.create_superuser(email=email, password=password, first_name=first_name, last_name=last_name,
                                             phone=phone, address=address, dob=dob, gender=gender)
        user.save()
        return redirect('/user/login/')

    def get(self, request):
        return render(request, 'user/register.html', context={'active_user': request.user.is_authenticated})


class LoginView(APIView):
    def post(self, request):
        email, password = request.POST['email'], request.POST['password']
        user = User.objects.filter(email=email).first()
        if user:
            if not check_password(password=password, encoded=user.password):
                user = None
        if user:
            login(request, user)
            return redirect('/')

        return render(request, 'user/login.html', {'error': 'Invalid email or password!'})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'user/login.html')


def logout_view(request):
    logout(request)
    return redirect('/')


class DashboardView(APIView):
    def get(self, request):
        authenticated = request.user.is_authenticated
        user = request.user.email.split("@")[0] if authenticated else None
        return render(request, 'dashboard.html', {'active_user': authenticated, 'user': user})
