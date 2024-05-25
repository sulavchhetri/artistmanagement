from rest_framework.views import APIView
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator

User = get_user_model()


class ViewUsers(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/user/login/')
        users = User.objects.all().order_by('created_at')
        paginator = Paginator(users, 5)  # Show 5 users per page
        try:
            page_number = int(request.GET.get('page'))
        except Exception as e:
            page_number = 1
        page_obj = paginator.get_page(page_number)
        user_details = [(user.first_name, user.last_name, user.id) for user in users]
        user_details = user_details[(page_number - 1) * 5:5 * page_number]
        return render(request, 'user/users.html',
                      {'users': user_details, 'page_obj': page_obj, 'active_user': request.user.is_authenticated})


class ModifyUser(APIView):
    def get(self, request, pk=None):
        user = User.objects.filter(id=pk).first()
        context = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': user.phone,
            'address': user.address,
            'dob': user.dob.strftime('%Y-%m-%d'),
            'gender': user.gender,
            'modify': True,
            'active_user': request.user.is_authenticated
        }
        return render(request, 'user/register.html', context)

    def post(self, request, pk=None):
        user = User.objects.filter(id=pk).first()

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        gender = request.POST.get('gender')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        dob = request.POST.get('dob')
        dob = datetime.strptime(dob, '%Y-%m-%d').date()
        address = request.POST.get('address')

        # Validate the data
        validated, message = validate_credentials(email=email, password=password, dob=dob)
        # if not validated:
        # messages.error(request, message)
        # return redirect('user_modify', pk=user.id)

        # Update user details
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password:
            user.set_password(password)
        user.phone = phone
        user.address = address
        user.dob = dob
        user.gender = gender
        user.save()
        # messages.success(request, 'User details updated successfully.')
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
        user = User.objects.filter(id=pk).first()
        if user:
            context = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': user.phone,
                'address': user.address,
                'dob': user.dob.strftime('%Y-%m-%d'),
                'gender': user.gender,
                'updated_at': user.updated_at.strftime('%Y-%m-%d'),
                'created_at': user.created_at.strftime('%Y-%m-%d'),
                'active_user': request.user.is_authenticated
            }
            return render(request, 'user/user.html', context=context)


def validate_credentials(email, password, dob):
    if '@' not in email or '.' not in email:
        return False, "Invalid Email Address"
    user = User.objects.filter(email=email)
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
        validated, message = validate_credentials(email=email, password=password, dob=dob)
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
