from django.contrib import admin
from .models import Category, Keyword, PromptTemplate

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'popularity')
    list_filter = ('category',)
    search_fields = ('text',)

@admin.register(PromptTemplate)
class PromptTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'template')
