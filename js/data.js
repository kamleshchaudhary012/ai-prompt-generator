// Sample prompt templates data
const promptData = {
    chatgpt: {
        templates: [
            {
                id: "cg1",
                name: "Detailed Explanation",
                template: "I need a detailed explanation about {topic}. Include the following aspects: 1) Basic introduction, 2) Historical context, 3) Current applications, 4) Future potential, and 5) Key challenges. Please use simple language and provide real-world examples."
            },
            {
                id: "cg2",
                name: "Step-by-Step Guide",
                template: "Create a comprehensive step-by-step guide on {topic}. For each step, provide: 1) What to do, 2) Why it's important, 3) Common mistakes to avoid, and 4) A tip for success. Make it suitable for beginners."
            },
            {
                id: "cg3",
                name: "Expert Analysis",
                template: "Analyze {topic} from an expert perspective. Consider different viewpoints, latest research, statistical data, and industry standards. Conclude with actionable insights and future predictions."
            },
            {
                id: "cg4",
                name: "Comparison Framework",
                template: "Compare and contrast different approaches to {topic}. Create a structured comparison with categories like effectiveness, cost, time investment, complexity, and outcomes. End with recommendations for different scenarios."
            }
        ]
    },
    midjourney: {
        templates: [
            {
                id: "mj1",
                name: "Photorealistic Scene",
                template: "Photorealistic image of {topic}, golden hour lighting, dramatic shadows, detailed textures, 8k resolution, hyperrealistic, cinematic composition, --ar 16:9 --v 5 --q 2"
            },
            {
                id: "mj2",
                name: "Fantasy Illustration",
                template: "Fantasy illustration of {topic}, magical atmosphere, glowing elements, intricate details, vibrant colors, digital art, concept art style, Greg Rutkowski, Artgerm, --ar 3:4 --v 5 --q 2"
            },
            {
                id: "mj3",
                name: "Isometric Design",
                template: "Isometric design of {topic}, clean lines, colorful palette, miniature style, cute, professional 3D rendering, low poly art, architectural visualization, --ar 1:1 --v 5 --q 2"
            },
            {
                id: "mj4",
                name: "Abstract Art",
                template: "Abstract representation of {topic}, fluid shapes, bold color contrasts, experimental, modern art, digital painting, generative art, Jackson Pollock inspiration, --ar 16:9 --v 5 --stylize 1000"
            }
        ]
    },
    blogging: {
        templates: [
            {
                id: "bl1",
                name: "SEO-Optimized Article",
                template: "Write an SEO-optimized article about {topic} that is 1000 words long. Include: 1) An engaging introduction with statistics, 2) 5 subheadings with H2 tags, 3) Bullet points for key takeaways, 4) A conclusion with a call-to-action, and 5) Meta description of 150 characters. Target audience: beginners seeking practical advice."
            },
            {
                id: "bl2",
                name: "Listicle Post",
                template: "Create a '10 Best {topic}' listicle blog post. For each item include: name, key features, pros and cons, pricing (if applicable), and why it made the list. Add a buyer's guide section at the end with 3 tips for choosing the right option. Optimize for keywords related to '{topic} recommendations'."
            },
            {
                id: "bl3",
                name: "How-To Guide",
                template: "Write a comprehensive how-to guide on {topic} with these sections: 1) Introduction explaining why this skill matters, 2) Materials/tools needed, 3) Step-by-step instructions with images suggestions, 4) Troubleshooting common problems, 5) Advanced tips for experienced users, and 6) FAQs. Include internal linking suggestions."
            },
            {
                id: "bl4",
                name: "Expert Interview",
                template: "Generate a mock expert interview about {topic} with 10 insightful questions and detailed answers. Structure it with an introduction to the expert (you can invent a suitable persona), the main interview content, and a conclusion with key insights. Include pull quotes that would work well for social media sharing."
            }
        ]
    },
    coding: {
        templates: [
            {
                id: "cd1",
                name: "Project Structure",
                template: "Help me plan a software project for {topic}. Include: 1) Recommended tech stack with reasoning, 2) Folder structure and architecture pattern, 3) Key features for MVP, 4) Potential challenges and solutions, 5) Testing strategy, and 6) Deployment considerations. I'm an intermediate developer focused on creating a maintainable codebase."
            },
            {
                id: "cd2",
                name: "Algorithm Implementation",
                template: "Explain and implement an efficient algorithm for {topic}. Please: 1) Describe the problem clearly, 2) Explain the algorithm's approach and time/space complexity, 3) Provide pseudocode, 4) Implement the solution in Python or JavaScript (preferred), 5) Add comprehensive comments, and 6) Include test cases covering edge scenarios."
            },
            {
                id: "cd3",
                name: "Code Refactoring",
                template: "I need to refactor code related to {topic}. Please provide guidance on: 1) Common code smells to look for, 2) Refactoring techniques specific to this domain, 3) Design patterns that might improve the architecture, 4) Performance optimization strategies, and 5) Best practices for maintaining code quality after refactoring."
            },
            {
                id: "cd4",
                name: "API Design",
                template: "Design a RESTful API for {topic}. Include: 1) Resource modeling and endpoints, 2) Request/response examples in JSON, 3) Authentication and authorization strategy, 4) Error handling approach, 5) Pagination and filtering options, 6) API versioning strategy, and 7) Documentation structure. Focus on creating a developer-friendly and scalable API."
            }
        ]
    },
    social: {
        templates: [
            {
                id: "sm1",
                name: "Content Calendar",
                template: "Create a 2-week content calendar for {topic} across Instagram, Twitter, and LinkedIn. For each platform, provide: 1) 3 post ideas per week with optimal posting times, 2) Hashtag suggestions (5-10 per post), 3) Caption templates that encourage engagement, 4) Content themes to maintain consistency, and 5) Ideas for Stories/ephemeral content. Target audience: [describe your audience]."
            },
            {
                id: "sm2",
                name: "Viral Post Formula",
                template: "Design 5 potentially viral social media posts about {topic}. For each post: 1) Platform it's optimized for, 2) Hook/opening line that grabs attention, 3) Content structure and format (carousel, video script, etc.), 4) Call-to-action to maximize engagement, 5) Psychological trigger it leverages (curiosity, controversy, etc.). Include tips for riding trending topics related to {topic}."
            },
            {
                id: "sm3",
                name: "Engagement Strategy",
                template: "Develop an engagement strategy for a {topic} focused social media account. Include: 1) Community building tactics, 2) 10 conversation starters/questions to ask followers, 3) Response templates for common scenarios (praise, complaints, questions), 4) User-generated content campaign ideas, 5) Engagement metrics to track, and 6) Competitor analysis framework to identify engagement opportunities."
            },
            {
                id: "sm4",
                name: "Influencer Campaign",
                template: "Plan an influencer marketing campaign for {topic}. Outline: 1) Criteria for selecting appropriate influencers, 2) Outreach message template, 3) Campaign brief structure, 4) Collaboration ideas beyond standard sponsored posts, 5) Tracking KPIs and ROI, 6) Compliance and disclosure requirements, and 7) Strategy for repurposing influencer-generated content across channels."
            }
        ]
    }
};

// Function to replace template placeholders with actual topic
function generatePrompt(template, topic) {
    return template.replace(/{topic}/g, topic);
} 