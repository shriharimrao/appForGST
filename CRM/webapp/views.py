from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from .forms import (
    UserRegistrationForm,
    LoginForm,
    CreateInvoice,
    UpdateInvoice,
    ExcelFileForm,
    CreateGst,
)
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import pandas as pd
from .models import GSTIN, Item
from django.contrib import messages
from django.forms import ValidationError
import openpyxl
from decimal import Decimal
from django.urls import reverse


# home page
def home(request):
    return render(request, "webapp/index.html")


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


# creategst
@login_required(login_url="my-login")
def creategstinform(request):
    form = CreateGst()
    if request.method == "POST":
        form = CreateGst(request.POST)
        if form.is_valid():
            gstin_object = form.save()
            print("GSTIN_OBJ", gstin_object.__dict__)
            dashboard_url = reverse(
                "dashboard", kwargs={"gstin": gstin_object.gstin_number}
            )
            return redirect(dashboard_url)
    context = {"form": form}
    return render(request, "webapp/create_gstin.html", context=context)


# dashboard
@login_required(login_url="my-login")
def dashboard(request, gstin):
    gstin_instance = get_object_or_404(GSTIN, gstin_number=gstin)
    items = Item.objects.filter(gstin=gstin_instance)
    context = {"items": items, "gstin": gstin_instance}
    return render(request, "webapp/dashboard.html", context)


# create invoice
@login_required(login_url="my-login")
def create_invoice(request, gstin):
    print("GSTIN", gstin)
    print("IFGSTIN INTSCE", isinstance(gstin, GSTIN))
    form = CreateInvoice()
    if request.method == "POST":
        form = CreateInvoice(request.POST)
        if form.is_valid():
            invoice_object = form.save(commit=False)
            gstin = get_object_or_404(GSTIN, gstin_number=gstin)
            invoice_object.gstin = gstin
            invoice_object.save()
            dashboard_url = reverse("dashboard", kwargs={"gstin": gstin.gstin_number})
            return redirect(dashboard_url)
    context = {"form": form}
    return render(request, "webapp/create-invoice.html", context=context)


# upload invoice
@login_required(login_url="my-login")
def Upload_invoice(request, gstin):
    excel_form = ExcelFileForm()
    print("Request method", request.method)
    if request.method == "POST":
        input_method = request.POST.get("input_method")
        print("Input Method", input_method)
        if input_method == "upload_excel":
            # excel_form = ExcelFileForm(request.POST, request.FILES)

            print("is valid")
            excel_file = request.FILES["excel_file"]
            try:
                wb = openpyxl.load_workbook(excel_file)
                worksheet = wb.active
                gstin = get_object_or_404(GSTIN, gstin_number=gstin)
                for name, quantity, unit, rate in worksheet.iter_rows(
                    min_row=2, values_only=True
                ):
                    print(name, quantity, unit, rate)
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
    return render(request, "webapp/Upload-invoice.html", context=context)


# update invoice
@login_required(login_url="my-login")
def update_invoice(request, pk):
    item = Item.objects.get(id=pk)
    form = UpdateInvoice(instance=item)
    if request.method == "POST":
        form = UpdateInvoice(request.POST, instance=item)
        if form.is_valid():
            item_object = form.save()
            dashboard_url = reverse(
                "dashboard", kwargs={"gstin": item_object.gstin.gstin_number}
            )
            return redirect(dashboard_url)
    context = {"form": form, "item": item}
    return render(request, "webapp/update-invoice.html", context=context)


# view single record
@login_required(login_url="my-login")
def singular_invoice(request, pk):
    all_records = Item.objects.get(id=pk)

    context = {"item": all_records}

    return render(request, "webapp/view-invoice.html", context=context)


# delete invoice
@login_required(login_url="my-login")
def delete_invoice(request, pk):
    """
    request : request,
    pk : ID of Invoice
    returns : Dashboard URL
    """
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
