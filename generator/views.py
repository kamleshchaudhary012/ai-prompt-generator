from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Category, Keyword, PromptTemplate
from django.db.models import Q, F, Value, FloatField
from django.db.models.functions import Length, Greatest
from functools import reduce
import random
import json
import re
import traceback
import sys

def home(request):
    try:
        categories = Category.objects.all()
        return render(request, 'home.html', {'categories': categories})
    except Exception as e:
        error_info = sys.exc_info()
        error_message = f"Error: {str(e)}\n\n{''.join(traceback.format_exception(*error_info))}"
        return HttpResponse(f"<pre>{error_message}</pre>", status=500)

def get_trending_topics(request):
    """API endpoint to get trending topics across all categories or for a specific category"""
    category_slug = request.GET.get('category')
    
    try:
        # Get top keywords by popularity
        if category_slug:
            # For a specific category
            category = Category.objects.get(slug=category_slug)
            trending = Keyword.objects.filter(category=category).order_by('-popularity')[:8]
        else:
            # Across all categories
            trending = Keyword.objects.order_by('-popularity')[:12]
            
        # Format the response
        topics = []
        for keyword in trending:
            topics.append({
                'text': keyword.text,
                'category': keyword.category.name,
                'category_slug': keyword.category.slug,
                'popularity': keyword.popularity
            })
            
        return JsonResponse({'topics': topics})
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_keywords_by_category(request):
    """API endpoint to get keywords suggestions based on selected category and optional query"""
    category_slug = request.GET.get('category')
    query = request.GET.get('query', '').strip().lower()
    
    if not category_slug:
        return JsonResponse({'error': 'Category is required'}, status=400)
    
    try:
        category = Category.objects.get(slug=category_slug)
        
        # If query is empty or too short, return most popular keywords
        if len(query) < 3:
            suggestions = [
                {'text': keyword.text, 'popularity': keyword.popularity} 
                for keyword in Keyword.objects.filter(category=category).order_by('-popularity')[:10]
            ]
            return JsonResponse({'suggestions': suggestions})
        
        # Start with direct matches on keyword text or related keywords
        exact_keywords = Keyword.objects.filter(
            category=category,
            text__icontains=query
        ).order_by('-popularity')
        
        # Find keywords that contain query in their related_keywords
        related_matches = []
        for keyword in Keyword.objects.filter(category=category):
            if any(query in related.lower() for related in keyword.get_related_keywords_list()):
                related_matches.append(keyword)
        
        # Find keywords with partial word matches (e.g., "python code" should match "code")
        words = re.findall(r'\w+', query)
        partial_matches = Keyword.objects.filter(
            category=category
        ).exclude(
            id__in=[k.id for k in exact_keywords]
        ).exclude(
            id__in=[k.id for k in related_matches]
        ).filter(
            reduce(lambda x, y: x | y, [Q(text__icontains=word) for word in words])
        ).order_by('-popularity')
        
        # Combine and limit results
        all_keywords = list(exact_keywords) + related_matches + list(partial_matches)
        unique_keywords = []
        seen_ids = set()
        
        for keyword in all_keywords:
            if keyword.id not in seen_ids:
                seen_ids.add(keyword.id)
                unique_keywords.append(keyword)
        
        suggestions = [
            {'text': keyword.text, 'popularity': keyword.popularity} 
            for keyword in unique_keywords[:10]
        ]
        
        # If we still don't have enough suggestions, create one from the query
        if not suggestions and query:
            # Create suggestion from query and store for future
            new_keyword, created = Keyword.objects.get_or_create(
                text=query.capitalize(),
                category=category,
                defaults={'popularity': 1}
            )
            if not created:
                new_keyword.popularity += 1
                new_keyword.save()
                
            suggestions = [{'text': new_keyword.text, 'popularity': new_keyword.popularity}]
        
        return JsonResponse({'suggestions': suggestions})
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Category not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_prompts(request):
    """API endpoint to generate prompts based on topic and category"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            topic = data.get('topic')
            category_slug = data.get('category')
            
            if not topic or not category_slug:
                return JsonResponse({'error': 'Both topic and category are required'}, status=400)
            
            category = Category.objects.get(slug=category_slug)
            
            # Increment keyword popularity or create new keyword
            keyword, created = Keyword.objects.get_or_create(
                text=topic,
                category=category,
                defaults={'popularity': 1}
            )
            
            if not created:
                keyword.popularity += 1
                keyword.save()
            
            # Get templates for this category
            templates = PromptTemplate.objects.filter(category=category)
            
            if not templates.exists():
                return JsonResponse({'error': 'No templates found for this category'}, status=404)
            
            # Randomly select 2-3 templates
            count = random.randint(2, 3)
            selected_templates = random.sample(list(templates), min(count, templates.count()))
            
            # Generate prompts
            prompts = []
            for template in selected_templates:
                generated_content = template.template.replace('{topic}', topic)
                prompts.append({
                    'id': template.id,
                    'name': template.name,
                    'generatedContent': generated_content
                })
            
            return JsonResponse({'prompts': prompts})
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
