from django.contrib.gis.db import models

from occurrences.choices import STATUS_CHOICES


class Category(models.Model):
    type = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.type


class Occurrence(models.Model):

    description = models.CharField(max_length=250, default='')
    geo_location = models.PointField()
    author = models.ForeignKey('auth.User', related_name='occurrences', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default='waiting_validation', max_length=50)
    category = models.ForeignKey(Category, verbose_name='Category', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']
        verbose_name = 'Occurrence'
        verbose_name_plural = 'Occurrences'

    def __str__(self):
        return self.description



