from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def get_default_categories(cls):
        return [
            {"id": 1, "name": "ChatGPT", "slug": "chatgpt"},
            {"id": 2, "name": "Midjourney", "slug": "midjourney"},
            {"id": 3, "name": "Blogging / SEO", "slug": "blogging-seo"},
            {"id": 4, "name": "Coding", "slug": "coding"},
            {"id": 5, "name": "Social Media", "slug": "social-media"}
        ]
    
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
    
    @classmethod
    def get_default_keywords(cls):
        return [
            {"id": 1, "text": "AI assistant", "category_id": 1, "popularity": 10},
            {"id": 2, "text": "Digital art", "category_id": 2, "popularity": 10},
            {"id": 3, "text": "Content marketing", "category_id": 3, "popularity": 10},
            {"id": 4, "text": "Python", "category_id": 4, "popularity": 10},
            {"id": 5, "text": "Instagram", "category_id": 5, "popularity": 10}
        ]

class PromptTemplate(models.Model):
    name = models.CharField(max_length=200)
    template = models.TextField()
    category = models.ForeignKey(Category, related_name='templates', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    @classmethod
    def get_default_templates(cls):
        return [
            {
                "id": 1, 
                "name": "Basic Template", 
                "template": "Write about {topic} in detail.",
                "category_id": 1
            },
            {
                "id": 2, 
                "name": "Art Creation", 
                "template": "Create an image of {topic} with vibrant colors.",
                "category_id": 2
            },
            {
                "id": 3, 
                "name": "Blog Post", 
                "template": "Write a blog post about {topic} with SEO optimization.",
                "category_id": 3
            },
            {
                "id": 4, 
                "name": "Code Example", 
                "template": "Write a code example for {topic}.",
                "category_id": 4
            },
            {
                "id": 5, 
                "name": "Social Post", 
                "template": "Create an engaging social media post about {topic}.",
                "category_id": 5
            }
        ]
