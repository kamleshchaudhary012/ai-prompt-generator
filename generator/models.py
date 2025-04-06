from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Keyword(models.Model):
    text = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='keywords', on_delete=models.CASCADE)
    popularity = models.IntegerField(default=0)
    related_keywords = models.TextField(blank=True, help_text="Comma-separated related keywords or synonyms")
    
    def __str__(self):
        return self.text
    
    def get_related_keywords_list(self):
        """Return the related keywords as a list"""
        if not self.related_keywords:
            return []
        return [kw.strip() for kw in self.related_keywords.split(',')]

class PromptTemplate(models.Model):
    name = models.CharField(max_length=200)
    template = models.TextField()
    category = models.ForeignKey(Category, related_name='templates', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
