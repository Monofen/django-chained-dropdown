
from django.shortcuts import redirect, render, get_object_or_404
from .models import Categories, Product, Customer, Order
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone

def index(request):
    categories = Categories.objects.filter(parent=None)
    return render(request, 'test.html', {'categoryData': categories})

def category_view(request, category_id):
    category = get_object_or_404(Categories, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'category': category, 'products': products})

def billing_page(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'billing_page.html', context)

def place_order(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        quantity = int(request.POST.get('quantity', 1))  
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        
        customer, created = Customer.objects.get_or_create(email=email)
        customer.first_name = first_name
        customer.last_name = last_name
        customer.phone = phone
        customer.save()

        order = Order.objects.create(
            product=product,
            customer=customer,
            quantity=quantity,
            address=address,
            phone=phone,
            date=timezone.now(),
            status=False  
        )


        return render(request, 'order_confirmation.html', {'order': order})

    
    return redirect('index')  

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        
        try:
            customer = Customer.objects.get(email=email)
            request.session['customer_id'] = customer.id  
            if customer.password:
                
                return render(request, 'login_password.html', {'customer': customer})
            else:
                
                return render(request, 'create_password.html', {'customer': customer})
        except Customer.DoesNotExist:
           
            return redirect('signup')  

    return render(request, 'login.html')

def create_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        customer_id = request.POST.get('customer_id')
        
        
        customer = get_object_or_404(Customer, pk=customer_id)
        customer.password = make_password(password)
        customer.save()
        
       
        return redirect('login')  

    return render(request, 'create_password.html')

def login_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')
        
       
        customer = get_object_or_404(Customer, email=email)
        if customer.password: 
            if check_password(password, customer.password):
                request.session['customer_id'] = customer.id  
                
               
                return redirect('order_list')  
            else:
              
                return render(request, 'login_password.html', {'error': 'Incorrect password'})
        else:
          
            return render(request, 'login_password.html', {'error': 'Please create a password'})

    return render(request, 'login_password.html')

def order_list(request):
   
    customer_id = request.session.get('customer_id')
    if customer_id:
        orders = Order.objects.filter(customer_id=customer_id)
        return render(request, 'order_list.html', {'orders': orders})
    else:
       
        return render(request, 'order_list.html', {'orders': None})

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')  
        password = request.POST.get('password')

        existing_customer = Customer.objects.filter(email=email).exists()

        if existing_customer:
            return redirect('login')

        if not phone:
            return render(request, 'signup.html', {'error_message': 'Phone number is required.'})

        hashed_password = make_password(password)

        customer = Customer.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone, 
            password=hashed_password
        )

        return redirect('login')

    return render(request, 'signup.html')