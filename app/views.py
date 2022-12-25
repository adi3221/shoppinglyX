from django.shortcuts import render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm,LoginForm,CustomerProfileForm
from django.contrib import messages

# def home(request):
#  return render(request, 'app/home.html')
class ProductView(View):
    def get(self,request):# filter  according to cateogry based
        topwears = Product.objects.filter(cateogry='TW')#we will filter the TW in products table
        bottomwears = Product.objects.filter(cateogry='Bw')
        mobiles = Product.objects.filter(cateogry='M')
        return render(request,'app/home.html',{'topwears':topwears, 'bottomwears':bottomwears,'mobiles':mobiles})


# def product_detail(request):
#  return render(request, 'app/productdetail.html')

class ProductDetailView(View):
    def get(self, request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,'app/productdetail.html',{'product':product})

def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')


def address(request):
    add = Customer.objects.filter(user=request.user)#to get current user details
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

def orders(request):
 return render(request, 'app/orders.html')

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(cateogry = 'M')
    elif data=='Redmi' or data =='Samsung' or data=='Oppo':
        mobiles = Product.objects.filter(cateogry='M').filter(brand=data)
    elif data=='below':
        mobiles = Product.objects.filter(cateogry='M').filter(discounted_price__lt=10000)
    elif data=='above':
        mobiles = Product.objects.filter(cateogry='M').filter(discounted_price__gt=10000)
    return render(request,'app/mobile.html',{'mobiles':mobiles})
 

# def login(request):
#  return render(request, 'app/login.html')
# noe need to have view as login use default as it is in url

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')
class CustomerRegistrationView(View):
    def get(self,request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})

    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid(): # isme direct save hoga bcoz registeration ek inbuilt form hai 
            messages.success(request,"Congratulations!! Registered Successfully") # ye msg waha jayega jaha ye niche wala render karega
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})


def checkout(request):
 return render(request, 'app/checkout.html')


class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr,name = name, locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations!! Profile Updated Successfully")
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})