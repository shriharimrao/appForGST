from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .forms import (
    UserRegistrationForm,
    LoginForm,
    CreateItem,
    UpdateItem,
    ExcelFileForm,
    CreateGst,
)
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import GSTIN, Item
from django.contrib import messages
from django.forms import ValidationError
import openpyxl
from django.urls import reverse
import re


# home page
def home(request):
    is_loggedin = request.user.is_authenticated
    return render(request, "webapp/index.html", context={"is_loggedin": is_loggedin})


# register
def register(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("my-login")
    context = {"form": form}
    return render(request, "webapp/register.html", context=context)


# login
def my_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("gstview")
    context = {"form": form}
    return render(request, "webapp/my-login.html", context=context)


# gstview
@login_required(login_url="my-login")
def gstview(request):
    items = GSTIN.objects.all()
    return render(request, "webapp/gst_list.html", context={"items": items})

#create gstin
@login_required(login_url="my-login")
def creategstinform(request):
    form = CreateGst()
    if request.method == "POST":
        form = CreateGst(request.POST)
        if form.is_valid():
            gstin = form.cleaned_data['gstin_number']
            regex_pattern = "^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"
            if not re.match(regex_pattern, gstin):
                form.add_error('gstin_number', 'Invalid GSTIN format')
            else:
                gstin_object = form.save()
                dashboard_url = reverse("dashboard", kwargs={"gstin": gstin_object.gstin_number})
                return redirect(dashboard_url)

    context = {"form": form}
    return render(request, "webapp/create_gstin.html", context=context)

#delete gstin

def delete_gst(request, gstin):
    try:
        gstin_instance = GSTIN.objects.get(gstin_number=gstin)
        gstin_instance.delete()
    except GSTIN.DoesNotExist:
        messages.error(request, 'GSTIN not found.')
    return  redirect("gstview")


# dashboard
@login_required(login_url="my-login")
def dashboard(request, gstin):
    gstin_instance = get_object_or_404(GSTIN, gstin_number=gstin)
    items = Item.objects.filter(gstin=gstin_instance)
    context = {"items": items, "gstin": gstin_instance}
    return render(request, "webapp/dashboard.html", context)


# create item list
@login_required(login_url="my-login")
def create_item(request, gstin):
    form = CreateItem()
    if request.method == "POST":
        form = CreateItem(request.POST)
        if form.is_valid():
            invoice_object = form.save(commit=False)
            gstin = get_object_or_404(GSTIN, gstin_number=gstin)
            invoice_object.gstin = gstin
            invoice_object.save()
            dashboard_url = reverse("dashboard", kwargs={"gstin": gstin.gstin_number})
            return redirect(dashboard_url)
    context = {"form": form}
    return render(request, "webapp/create-item.html", context=context)


# upload invoice
@login_required(login_url="my-login")
def Upload_item(request, gstin):
    excel_form = ExcelFileForm()
    if request.method == "POST":
        input_method = request.POST.get("input_method")
        if input_method == "upload_excel":
            excel_file = request.FILES["excel_file"]
            try:
                wb = openpyxl.load_workbook(excel_file)
                worksheet = wb.active
                gstin = get_object_or_404(GSTIN, gstin_number=gstin)
                for name, quantity, unit, rate in worksheet.iter_rows(
                    min_row=2, values_only=True
                ):
                    Item.objects.create(
                        name=name, quantity=quantity, unit=unit, rate=rate, gstin=gstin
                    )
                messages.success(request, "Data successfully imported from Excel file.")
                dashboard_url = reverse(
                    "dashboard", kwargs={"gstin": gstin.gstin_number}
                )
                return redirect(dashboard_url)
            except openpyxl.utils.exceptions.EmptySheetError:
                messages.error(request, "The Excel file is empty.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
    context = {"excel_form": excel_form}
    return render(request, "webapp/Upload-item.html", context=context)


# update invoice
@login_required(login_url="my-login")
def update_item(request, pk):
    item = Item.objects.get(id=pk)
    form = UpdateItem(instance=item)
    if request.method == "POST":
        form = UpdateItem(request.POST, instance=item)
        if form.is_valid():
            item_object = form.save()
            dashboard_url = reverse(
                "dashboard", kwargs={"gstin": item_object.gstin.gstin_number}
            )
            return redirect(dashboard_url)
    context = {"form": form, "item": item}
    return render(request, "webapp/update-item.html", context=context)


# delete item
@login_required(login_url="my-login")
def delete_item(request, pk):
    item = Item.objects.get(id=pk)
    if item:
        item.delete()
        messages.success(request, "your invoice was deletd!")
        dashboard_url = reverse("dashboard", kwargs={"gstin": item.gstin.gstin_number})
        return redirect(dashboard_url)


# user logout
def user_logout(request):
    auth.logout(request)
    return redirect("my-login")
