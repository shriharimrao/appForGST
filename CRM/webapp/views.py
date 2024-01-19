from django.shortcuts import render,redirect
from .forms import UserRegistrationForm, LoginForm ,CreateInvoice,UpdateInvoice,ExcelFileForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import pandas as pd
from .models import Item
from django.contrib import messages
from django.forms import ValidationError
from openpyxl import load_workbook
from decimal import Decimal




#home page
def home(request):
    return render(request,'webapp/index.html')

#register
def register(request):
    form=UserRegistrationForm()
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect ('my-login')
    context={'form':form}
    return render(request,'webapp/register.html',context=context)
    
    
#login
def my_login(request):
    form=LoginForm()
    if request.method=="POST":
        form =LoginForm(request,data=request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request,username=username,password=password)

            if user is not None:
                auth.login(request,user)
                return redirect('dashboard')
    context={'form':form}
    return render(request,'webapp/my-login.html',context=context)


@login_required(login_url='my-login')
def dashboard(request):
    items = Item.objects.all()
    form =ExcelFileForm()  # Define the form outside the conditional block

    if request.method == 'POST':
        input_method = request.POST.get('input_method')
        if input_method == 'upload_excel':
                    form = ExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file)

                # Validation for Excel data
                required_columns = ['name', 'quantity', 'unit', 'rate']
                if not all(column in df.columns for column in required_columns):
                    messages.error(request, "Missing required columns in Excel file.")
                    return redirect('dashboard')

                for index, row in df.iterrows():
                    try:
                        item = Item(
                            name=row['name'],
                            quantity=int(row['quantity']),
                            unit=row['unit'],
                            rate=Decimal(row['rate'])
                        )
                        item.full_clean()
                        item.save()
                    except ValidationError as e:
                        messages.error(request, str(e))

                messages.success(request, "Data successfully imported from Excel file.")
            except pd.errors.EmptyDataError:
                messages.error(request, "The Excel file is empty.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        elif input_method == 'create_data':
                
                my_records = Item.objects.all()

                context = {'items': my_records}

                return render(request, 'webapp/dashboard.html', context=context)

    # Define the context variable here
    context = {'form': form, 'items': items}
    return render(request, 'webapp/dashboard.html', context=context)


#create invoice
@login_required(login_url='my-login')
def create_invoice(request):
    form = CreateInvoice()
    if request.method == 'POST':
            
        form = CreateInvoice(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    context={'form': form}
    return render(request, 'webapp/create-invoice.html',context=context )

#update invoice
@login_required(login_url='my-login')
def update_invoice(request ,pk):
    item=Item.objects.get(id=pk)
    form=UpdateInvoice(instance=item)
    if  request.method=="POST":
        form=UpdateInvoice(request.POST,instance=item)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    context={'form':form}
    return render(request, 'webapp/update-invoice.html',context=context )

#view single record
@login_required(login_url='my-login')
def singular_invoice(request, pk):

    all_records = Item.objects.get(id=pk)

    context = {'item':all_records}

    return render(request, 'webapp/view-invoice.html', context=context)

#delete invoice
@login_required(login_url='my-login')
def delete_invoice(request, pk):
    item=Item.objects.get(id=pk)
    item.delete()
    messages.success(request,"your invoice was deletd!")
    return redirect("dashboard")


















#user logout
def user_logout(request):
    auth.logout(request)
    return redirect("my-login")

