from django.db import models

from goods.models import Products
from users.models import User


class Cart_Queryset(models.QuerySet):


    def total_price(self):
        return sum(cart.product_price() for cart in self)
    

    def total_amount(self):
        if self:
            return sum(cart.amount for cart in self)
        else:
            return 0

# Create your models here.
class Cart(models.Model):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    product = models.ForeignKey(to=Products, on_delete=models.CASCADE, verbose_name='Товар')
    amount = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = "cart"
        verbose_name = "Корзину"
        verbose_name_plural = "Корзины"
    
    objects = Cart_Queryset().as_manager()

    def product_price(self):
        return round(self.product.sell_price() * self.amount, 2)
    
    def __str__(self) -> str:
        return f"Корзина {self.user.username}| Товар {self.product.name}| Количество {self.amount}"