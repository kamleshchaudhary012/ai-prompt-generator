from django.core.management.base import BaseCommand
from generator.models import Category, PromptTemplate, Keyword
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Loads initial categories and prompt templates'

    def handle(self, *args, **kwargs):
        self.stdout.write('Loading initial data...')
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Category.objects.all().delete()
        
        # Create categories
        categories_data = [
            "ChatGPT",
            "Midjourney",
            "Blogging / SEO",
            "Coding",
            "Social Media"
        ]
        
        categories = {}
        for category_name in categories_data:
            slug = slugify(category_name)
            category = Category.objects.create(name=category_name, slug=slug)
            categories[slug] = category
            self.stdout.write(f'Created category: {category_name}')
        
        # Create templates for each category
        prompt_templates = {
            'chatgpt': [
                {
                    "name": "Detailed Explanation",
                    "template": "I need a detailed explanation about {topic}. Include the following aspects: 1) Basic introduction, 2) Historical context, 3) Current applications, 4) Future potential, and 5) Key challenges. Please use simple language and provide real-world examples."
                },
                {
                    "name": "Step-by-Step Guide",
                    "template": "Create a comprehensive step-by-step guide on {topic}. For each step, provide: 1) What to do, 2) Why it's important, 3) Common mistakes to avoid, and 4) A tip for success. Make it suitable for beginners."
                },
                {
                    "name": "Expert Analysis",
                    "template": "Analyze {topic} from an expert perspective. Consider different viewpoints, latest research, statistical data, and industry standards. Conclude with actionable insights and future predictions."
                },
                {
                    "name": "Comparison Framework",
                    "template": "Compare and contrast different approaches to {topic}. Create a structured comparison with categories like effectiveness, cost, time investment, complexity, and outcomes. End with recommendations for different scenarios."
                }
            ],
            'midjourney': [
                {
                    "name": "Photorealistic Scene",
                    "template": "Photorealistic image of {topic}, golden hour lighting, dramatic shadows, detailed textures, 8k resolution, hyperrealistic, cinematic composition, --ar 16:9 --v 5 --q 2"
                },
                {
                    "name": "Fantasy Illustration",
                    "template": "Fantasy illustration of {topic}, magical atmosphere, glowing elements, intricate details, vibrant colors, digital art, concept art style, Greg Rutkowski, Artgerm, --ar 3:4 --v 5 --q 2"
                },
                {
                    "name": "Isometric Design",
                    "template": "Isometric design of {topic}, clean lines, colorful palette, miniature style, cute, professional 3D rendering, low poly art, architectural visualization, --ar 1:1 --v 5 --q 2"
                },
                {
                    "name": "Abstract Art",
                    "template": "Abstract representation of {topic}, fluid shapes, bold color contrasts, experimental, modern art, digital painting, generative art, Jackson Pollock inspiration, --ar 16:9 --v 5 --stylize 1000"
                }
            ],
            'blogging-seo': [
                {
                    "name": "SEO-Optimized Article",
                    "template": "Write an SEO-optimized article about {topic} that is 1000 words long. Include: 1) An engaging introduction with statistics, 2) 5 subheadings with H2 tags, 3) Bullet points for key takeaways, 4) A conclusion with a call-to-action, and 5) Meta description of 150 characters. Target audience: beginners seeking practical advice."
                },
                {
                    "name": "Listicle Post",
                    "template": "Create a '10 Best {topic}' listicle blog post. For each item include: name, key features, pros and cons, pricing (if applicable), and why it made the list. Add a buyer's guide section at the end with 3 tips for choosing the right option. Optimize for keywords related to '{topic} recommendations'."
                },
                {
                    "name": "How-To Guide",
                    "template": "Write a comprehensive how-to guide on {topic} with these sections: 1) Introduction explaining why this skill matters, 2) Materials/tools needed, 3) Step-by-step instructions with images suggestions, 4) Troubleshooting common problems, 5) Advanced tips for experienced users, and 6) FAQs. Include internal linking suggestions."
                },
                {
                    "name": "Expert Interview",
                    "template": "Generate a mock expert interview about {topic} with 10 insightful questions and detailed answers. Structure it with an introduction to the expert (you can invent a suitable persona), the main interview content, and a conclusion with key insights. Include pull quotes that would work well for social media sharing."
                }
            ],
            'coding': [
                {
                    "name": "Project Structure",
                    "template": "Help me plan a software project for {topic}. Include: 1) Recommended tech stack with reasoning, 2) Folder structure and architecture pattern, 3) Key features for MVP, 4) Potential challenges and solutions, 5) Testing strategy, and 6) Deployment considerations. I'm an intermediate developer focused on creating a maintainable codebase."
                },
                {
                    "name": "Algorithm Implementation",
                    "template": "Explain and implement an efficient algorithm for {topic}. Please: 1) Describe the problem clearly, 2) Explain the algorithm's approach and time/space complexity, 3) Provide pseudocode, 4) Implement the solution in Python or JavaScript (preferred), 5) Add comprehensive comments, and 6) Include test cases covering edge scenarios."
                },
                {
                    "name": "Code Refactoring",
                    "template": "I need to refactor code related to {topic}. Please provide guidance on: 1) Common code smells to look for, 2) Refactoring techniques specific to this domain, 3) Design patterns that might improve the architecture, 4) Performance optimization strategies, and 5) Best practices for maintaining code quality after refactoring."
                },
                {
                    "name": "API Design",
                    "template": "Design a RESTful API for {topic}. Include: 1) Resource modeling and endpoints, 2) Request/response examples in JSON, 3) Authentication and authorization strategy, 4) Error handling approach, 5) Pagination and filtering options, 6) API versioning strategy, and 7) Documentation structure. Focus on creating a developer-friendly and scalable API."
                }
            ],
            'social-media': [
                {
                    "name": "Content Calendar",
                    "template": "Create a 2-week content calendar for {topic} across Instagram, Twitter, and LinkedIn. For each platform, provide: 1) 3 post ideas per week with optimal posting times, 2) Hashtag suggestions (5-10 per post), 3) Caption templates that encourage engagement, 4) Content themes to maintain consistency, and 5) Ideas for Stories/ephemeral content. Target audience: [describe your audience]."
                },
                {
                    "name": "Viral Post Formula",
                    "template": "Design 5 potentially viral social media posts about {topic}. For each post: 1) Platform it's optimized for, 2) Hook/opening line that grabs attention, 3) Content structure and format (carousel, video script, etc.), 4) Call-to-action to maximize engagement, 5) Psychological trigger it leverages (curiosity, controversy, etc.). Include tips for riding trending topics related to {topic}."
                },
                {
                    "name": "Engagement Strategy",
                    "template": "Develop an engagement strategy for a {topic} focused social media account. Include: 1) Community building tactics, 2) 10 conversation starters/questions to ask followers, 3) Response templates for common scenarios (praise, complaints, questions), 4) User-generated content campaign ideas, 5) Engagement metrics to track, and 6) Competitor analysis framework to identify engagement opportunities."
                },
                {
                    "name": "Influencer Campaign",
                    "template": "Plan an influencer marketing campaign for {topic}. Outline: 1) Criteria for selecting appropriate influencers, 2) Outreach message template, 3) Campaign brief structure, 4) Collaboration ideas beyond standard sponsored posts, 5) Tracking KPIs and ROI, 6) Compliance and disclosure requirements, and 7) Strategy for repurposing influencer-generated content across channels."
                }
            ]
        }
        
        # Map dictionary to normalize slug names
        slug_mapping = {
            'blogging-seo': 'blogging-seo',
            'social-media': 'social-media',
        }
        
        template_count = 0
        for template_category, templates in prompt_templates.items():
            # Get the correct category slug mapping
            if template_category in slug_mapping:
                category_slug = slug_mapping[template_category]
            else:
                category_slug = template_category
                
            # Find the category in our categories
            category = None
            for cat_slug, cat in categories.items():
                if template_category in cat_slug or cat_slug in template_category:
                    category = cat
                    break
                    
            if not category:
                self.stdout.write(self.style.WARNING(f'Category not found for slug: {template_category}'))
                continue
                
            for template_data in templates:
                PromptTemplate.objects.create(
                    name=template_data['name'],
                    template=template_data['template'],
                    category=category
                )
                template_count += 1
        
        self.stdout.write(f'Created {template_count} prompt templates')
        
        # Add expanded keywords with related terms for each category
        keywords_data = {
            'chatgpt': [
                {'text': 'AI assistant', 'related': 'virtual assistant, chatbot, digital helper, AI chat, language model'},
                {'text': 'natural language', 'related': 'NLP, language processing, text analysis, linguistics, conversation'},
                {'text': 'GPT-4', 'related': 'GPT-3, large language model, OpenAI, AI model, transformer'},
                {'text': 'machine learning', 'related': 'AI, deep learning, neural networks, algorithms, data science'},
                {'text': 'conversational AI', 'related': 'dialogue systems, chat interface, interactive AI, voice assistant'},
                {'text': 'prompt engineering', 'related': 'AI prompts, input design, instruction crafting, query formation'},
                {'text': 'AI writing', 'related': 'content generation, automated writing, text creation, AI author'},
                {'text': 'creative writing', 'related': 'storytelling, fiction, narrative, creative content, imaginative text'},
                {'text': 'fact checking', 'related': 'information verification, accuracy, truth assessment, validation'},
                {'text': 'AI ethics', 'related': 'responsible AI, AI safety, fairness, bias, transparency'}
            ],
            'midjourney': [
                {'text': 'digital art', 'related': 'digital illustration, computer art, digital painting, digital design'},
                {'text': 'generative AI', 'related': 'AI art, image generation, AI-created images, machine-made art'},
                {'text': 'illustration', 'related': 'drawing, artwork, visual representation, graphic design, picture'},
                {'text': '3D rendering', 'related': 'CGI, 3D graphics, 3D visualization, 3D modeling, three-dimensional'},
                {'text': 'fantasy art', 'related': 'magical scenes, fantastical imagery, mythical art, imaginative art'},
                {'text': 'portrait style', 'related': 'character design, face rendering, human figure, person illustration'},
                {'text': 'landscape scene', 'related': 'scenery, vista, environment art, natural setting, outdoor scene'},
                {'text': 'concept art', 'related': 'visual development, pre-production art, design concept, idea visualization'},
                {'text': 'photorealistic', 'related': 'hyperrealistic, lifelike, true-to-life, realistic rendering'},
                {'text': 'abstract design', 'related': 'non-representational, geometric, expressionist, non-figurative art'}
            ],
            'blogging-seo': [
                {'text': 'content marketing', 'related': 'content strategy, inbound marketing, digital marketing, content creation'},
                {'text': 'keyword research', 'related': 'SEO keywords, search terms, keyword analysis, query research'},
                {'text': 'blog optimization', 'related': 'blog SEO, content optimization, blogging strategy, website optimization'},
                {'text': 'article writing', 'related': 'blog post creation, content writing, web articles, written content'},
                {'text': 'SEO tactics', 'related': 'search engine optimization, SEO techniques, ranking strategies, SERP improvement'},
                {'text': 'backlink strategy', 'related': 'link building, external links, inbound links, link profile'},
                {'text': 'audience engagement', 'related': 'reader interaction, user engagement, audience retention, engagement metrics'},
                {'text': 'content calendar', 'related': 'editorial calendar, publishing schedule, content planning, post timeline'},
                {'text': 'conversion optimization', 'related': 'CRO, conversion rate, user conversion, action optimization'},
                {'text': 'meta descriptions', 'related': 'meta tags, SERP snippet, search preview, page description'}
            ],
            'coding': [
                {'text': 'Python', 'related': 'Python programming, python code, python syntax, python development, python script'},
                {'text': 'JavaScript', 'related': 'JS, ECMAScript, frontend code, web scripting, JS development'},
                {'text': 'web development', 'related': 'web design, website creation, web programming, web apps, frontend'},
                {'text': 'algorithms', 'related': 'data structures, computational procedures, coding algorithms, problem-solving approaches'},
                {'text': 'data structures', 'related': 'arrays, linked lists, trees, hash tables, computational structures'},
                {'text': 'API development', 'related': 'API design, endpoints, REST API, API integration, web services'},
                {'text': 'testing frameworks', 'related': 'unit testing, test automation, QA tools, test suites, code testing'},
                {'text': 'version control', 'related': 'git, GitHub, code repository, commit history, branches'},
                {'text': 'database design', 'related': 'SQL, NoSQL, data modeling, schema design, relational databases'},
                {'text': 'mobile development', 'related': 'app creation, iOS, Android, mobile apps, smartphone applications'}
            ],
            'social-media': [
                {'text': 'Instagram', 'related': 'IG, Insta, Instagram marketing, Instagram content, Instagram strategy'},
                {'text': 'TikTok', 'related': 'TikTok videos, short-form content, TikTok trends, TikTok marketing'},
                {'text': 'content strategy', 'related': 'content planning, social strategy, content marketing, posting strategy'},
                {'text': 'engagement', 'related': 'likes, comments, shares, follower interaction, audience engagement'},
                {'text': 'audience growth', 'related': 'follower growth, increasing followers, expanding reach, growing audience'},
                {'text': 'hashtag strategy', 'related': 'hashtag research, trending hashtags, hashtag optimization, tag selection'},
                {'text': 'social media bio', 'related': 'profile description, account bio, self-introduction, profile text, about me section'},
                {'text': 'content creation', 'related': 'post creation, social media content, original posts, media creation'},
                {'text': 'reels creation', 'related': 'short videos, Instagram reels, video content, short-form video'},
                {'text': 'social analytics', 'related': 'metrics tracking, performance analysis, engagement stats, reach metrics'}
            ]
        }
        
        keyword_count = 0
        for keyword_category, keywords in keywords_data.items():
            # Find the category in our categories
            category = None
            for cat_slug, cat in categories.items():
                if keyword_category in cat_slug or cat_slug in keyword_category:
                    category = cat
                    break
                    
            if not category:
                self.stdout.write(self.style.WARNING(f'Category not found for slug: {keyword_category}'))
                continue
                
            for i, keyword_data in enumerate(keywords):
                # Give some keywords higher popularity
                popularity = 10 - i if i < 5 else 5
                
                Keyword.objects.create(
                    text=keyword_data['text'],
                    category=category,
                    popularity=popularity,
                    related_keywords=keyword_data['related']
                )
                keyword_count += 1
        
        self.stdout.write(f'Created {keyword_count} initial keywords')
        
        # Add some additional common search terms
        additional_terms = [
            {'category': 'social-media', 'text': 'create best bio for Instagram', 'related': 'Instagram bio, profile bio, good bio, attractive bio, bio examples', 'popularity': 8},
            {'category': 'social-media', 'text': 'create best bio for Twitter', 'related': 'Twitter bio, profile bio, good bio, attractive bio, bio examples', 'popularity': 7},
            {'category': 'social-media', 'text': 'how to add best bio for men', 'related': 'male bio, men profile, dating bio, attractive bio for guys', 'popularity': 9},
            {'category': 'coding', 'text': 'create a simple python code', 'related': 'basic python, python beginner, hello world, simple script, python example', 'popularity': 8},
            {'category': 'coding', 'text': 'create a simple JavaScript function', 'related': 'JS function, basic JavaScript, beginner JS, function example', 'popularity': 6},
            {'category': 'chatgpt', 'text': 'kamlesh name related', 'related': 'name meaning, name origin, name information, personal name', 'popularity': 5},
            {'category': 'chatgpt', 'text': 'write a poem about', 'related': 'poetry, creative writing, verses, rhymes, sonnet', 'popularity': 9},
        ]
        
        add_count = 0
        for term in additional_terms:
            try:
                category = Category.objects.get(slug__icontains=term['category'])
                Keyword.objects.create(
                    text=term['text'],
                    category=category,
                    popularity=term['popularity'],
                    related_keywords=term['related']
                )
                add_count += 1
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Category not found for: {term['category']}"))
        
        self.stdout.write(f'Added {add_count} common search terms')
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data')) 