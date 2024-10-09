from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .models import CustomUser, Product, Order
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer, ProductSerializer
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView  # Import TemplateView here

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form}) 

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

# User Dashboard
@login_required
def user_dashboard(request):
    products = Product.objects.all()
    orders = Order.objects.filter(user=request.user)
    context = {
        'products': products,
        'orders': orders
    }
    return render(request, 'user_dashboard.html', context)

# Product List View
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

# Product Detail View
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

# Make Order View
@require_POST
@login_required
def make_order(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))
    product = get_object_or_404(Product, pk=product_id)

    if quantity > product.stock_quantity:
        messages.error(request, "Not enough stock available.")
        return redirect('product_detail', pk=product_id)

    # Create an order
    order = Order.objects.create(user=request.user, product=product, quantity=quantity)
    # Update product stock
    product.stock_quantity -= quantity
    product.save()
    messages.success(request, "Order placed successfully.")
    return redirect('user_dashboard')

def home(request):
    return render(request, 'home.html')

# Product List View for TemplateView
class ProductListView(TemplateView):
    template_name = 'product_list.html'
