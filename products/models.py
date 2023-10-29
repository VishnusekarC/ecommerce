from django.db import models
from django.utils.text import slugify
from utilities.models import TimestampedModel
from versatileimagefield.fields import PPOIField, VersatileImageField


class Category(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'ec_categories'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Collection(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'ec_collections'
        verbose_name_plural = 'Collections'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Product(TimestampedModel):
    name = models.CharField(max_length=300)
    sku = models.CharField(max_length=20, unique=True)
    image = VersatileImageField('Image',
                                 upload_to='products/images')
    description = models.TextField()
    ppoi = PPOIField('Image PPOI')
    price = models.DecimalField(max_digits=7, decimal_places=2)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category)
    collections = models.ManyToManyField(Collection, blank=True)

    class Meta:
        db_table = 'ec_products'
        verbose_name_plural = 'Products'

    def __str__(self) -> str:
        return self.sku




