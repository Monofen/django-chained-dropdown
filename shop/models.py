from django.db import models
import datetime

class Categories(models.Model):
    search_field = ('name',)
    name = models.CharField(max_length=50, default='', blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_electronics = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

    def get_children(self):
        return Categories.objects.filter(parent=self)

class Customer(models.Model):
    search_field = ('email',)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Product(models.Model):
    search_field = ('name',)
    name = models.CharField(max_length=100)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=6)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name

class ElectronicProduct(models.Model):
    SCREEN_CHOICES = [
        ('LCD', 'LCD'),
        ('LED', 'LED'),
        ('OLED', 'OLED'),
        ('AMOLED', 'AMOLED'),
        
    ]
    RAM_CHOICES = [
        ('2GB', '2GB'),
        ('4GB', '4GB'),
        ('8GB', '8GB'),
        ('16GB', '16GB'),
    
    ]
    product = models.OneToOneField(Product, related_name='electronic_features', on_delete=models.CASCADE)
    screen = models.CharField(max_length=30, choices=SCREEN_CHOICES)
    ram = models.CharField(max_length=15, choices=RAM_CHOICES)

    def __str__(self):
        return f'{self.product.name} Electronics Features'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/product/')

    def __str__(self):
        return f'{self.product.name} Image'

class Order(models.Model):
    search_field = ('phone',)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    date = models.DateField(default=datetime.datetime.today)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.product)
    
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    user_name = models.CharField(max_length=50, default='', blank=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.product.name, self.user_name)
    
