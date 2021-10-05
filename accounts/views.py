from django.contrib.auth.models import Group
from django.db.models.deletion import SET_DEFAULT
from django.db.models.query import QuerySet
from accounts import models
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.forms import inlineformset_factory
from accounts import form
from accounts.decorators import authenticated_user,admin_only,allowed_roles
from accounts.models import *
from accounts.form import *
from .filter import *
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')#if not login redirect to login page
@admin_only#don't put () while setting decorators because it will ask for certain parameters, not putting parameters will take the whole fun under ur specified decorator as parameter.
def dashboard(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()
    total=orders.count()
    delivered=Order.objects.filter(status="delivered").count()
    pending=Order.objects.filter(status="pending").count()
    return render(request,'accounts/dashboard.html',{
        'customers':customers,
        'orders':orders,
        'total':total,
        'delivered':delivered,
        'pending':pending
    })

@login_required(login_url='/login')
@allowed_roles(roles=['customer'])#spell exactly as group name in your SQL server
def customer_profile(request):
    orders=request.user.customer.order_set.all()
    total=orders.count()
    delivered=orders.filter(status="delivered").count()
    pending=orders.filter(status="pending").count()
    return render(request,'accounts/customer_profile.html',{
        'orders':orders,
        'total':total,
        'delivered':delivered,
        'pending':pending
    })

@login_required(login_url='/login')
@allowed_roles(roles=['admin'])
def customers(request,id):
    customer=Customer.objects.get(id=id)
    orders=customer.order_set.all()
    order_count=orders.count()
    filterObj=OrderFilter(request.GET,queryset=orders)
    orders=filterObj.qs
    return render(request,'accounts/customers.html',{
        'customer':customer,
        'orders':orders,
        'order_count':order_count,
        'filterObj':filterObj
    })

@login_required(login_url='/login')
@allowed_roles(roles=['admin'])
def products(request):
    products=Product.objects.all()
    return render(request,'accounts/products.html',{
        'products':products
    })

@login_required(login_url='/login')
@allowed_roles(roles=['admin'])
def ordercreate(request,customerid):
    #inline factory returns as class so name your varible with uppercase 
    Orderformset=inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)#inline_fac takes parent and child model, fields come from child model
    customer=Customer.objects.get(id=customerid)
    formset=Orderformset(instance=customer,queryset=Order.objects.none())
    #form=OrderForm(initial={'customer'}#initial= {put Order model attribute e.g. customer or product or ..}

    if request.method=="POST":
        formset=Orderformset(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    return render(request,'accounts/form.html',{
        'formset':formset
    })

@login_required(login_url='/login')
@allowed_roles(roles=['admin'])
def orderupdate(request,orderid):
    selected_order=Order.objects.get(id=orderid)
    form=OrderForm(instance=selected_order)
    if request.method=="POST":
        form=OrderForm(request.POST,instance=selected_order)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'accounts/form.html',{
        'form':form
    })

@login_required(login_url='/login')
@allowed_roles(roles=['admin'])
def orderDelete(request,orderid):
    selectedorder=Order.objects.get(id=orderid)
    if request.method=="POST":
        selectedorder.delete()
        return redirect('/')
    return render(request,'accounts/orderdelete.html',{
        'order':selectedorder
    })

@authenticated_user
def register(request):
    form=RegisterForm()
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            #add customer gp as default
            gp=Group.objects.get(name='customer')
            user.groups.add(gp)

            login(request,user)
            return redirect('/')

    return render(request,'accounts/register.html',{
        'form':form
    })

@authenticated_user
def userlogin(request):
    if request.method=="POST":
        username=request.POST['username']#username is the name attr in login template
        password=request.POST['password']#pwd is the name attr in login template

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.error(request,"username and password are incorrect please try again.") #flash messages
            return redirect('/login')

    return render(request,'accounts/login.html')

@login_required(login_url='/login')
def userlogout(request):
    logout(request)
    return redirect('/login')