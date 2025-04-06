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
            "Social Media",
            "Digital Marketing",
            "Business & Entrepreneurship",
            "Academic Writing",
            "Creative Writing",
            "Video Production",
            "E-commerce",
            "Personal Development"
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
        
        # Add templates for the new categories
        additional_templates = {
            'digital-marketing': [
                {
                    "name": "Marketing Campaign",
                    "template": "Design a complete digital marketing campaign for {topic}. Include: 1) Target audience definition, 2) Channel strategy, 3) Content plan, 4) Budget allocation, 5) Timeline, and 6) KPIs to measure success. Focus on creating an integrated approach across paid, owned and earned media."
                },
                {
                    "name": "Conversion Funnel",
                    "template": "Create a conversion funnel strategy for {topic}. Detail each stage (awareness, interest, consideration, conversion, retention) with: specific tactics, content types, calls-to-action, and metrics to track. Include suggestions for addressing drop-offs at each stage."
                },
                {
                    "name": "PPC Strategy",
                    "template": "Develop a comprehensive PPC strategy for {topic}. Include: 1) Platform selection with rationale, 2) Keyword strategy and examples, 3) Ad copy templates, 4) Bid strategy, 5) Landing page optimization tips, 6) Budget recommendations, and 7) A/B testing plan for continual improvement."
                }
            ],
            'business-entrepreneurship': [
                {
                    "name": "Business Plan",
                    "template": "Create a comprehensive business plan outline for a {topic} venture. Include: 1) Executive summary framework, 2) Market analysis approach, 3) Organizational structure, 4) Product/service description, 5) Marketing strategy, 6) Financial projections template, and 7) Funding requirements calculation method."
                },
                {
                    "name": "Pitch Deck",
                    "template": "Design a compelling investor pitch deck for a {topic} startup. Include slide outlines for: 1) Problem statement, 2) Solution overview, 3) Market opportunity with TAM/SAM/SOM, 4) Business model, 5) Competitive landscape analysis, 6) Go-to-market strategy, 7) Team highlights, 8) Financial projections, and 9) Investment ask with use of funds."
                },
                {
                    "name": "Revenue Model",
                    "template": "Analyze potential revenue models for a {topic} business. For each model, provide: 1) Structure explanation, 2) Key metrics to track, 3) Pricing strategy suggestions, 4) Unit economics breakdown, 5) Scalability considerations, and 6) Example companies using this model successfully. Recommend the best option based on current market conditions."
                }
            ],
            'academic-writing': [
                {
                    "name": "Research Paper",
                    "template": "Create an outline for a research paper on {topic}. Structure should include: 1) Abstract summary points, 2) Introduction with thesis statement, 3) Literature review approach, 4) Methodology section components, 5) Results presentation format, 6) Discussion points framework, 7) Conclusion elements, and 8) Key references to consider. Focus on academic rigor and scholarly tone."
                },
                {
                    "name": "Literature Review",
                    "template": "Generate a framework for a literature review on {topic}. Include: 1) Historical development of key concepts, 2) Major theoretical frameworks to consider, 3) Critical debates and controversies, 4) Methodological approaches in the research, 5) Gaps in current literature, and 6) Synthesis approach that connects findings across studies."
                },
                {
                    "name": "Thesis Statement",
                    "template": "Develop 3 potential thesis statements for a research paper on {topic}. For each statement: 1) Provide the thesis with a clear position/argument, 2) Explain the theoretical foundation supporting it, 3) Outline key evidence needed to defend it, 4) Identify potential counterarguments, and 5) Suggest methodological approach for investigating it."
                }
            ],
            'creative-writing': [
                {
                    "name": "Story Concept",
                    "template": "Develop a story concept around {topic}. Include: 1) High-concept premise (1-2 sentences), 2) Protagonist details with primary motivation and flaw, 3) Antagonist or main conflict source, 4) Setting description with unique elements, 5) Three major plot points, 6) Thematic question explored, and 7) Potential genres this story could fit within."
                },
                {
                    "name": "Character Profile",
                    "template": "Create a detailed character profile centered around {topic}. Include: 1) Basic demographics and physical description, 2) Psychological traits including fears, desires, and values, 3) Background and formative experiences, 4) Skills and abilities (both strengths and weaknesses), 5) Relationship dynamics with other characters, 6) Character arc potential, and 7) Unique voice examples (dialogue snippets)."
                },
                {
                    "name": "World Building",
                    "template": "Design a fictional world involving {topic}. Detail: 1) Physical environment and geography, 2) Cultural systems including beliefs, traditions, and social structures, 3) Historical timeline with key events, 4) Political/power structures, 5) Economic systems, 6) Technological level and unique innovations, and 7) Magical/supernatural elements or scientific principles (if applicable)."
                }
            ],
            'video-production': [
                {
                    "name": "Video Script",
                    "template": "Create a video script about {topic} for a 5-minute informational video. Include: 1) Hook opening (15 seconds), 2) Introduction with value proposition, 3) 3-5 main content sections with talking points, 4) B-roll and visual suggestions, 5) Graphics/text overlay notes, 6) Call-to-action closing, and 7) Estimated timing for each section. Write in a conversational, engaging tone."
                },
                {
                    "name": "Shot List",
                    "template": "Develop a detailed shot list for a video about {topic}. For each shot include: 1) Shot number, 2) Shot type (wide, medium, close-up, etc.), 3) Camera movement (if any), 4) Subject and action description, 5) Lighting notes, 6) Equipment requirements, 7) Location details, and 8) Estimated setup time. Organize into sequences for efficient shooting."
                },
                {
                    "name": "Video Edit Plan",
                    "template": "Create a post-production plan for a {topic} video. Include: 1) Editing style guide with pacing notes, 2) Color grading mood board description, 3) Sound design elements and music suggestions, 4) Text/graphic treatment style, 5) Key transition types, 6) Special effects requirements, and 7) Approximate edit timeline with milestones. Consider target platform specifications in your recommendations."
                }
            ],
            'e-commerce': [
                {
                    "name": "Product Description",
                    "template": "Write a compelling product description for a {topic} product. Include: 1) Attention-grabbing headline, 2) Emotional hook connecting to customer pain points, 3) 3-5 key features with benefits, 4) Technical specifications in scannable format, 5) Social proof elements, 6) Pricing justification, and 7) Clear call-to-action. Optimize for both conversion and SEO."
                },
                {
                    "name": "Product Launch",
                    "template": "Design a product launch strategy for a {topic} item. Detail: 1) Pre-launch campaign timeline and tactics, 2) Launch day promotional plan, 3) Email sequence structure, 4) Social media announcement strategy, 5) Influencer collaboration approach, 6) Special offers/incentives structure, and 7) Post-launch follow-up plan to maintain momentum."
                },
                {
                    "name": "Store Optimization",
                    "template": "Create an optimization plan for an e-commerce store selling {topic} products. Include recommendations for: 1) Homepage layout and hero section, 2) Navigation structure and categorization, 3) Product page elements and priority order, 4) Cart abandonment reduction tactics, 5) Checkout process streamlining, 6) Cross-sell/upsell implementation, and 7) Mobile optimization priorities."
                }
            ],
            'personal-development': [
                {
                    "name": "Goal Setting Framework",
                    "template": "Develop a comprehensive goal setting framework for {topic}. Include: 1) Self-assessment questions to identify current state, 2) SMART goal template with examples, 3) Goal categorization system (short/medium/long-term), 4) Milestone planning approach, 5) Tracking method and metrics, 6) Accountability system suggestions, and 7) Reflection and adjustment protocols."
                },
                {
                    "name": "Habit Building Plan",
                    "template": "Create a 30-day habit building plan centered on {topic}. Include: 1) Habit definition with clear triggers and rewards, 2) Environment design recommendations, 3) Daily implementation schedule with time blocking, 4) Obstacle identification and mitigation strategies, 5) Progressive difficulty scaling, 6) Tracking system, and 7) Celebration/reward milestones."
                },
                {
                    "name": "Self-Improvement Workshop",
                    "template": "Design a self-improvement workshop outline focused on {topic}. Structure with: 1) Opening activity to establish relevance, 2) Key concept explanations with research backing, 3) Self-assessment exercises, 4) Practical skill-building activities, 5) Group discussion questions, 6) Personal action planning framework, and 7) Follow-up resources and practices for continued growth."
                }
            ]
        }
        
        # Merge the additional templates into the prompt_templates dictionary
        prompt_templates.update(additional_templates)
        
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
            ],
            'digital-marketing': [
                {'text': 'Social media marketing', 'related': 'Facebook ads, Instagram marketing, LinkedIn strategy, social campaigns'},
                {'text': 'Email marketing', 'related': 'Newsletter, email campaigns, drip sequences, email automation, subscriber growth'},
                {'text': 'SEO strategy', 'related': 'Search ranking, organic traffic, SERP optimization, keyword targeting'},
                {'text': 'Content marketing', 'related': 'Blog strategy, content creation, inbound marketing, lead magnets'},
                {'text': 'PPC campaigns', 'related': 'Google Ads, paid search, CPC, SEM, ad copy, display ads'},
                {'text': 'Analytics tools', 'related': 'Google Analytics, data tracking, metrics, conversion tracking, attribution'},
                {'text': 'Marketing automation', 'related': 'Workflow automation, drip campaigns, triggered emails, nurture sequences'},
                {'text': 'Conversion optimization', 'related': 'CRO, A/B testing, landing pages, call-to-action optimization'},
                {'text': 'Lead generation', 'related': 'Lead magnets, opt-ins, lead capture, prospect acquisition'},
                {'text': 'Brand strategy', 'related': 'Brand positioning, brand voice, visual identity, brand guidelines'}
            ],
            'business-entrepreneurship': [
                {'text': 'Startup launch', 'related': 'Business launch, company founding, venture creation, startup journey'},
                {'text': 'Business model', 'related': 'Revenue model, pricing strategy, business structure, business framework'},
                {'text': 'Market research', 'related': 'Customer research, market analysis, competitive analysis, industry trends'},
                {'text': 'Funding strategy', 'related': 'Investor pitch, venture capital, angel investors, fundraising'},
                {'text': 'Growth hacking', 'related': 'Rapid growth, startup scaling, user acquisition, growth strategy'},
                {'text': 'Lean startup', 'related': 'MVP, minimum viable product, lean methodology, product-market fit'},
                {'text': 'Business operations', 'related': 'Operational efficiency, business processes, workflow optimization'},
                {'text': 'Financial planning', 'related': 'Budget forecasting, cash flow management, financial projections'},
                {'text': 'Team building', 'related': 'Hiring strategy, company culture, talent acquisition, leadership'},
                {'text': 'Strategic partnerships', 'related': 'Business alliances, joint ventures, collaboration, networking'}
            ],
            'academic-writing': [
                {'text': 'Research methodology', 'related': 'Research design, methods section, data collection, research approach'},
                {'text': 'Literature review', 'related': 'Academic sources, bibliography, research synthesis, scholarly articles'},
                {'text': 'Thesis writing', 'related': 'Dissertation, academic paper, scholarly writing, research paper'},
                {'text': 'Data analysis', 'related': 'Statistical analysis, qualitative research, quantitative methods, research findings'},
                {'text': 'APA format', 'related': 'Citation style, bibliographic format, academic formatting, references'},
                {'text': 'Academic argument', 'related': 'Scholarly debate, position defense, evidence-based reasoning'},
                {'text': 'Research proposal', 'related': 'Research plan, study design, project proposal, academic proposal'},
                {'text': 'Academic publication', 'related': 'Scholarly journal, peer review, academic publishing, journal submission'},
                {'text': 'Critical analysis', 'related': 'Critical thinking, analytical writing, critique methodology, evaluation'},
                {'text': 'Academic presentation', 'related': 'Conference presentation, research presentation, scholarly talk'}
            ],
            'creative-writing': [
                {'text': 'Character development', 'related': 'Character arc, character design, protagonist, antagonist, character traits'},
                {'text': 'Plot structure', 'related': 'Narrative arc, story structure, plot points, storyline, narrative flow'},
                {'text': 'World building', 'related': 'Fictional world, setting creation, fantasy realm, universe design'},
                {'text': 'Dialogue writing', 'related': 'Character speech, conversation, dialogue tags, speech patterns'},
                {'text': 'Creative narrative', 'related': 'Storytelling, narrative voice, literary fiction, creative prose'},
                {'text': 'Descriptive writing', 'related': 'Sensory details, scene setting, vivid description, show don\'t tell'},
                {'text': 'Genre fiction', 'related': 'Fantasy writing, sci-fi, romance, thriller, mystery, horror'},
                {'text': 'Short story', 'related': 'Flash fiction, short narrative, brief story, compact tale'},
                {'text': 'Poetry composition', 'related': 'Verse, poetic forms, poem structure, lyrical writing'},
                {'text': 'Editing fiction', 'related': 'Manuscript revision, story editing, draft improvement, polishing writing'}
            ],
            'video-production': [
                {'text': 'Video scripting', 'related': 'Script writing, screenplay, video content, shot planning'},
                {'text': 'Cinematography', 'related': 'Camera work, shot composition, visual storytelling, filming techniques'},
                {'text': 'Video editing', 'related': 'Post-production, cuts, transitions, video assembly, editing software'},
                {'text': 'Sound design', 'related': 'Audio editing, soundtrack, sound effects, audio mixing, foley'},
                {'text': 'YouTube content', 'related': 'YouTube videos, YouTube channel, video creation, content strategy'},
                {'text': 'Visual effects', 'related': 'VFX, special effects, motion graphics, CGI, visual enhancements'},
                {'text': 'Color grading', 'related': 'Color correction, color palette, visual tone, color effects'},
                {'text': 'Interview filming', 'related': 'Interview setup, talking head, testimonial video, interview lighting'},
                {'text': 'Social video', 'related': 'TikTok videos, Instagram reels, short-form video, social media content'},
                {'text': 'Documentary style', 'related': 'Documentary filmmaking, non-fiction video, real-life storytelling'}
            ],
            'e-commerce': [
                {'text': 'Product listing', 'related': 'Product catalog, inventory, product pages, e-commerce listings'},
                {'text': 'Online store', 'related': 'E-commerce website, web store, online shop, digital storefront'},
                {'text': 'Conversion rate', 'related': 'Sales conversion, checkout optimization, purchase completion'},
                {'text': 'Product description', 'related': 'Item details, product copy, feature listing, benefit description'},
                {'text': 'E-commerce platform', 'related': 'Shopify, WooCommerce, Magento, online store platform'},
                {'text': 'Shopping cart', 'related': 'Checkout process, cart abandonment, purchase flow, order completion'},
                {'text': 'Product photography', 'related': 'Product images, item photos, visual merchandising, product shots'},
                {'text': 'Customer reviews', 'related': 'Product feedback, testimonials, ratings, social proof'},
                {'text': 'Pricing strategy', 'related': 'Price points, discount structure, pricing model, competitive pricing'},
                {'text': 'Shipping options', 'related': 'Delivery methods, fulfillment, shipping costs, delivery timelines'}
            ],
            'personal-development': [
                {'text': 'Goal setting', 'related': 'Goal achievement, objective planning, target setting, SMART goals'},
                {'text': 'Habit formation', 'related': 'Habit building, behavior change, routine establishment, consistency'},
                {'text': 'Productivity systems', 'related': 'Time management, efficiency techniques, productivity methods, GTD'},
                {'text': 'Mindfulness practice', 'related': 'Meditation, presence, mindful living, awareness training'},
                {'text': 'Self improvement', 'related': 'Personal growth, self development, life improvement, better self'},
                {'text': 'Motivation techniques', 'related': 'Inspiration, drive cultivation, motivational methods, self-motivation'},
                {'text': 'Learning strategies', 'related': 'Skill acquisition, educational approaches, learning methods, study techniques'},
                {'text': 'Emotional intelligence', 'related': 'EQ, emotional awareness, interpersonal skills, emotional management'},
                {'text': 'Work-life balance', 'related': 'Life harmony, balanced living, stress management, burnout prevention'},
                {'text': 'Personal reflection', 'related': 'Self-assessment, journaling, introspection, self-awareness'}
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