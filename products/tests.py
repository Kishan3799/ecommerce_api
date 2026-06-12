from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Category, Product

class ProductAPITestCase(APITestCase):
    def setUp(self):
        """Run before each test"""
        self.user = User.objects.create_user(
            username = 'testuser',
            password = 'testpass123'
        )
        self.category = Category.objects.create(
            name = 'Eco-Friendly Bamboo Kitchenware',
            slug = 'eco-friendly-bamboo-kitchenware'
        )
        self.product = Product.objects.create(
            category = self.category,
            name = 'Artisan Handwoven Bamboo Serving Tray (Large)',
            slug = 'artisan-handwoven-bamboo-serving-tray-large',
            description = 'A great serving tray',
            price = 50000,
            stock = 10
        )
        
    def test_get_product_list(self):
        """TEst reteriving product list"""
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']),1)
        
    def test_get_product_detail(self):
        """Test retrieving single product"""
        response = self.client.get(f'/api/products/{self.product.slug}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Artisan Handwoven Bamboo Serving Tray (Large)')

    def test_create_product_unauthenticated(self):
        """Test creating product without authentication fails"""
        data = {
            'category_id': self.category.id,
            'name': 'Mouse',
            'slug': 'mouse',
            'description': 'Wireless mouse',
            'price': 500,
            'stock': 20
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_product_authenticated(self):
        """Test creating product with authentication"""
        self.client.force_authenticate(user=self.user)
        data = {
            'category_id': self.category.id,
            'name': 'Mischief 320 GSM Heavyweight Graphic Hoodie',
            'slug': 'mischief-320-gsm-heavyweight-graphic-hoodie',
            'description': 'A great hoodie',
            'price': 500,
            'stock': 20
        }
        response = self.client.post('/api/products/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        
    def test_filter_products_by_category(self):
        """Test filtering products by category"""
        response = self.client.get(f'/api/products/?category={self.category.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
    def test_search_products(self):
        """Test searching products"""
        response = self.client.get('/api/products/?search=Artisan')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
class OrderAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Eco-Friendly Bamboo Kitchenware',
            slug='eco-friendly-bamboo-kitchenware'
        )
        self.product = Product.objects.create(
            category=self.category,
            name='Artisan Handwoven Bamboo Serving Tray (Large)',
            slug='artisan-handwoven-bamboo-serving-tray-large',
            description='A great serving tray',
            price=50000,
            stock=10
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_order(self):
        """Test creating an order"""
        data = {
            'shipping_address': '123 Main St, City',
            'items': [
                {
                    'product_id': self.product.id,
                    'quantity': 2
                }
            ]
        }
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_amount'], '100000.00')
    
    def test_create_order_insufficient_stock(self):
        """Test creating order with insufficient stock"""
        data = {
            'shipping_address': '123 Main St, City',
            'items': [
                {
                    'product_id': self.product.id,
                    'quantity': 20  # More than available stock
                }
            ]
        }
        response = self.client.post('/api/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)