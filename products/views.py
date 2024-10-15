from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from .models import CustomUser, Product, Order
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer, ProductSerializer
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import CustomUserCreationForm



# Custom pagination class
class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# User Views
class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserUpdate(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

class UserDelete(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

# Product Views with search and filtering
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        stock_available = self.request.query_params.get('in_stock', None)
        if stock_available is not None:
            queryset = queryset.filter(stock_quantity__gt=0) if stock_available.lower() == 'true' else queryset
        return queryset

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreate(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductUpdate(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDelete(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# User Signup View
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user automatically after signup
            return redirect('login')  # Redirect to login page after signup
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')

                # Redirect based on user role
                if user.role == 'admin':
                    return redirect('admin-dashboard')
                else:
                    return redirect('user-dashboard')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

# User Dashboard
@login_required
def user_dashboard(request):
    products = Product.objects.all()
    orders = Order.objects.filter(user=request.user)
    context = {
        'products': products,
        'orders': orders
    }
    return render(request, 'user-dashboard.html', context)

# Admin Dashboard
@login_required
def admin_dashboard(request):
    # Logic for the admin dashboard can go here
    return render(request, 'admin-dashboard.html')  # Create this template

# Product List View
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product-list.html', {'products': products})

# Product Detail View
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product-detail.html', {'product': product})

# Make Order View
@require_POST
@login_required
def make_order(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))
    product = get_object_or_404(Product, pk=product_id)

    if quantity > product.stock_quantity:
        messages.error(request, "Not enough stock available.")
        return redirect('product-detail', pk=product_id)

    # Create an order
    order = Order.objects.create(user=request.user, product=product, quantity=quantity)
    # Update product stock
    product.stock_quantity -= quantity
    product.save()
    messages.success(request, "Order placed successfully.")
    return redirect('user-dashboard')

def home(request):
    return render(request, 'home.html')

# Product List View for TemplateView
class ProductListView(TemplateView):
    template_name = 'product-list.html'

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Use the custom form
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log in the user
            return redirect('user-dashboard')  # Redirect after signup
    else:
        form = CustomUserCreationForm()  # Initialize with the custom form
    return render(request, 'signup.html', {'form': form})


# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful!')

                # Redirect based on user role
                if user.role == 'admin':
                    return redirect('admin-dashboard')
                else:
                    return redirect('user-dashboard')  # Change this line
                
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})



