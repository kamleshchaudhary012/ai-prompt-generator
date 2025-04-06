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
from django.utils.text import slugify
from django.db import connection, DatabaseError, ProgrammingError, OperationalError
from django.db.migrations.executor import MigrationExecutor
from django.db.migrations.recorder import MigrationRecorder

def home(request):
    try:
        # First try to access the categories
        try:
            categories = Category.objects.all()
            if not categories.exists():
                # Create basic categories
                category_names = ["ChatGPT", "Midjourney", "Blogging / SEO", "Coding", "Social Media"]
                for name in category_names:
                    Category.objects.create(name=name, slug=slugify(name))
                categories = Category.objects.all()
            
            return render(request, 'home.html', {'categories': categories})
        except (OperationalError, ProgrammingError) as db_error:
            # Database tables do not exist - run migrations and create tables manually
            try:
                # Try to manually create the tables
                with connection.cursor() as cursor:
                    # Create Category table
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS generator_category (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        name VARCHAR(100) NOT NULL, 
                        slug VARCHAR(50) NOT NULL UNIQUE
                    )
                    ''')
                    
                    # Create PromptTemplate table
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS generator_prompttemplate (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(200) NOT NULL,
                        template TEXT NOT NULL,
                        category_id INTEGER NOT NULL REFERENCES generator_category(id)
                    )
                    ''')
                    
                    # Create Keyword table
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS generator_keyword (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        text VARCHAR(100) NOT NULL,
                        popularity INTEGER NOT NULL DEFAULT 0,
                        related_keywords TEXT NOT NULL DEFAULT '',
                        category_id INTEGER NOT NULL REFERENCES generator_category(id)
                    )
                    ''')
                    
                    # Insert some basic categories
                    categories_data = [
                        ("ChatGPT", "chatgpt"),
                        ("Midjourney", "midjourney"),
                        ("Blogging / SEO", "blogging-seo"),
                        ("Coding", "coding"),
                        ("Social Media", "social-media")
                    ]
                    
                    for name, slug in categories_data:
                        cursor.execute(
                            "INSERT INTO generator_category (name, slug) VALUES (?, ?)",
                            (name, slug)
                        )
                
                # Now try to render the template with hardcoded categories
                hardcoded_categories = []
                for name, slug in categories_data:
                    hardcoded_categories.append({'name': name, 'slug': slug})
                    
                return render(request, 'home.html', {'categories': hardcoded_categories})
                
            except Exception as inner_error:
                # If all else fails, render a simple template with no database
                error_info = f"Database error: {str(db_error)}\nFailed to create tables: {str(inner_error)}"
                emergency_html = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>AI Prompt Generator</title>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
                </head>
                <body class="bg-gray-100 min-h-screen">
                    <div class="container mx-auto px-4 py-8">
                        <h1 class="text-3xl font-bold text-center mb-8">AI Prompt Generator</h1>
                        <div class="bg-white p-6 rounded-lg shadow-md">
                            <h2 class="text-xl font-semibold mb-4">Welcome!</h2>
                            <p class="mb-4">The application is currently initializing the database. Please try again in a few moments.</p>
                            <div class="flex justify-center">
                                <button onclick="location.reload()" class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                                    Refresh Page
                                </button>
                            </div>
                        </div>
                        {f'<div class="mt-8 p-4 bg-red-100 rounded text-sm"><pre>{error_info}</pre></div>' if request.GET.get('debug') else ''}
                    </div>
                </body>
                </html>
                """
                return HttpResponse(emergency_html)
    except Exception as e:
        error_info = sys.exc_info()
        error_message = f"Error: {str(e)}\n\n{''.join(traceback.format_exception(*error_info))}"
        return HttpResponse(f"<pre>{error_message}</pre>", status=500)

def get_trending_topics(request):
    """API endpoint to get trending topics across all categories or for a specific category"""
    category_slug = request.GET.get('category')
    
    try:
        # Get top keywords by popularity
        try:
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
        except (OperationalError, ProgrammingError):
            # Fallback to hardcoded data if database tables don't exist
            topics = []
            default_categories = {cat['id']: cat for cat in Category.get_default_categories()}
            
            for keyword in Keyword.get_default_keywords():
                category = default_categories.get(keyword['category_id'])
                if category and (not category_slug or category_slug == category['slug']):
                    topics.append({
                        'text': keyword['text'],
                        'category': category['name'],
                        'category_slug': category['slug'],
                        'popularity': keyword['popularity']
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
        try:
            # Regular database approach
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
        except (OperationalError, ProgrammingError):
            # Fallback to hardcoded data
            default_categories = {cat['slug']: cat for cat in Category.get_default_categories()}
            if category_slug not in default_categories:
                return JsonResponse({'error': 'Category not found'}, status=404)
                
            default_keywords = Keyword.get_default_keywords()
            category_id = default_categories[category_slug]['id']
            
            # Filter keywords for this category
            category_keywords = [k for k in default_keywords if k['category_id'] == category_id]
            
            # If query is too short, return all keywords
            if len(query) < 3:
                suggestions = [
                    {'text': k['text'], 'popularity': k['popularity']} 
                    for k in category_keywords
                ]
            else:
                # Simple text matching for suggestions
                matching_keywords = [k for k in category_keywords if query.lower() in k['text'].lower()]
                suggestions = [
                    {'text': k['text'], 'popularity': k['popularity']} 
                    for k in matching_keywords
                ]
                
                # If no suggestions, use the query itself
                if not suggestions:
                    suggestions = [{'text': query.capitalize(), 'popularity': 1}]
        
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
            
            try:
                # Regular database approach
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
            except (OperationalError, ProgrammingError):
                # Fallback to hardcoded data
                default_categories = {cat['slug']: cat for cat in Category.get_default_categories()}
                default_templates = PromptTemplate.get_default_templates()
                
                if category_slug not in default_categories:
                    return JsonResponse({'error': 'Category not found'}, status=404)
                    
                category_id = default_categories[category_slug]['id']
                
                # Filter templates for this category
                category_templates = [t for t in default_templates if t['category_id'] == category_id]
                
                if not category_templates:
                    return JsonResponse({'error': 'No templates found for this category'}, status=404)
                
                # Randomly select 2-3 templates
                count = random.randint(2, 3)
                selected_templates = random.sample(category_templates, min(count, len(category_templates)))
                
                # Generate prompts
                prompts = []
                for template in selected_templates:
                    generated_content = template['template'].replace('{topic}', topic)
                    prompts.append({
                        'id': template['id'],
                        'name': template['name'],
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
