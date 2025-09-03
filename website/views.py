from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django_daraja.mpesa.core import MpesaClient

from website.forms import StudentForm
from website.models import Student, Payment


# Create your views here.
def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def events(request):
    return render(request, 'events.html')
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'signup.html')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error':'Invalid credentials'})
    return render(request, 'login.html')

@login_required(login_url='login')
def dashboard(request):
    students = Student.objects.all()
    return render(request, 'dashboard.html',{'students':students})


def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect('dashboard')

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = StudentForm(instance=student)
        return render(request, 'edit_student.html', {'form': form, 'student': student})

def user_logout(request):
    logout(request)
    return redirect('login')

def mpesaapi(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        amount = int(request.POST.get('amount'))
        client = MpesaClient()
        account_reference = 'EMOBILIS'
        transaction_desc = 'Payment for school fees'
        callback_url = 'https://example.com/callback'

        response = client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        res_dict = response.json()
        Payment.objects.create(
            phone = phone_number,
            amount = amount,
            description = res_dict.get("ResponseDescription",""),
            response_code = res_dict.get("ResponseCode",""),
            customer_message_id = res_dict.get("CustomerMessage",""),
            merchant_request_id = res_dict.get("MerchantRequestID",""),
            checkout_request_id = res_dict.get("CheckoutRequestID",""),
            status = "Pending"
        )
        return render(request, "payment_form.html")
    return render(request, 'payment_form.html')