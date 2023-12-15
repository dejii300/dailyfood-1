from decimal import Decimal
from venv import logger
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from .models import *
from .forms import *
from django.forms import inlineformset_factory, modelformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
from .utils import *
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
import json
from django.contrib.auth.forms import PasswordChangeForm
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
import logging

@csrf_exempt
def extract_keywords(request):
    text = request.POST.get('text')
    return JsonResponse(text)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def Index(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    categories = Category.objects.all()
    comments = Comment.objects.filter(approved=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Assuming you are using the default User model
            comment.save()
            # Additional logic or redirection after saving the comment if needed
            return redirect('comment_success')  # You can define this URL in your urls.py
    else:
        form = CommentForm()

    context = {'comments': comments,'messages': messages, 'form': form, 'cartItems': cartItems, 'items': items, 'categories': categories}

    return render(request, 'chops/index.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def ChopsView(request):
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {'products':products, 'categories':categories, 'items': items, 'cartItems':cartItems}
    return render(request, "chops/chops.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def product_category(request, category):

    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']
    categories = Category.objects.all()
    products = Product.objects.filter(
        category__name__contains=category
    )  
    context = {
        "Category": category,
        "products": products,
        'categories': categories,
        'cartItems': cartItems,
        'items': items,
    }
    return render(request, "chops/products_category.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def ChopsDetail(request, product_id):
    categories = Category.objects.all()
    product = Product.objects.get(pk=product_id)
    data = cartData(request)
    cartItems = data['cartItems']
    items = data['items']  
    context = {'items': items, 'product':product,  'cartItems': cartItems, 'categories': categories }
    return render(request, 'chops/chops_detail.html',  context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def cart(request):
    categories = Category.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']   

    context = {'items': items, 'order': order, 'cartItems': cartItems, 'categories': categories }
    return render(request, "chops/cart.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def checkout(request):
    categories = Category.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    if not items:
        # Redirect or handle the case where the cart is empty
        return redirect('')

    # Retrieve the delivery price associated with the customer
    customer = Customer.objects.get(user=request.user)
    delivery = Delivery.objects.filter(customer=customer).first()
    delivery_price = delivery.price if delivery else 0  # Set a default if no delivery is found

    # Placeholder for updated_total; replace it with the actual calculation
    updated_total = order.get_cart_total + delivery_price
    print(f"update total : {updated_total}")
    context = {'items': items, 'order': order, 'cartItems': cartItems, 'updated_total': updated_total, 'categories': categories }

    return render(request, "chops/checkout.html", context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def updateItem(request):
    data = json.loads(request.body)
    productId = data.get('productId')
    action = data.get('action')
    quantity = data.get('quantity', 1) 

    print('Before Processing - productId:', productId)
    print('Before Processing - action:', action)
    print('Before Processingebj - quantity:', quantity)

    if not productId or action not in ['add', 'delete']:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    try:
        customer = request.user.customer
        print('Customer ID:', customer.id)

        product = Product.objects.get(id=productId)
        print('Product Name:', product.name) 

        order, created_order = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created_order_item= OrderItem.objects.get_or_create(order=order, product=product)

        print('OrderItem ID:', orderItem.id)  # Debug line
        print('OrderItem Quantity (before):', orderItem.quantity)

        if action == 'add':
            new_quantity = max(0, int(quantity))
            orderItem.quantity = new_quantity
        
            
        

            

            orderItem.save()
               

        elif action == 'delete':
            orderItem.delete()
            return JsonResponse({'message': 'Item deleted successfully'}, status=200)

        print('OrderItem Quantity (after):', orderItem.quantity)

        return JsonResponse({'message': f'Item {action}ed successfully'}, status=200)

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=400)

    except Exception as e:
        print('Error:', str(e))  
        return JsonResponse({'error': str(e)}, status=500)
    

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def shipping_view(request):
    
    # Retrieve the current customer
    customer = Customer.objects.get(user=request.user)

    # Retrieve all delivery locations
    delivery_locations = Delivery.objects.all()

    if request.method == 'POST':
        # Handle form submission
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            # Get the selected delivery location and its price
            selected_location = form.cleaned_data['selected_location']
            delivery = Delivery.objects.get(location=selected_location)

            # Associate the delivery with the current customer
            delivery.customer = customer
            delivery.save()

            delivery_price = delivery.price
            form.save()
            print(f"Delivery Price: {delivery_price}")

            return redirect('checkout')
    else:
        # Display the form with delivery location options
        form = ShippingAddressForm()

    context = {'form': form, 'delivery_locations': delivery_locations, }
    return render(request, 'chops/shipping.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        delivery = Delivery.objects.filter(customer=customer).first()
        delivery_price = delivery.price if delivery else 0  # Set a default if no delivery is found

        order,created = Order.objects.get_or_create(customer=customer, complete=False)
        
        
    
        
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total + delivery_price:
            order.complete = True
            order.save()

            return redirect('checkout_successfull')
    else:
        return JsonResponse({'message': 'Payment faild'}, safe=False)



@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        
        if user is not None:
            login(request, user)
            if user.is_staff:
                # Admin user
                return redirect('home') 
            
            elif user.last_login is None:
                return redirect('edit_profile')
            
            else:
                return redirect('index')
           
        else:
            messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'account/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerPage(request):
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid(): 
                #saving the registered user
                user = form.save()
                Customer.objects.create(
                    user = user,
                    name = user.username,
                    
                )    
                username= form.cleaned_data.get('username')
                group = Group.objects.get(name='customer')
                user.groups.add(group)
 
                messages.success(request, f'Your Account has been created! You can now log in')
                return redirect('login')
        else:
            form = CreateUserForm() #creates an empty form
        return render(request, 'account/register.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def ProfilePage(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'account/profile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def edit_profile(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST,request.FILES, instance=request.user.customer)

        if form.is_valid():
            if 'clear_profile_pic' in request.POST:
                form.instance.profile_pic = 'profile1.png'
            print(form.cleaned_data)     
            form.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')  # Redirect to the user's profile page after editing
    else:
        form = CustomerForm(instance=request.user.customer)

    return render(request, 'account/edit_profile.html', {'form': form})

   

@login_required(login_url='login')
@admin_only
def adminD(request):
    orders = Order.objects.all()
    
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders, 'customers': customers, 'total_orders': total_orders, 'delivered': delivered,
        'pending': pending, 'total_customer':total_customers
        }

    return render(request, 'admin/admin_template.html', context)

   

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    print('ORDERS:', orders)
    context = {
        'orders': orders, 'total_orders': total_orders, 'delivered': delivered,
        'pending': pending
        }
    return render(request, 'account/user.html', context)     

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, 'account/products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def admin_user_orders(request):
    orders = Order.objects.all()
    return render(request, 'admin/admin_user_orders.html', {'orders': orders})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        'customer': customer, 'orders': orders, 'order_count': order_count, 'myFilter': myFilter,
        
    }
    return render(request, 'account/customer.html', context) 

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def createproduct(request, pk):
#     OrderFormSet = inlineformset_factory(Customer, Order, fields=('Product', 'status'), extra=20)
    
#     customer = Customer.objects.get(id=pk)
#     formset = OrderFormSet( queryset=Order.objects.none(), instance=customer)
#     #form = OrderForm()
#     if request.method == 'POST':
#        # form = OrderForm(request.POST)
#        formset = OrderFormSet(request.POST, instance=customer)
#        if formset.is_valid():
#             formset.save()
#             return redirect('/')
#     context = {'formset': formset}    
#     return render(request, 'account/order_form.html',context)
  

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def updateproduct(request, pk):
 
#     order = Order.objects.get(id=pk)
#     formset = OrderForm( instance=order)

#     if request.method =='POST':
#         formset = OrderForm(request.POST, instance=order)
#         if formset.is_valid():
#             formset.save()
#             return redirect('/')
#     context = {'formset': formset}
#     return render(request, 'account/order_form.html', context)

# @login_required(login_url='login')
# @allowed_users(allowed_roles=['admin'])
# def deleteproduct(request, pk):
#     order = Order.objects.get(id=pk)
#     if request.method == 'POST':
#         order.delete()   
#         return redirect('/') 
#     context = {'item': order}  
#     return render(request, 'account/delete_form.html', context)    

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product_list(request):
    products = Product.objects.all()
    return render(request, 'admin/product_list.html', {'products': products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'admin/product_detail.html', {'product': product})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'admin/product_form.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin/product_form.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'admin/product_confirm_delete.html', {'product': product})

#Event
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def evtproduct_list(request):
    evtproducts = EvtProduct.objects.all()
    return render(request, 'admin/evtproduct_list.html', {'evtproducts': evtproducts})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def evtproduct_detail(request, pk):
    evtproduct = get_object_or_404(EvtProduct, pk=pk)
    return render(request, 'admin/evtproduct_detail.html', {'evtproduct': evtproduct})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def evtproduct_create(request):
    if request.method == 'POST':
        form = EvtProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('evtproduct_list')
    else:
        form = EvtProductForm()
    return render(request, 'admin/evtproduct_form.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def evtproduct_update(request, pk):
    evtproduct = get_object_or_404(EvtProduct, pk=pk)
    if request.method == 'POST':
        form = EvtProductForm(request.POST, request.FILES, instance=evtproduct)
        if form.is_valid():
            form.save()
            return redirect('evtproduct_detail',pk=pk)
    else:
        form = EvtProductForm(instance=evtproduct)
    return render(request, 'admin/evtproduct_form.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def evtproduct_delete(request, pk):
    evtproduct = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        evtproduct.delete()
        return redirect('product_list')
    return render(request, 'admin/evtproduct_confirm_delete.html', {'evtproduct': evtproduct})



@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def event_form(request):
    evtproducts = EvtProduct.objects.all()
    if request.method == 'POST':
        
        print(request.POST) 
        
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            logger.info(f"Event {event.id} saved successfully.")
            return redirect('review_page', event_id=event.id)
        else:
            print(form.errors)
    else:
        form = EventForm()

    return render(request, 'chops/event_form.html', {'form': form, 'evtproducts': evtproducts,})
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def Review_page(request, event_id):
    event = Event.objects.get(id=event_id)
    EventItemFormSet = modelformset_factory(EventItem, fields=('chops', 'guest'), extra=0)
    
    if request.method == 'POST':
        formset = EventItemFormSet(request.POST, queryset=EventItem.objects.filter(event=event))
        if formset.is_valid():
            # Custom validation for 'guest' field
            for form in formset:
                guest = form.cleaned_data.get('guest', 0)
                if guest <= 0:
                    messages.error(request, "Guest must be a valid number greater than 0.")
                    return render(request, 'chops/event_review.html', {'event': event, 'formset': formset})

            formset.save()
            return redirect('checkout', event_id=event_id)
    else:
        formset = EventItemFormSet(queryset=EventItem.objects.filter(event=event))

    return render(request, 'chops/event_review.html', {'event': event, 'formset': formset})

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def Event_Checkout(request, event_id):
    event = Event.objects.get(id=event_id)
    event_items = EventItem.objects.filter(event=event)
    total_sum = 0

    for item in event_items:
        item_total = item.guest * item.chops.price
        total_sum += item_total
        item.total = item_total

    
    context= {'event': event, 'event_items': event_items, 'item_total': item_total, 'total_sum': total_sum}
    return render(request, 'chops/event_checkout.html', context)

def generate_transaction_id():
    # Placeholder function to generate a transaction ID
    import uuid
    return str(uuid.uuid4())

def checkout_success(request):
    return render(request, 'events/checkout_success.html')
def checkout_successfull(request):
    return render(request, 'chops/checkout_success.html')

class CustomPasswordResetView(PasswordResetView):
    form_class = PhoneNumberResetForm
    template_name = 'account/password_reset.html'  # Create this template
    success_url = '/password-reset/confirm/'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'account/password_reset_form.html'  # Create this template
    success_url = '/password-reset/done/'   

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def change_password_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')  # Change 'profile' to the desired redirect URL
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change_password_template.html', {'form': form})    

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_category(request, category_id=None):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_category')
    else:
        form = CategoryForm()

    # Retrieve all categories for display
    categories = Category.objects.all()

    if category_id:
        # If category_id is provided, it means the user wants to delete an existing category
        if request.GET.get('delete') == 'true':
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            return redirect('create_category')
        else:
            raise Http404("Invalid request")

    return render(request, 'admin/create_category.html', {'form': form, 'categories': categories})



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def view_comments(request):
    comments = Comment.objects.filter(approved=False)
    return render(request, 'admin/view_comments.html', {'comments': comments})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.approved = True
    comment.save()
    return redirect('view_comments')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('view_comments')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delivery_list(request):
    deliveries = Delivery.objects.all()
    return render(request, 'admin/delivery_list.html', {'deliveries': deliveries})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delivery_create(request):
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('delivery-list')
    else:
        form = DeliveryForm()
    return render(request, 'admin/delivery_form.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delivery_update(request, pk):
    delivery = get_object_or_404(Delivery, pk=pk)
    if request.method == 'POST':
        form = DeliveryForm(request.POST, instance=delivery)
        if form.is_valid():
            form.save()
            return redirect('delivery-list')
    else:
        form = DeliveryForm(instance=delivery)
    return render(request, 'admin/delivery_form.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delivery_delete(request, pk):
    delivery = get_object_or_404(Delivery, pk=pk)
    if request.method == 'POST':
        delivery.delete()
        return redirect('delivery-list')
    return render(request, 'admin/delivery_confirm_delete.html', {'delivery': delivery})