// DOM Elements
document.addEventListener('DOMContentLoaded', () => {
    // Main elements
    const topicInput = document.getElementById('topic');
    const generateBtn = document.getElementById('generate-btn');
    const resultsSection = document.getElementById('results-section');
    const promptsContainer = document.getElementById('prompts-container');
    const refreshBtn = document.getElementById('refresh-btn');
    const categoryBtns = document.querySelectorAll('.category-btn');

    // Mobile menu
    const mobileMenuBtn = document.querySelector('.md\\:hidden button');
    const mobileMenu = document.createElement('div');
    mobileMenu.className = 'mobile-menu absolute w-full left-0 bg-white shadow-md py-4 px-6 mt-4 rounded-md z-50';
    mobileMenu.innerHTML = `
        <ul class="space-y-3">
            <li><a href="#" class="block text-gray-700 hover:text-indigo-600 transition">Home</a></li>
            <li><a href="#" class="block text-gray-700 hover:text-indigo-600 transition">Examples</a></li>
            <li><a href="#" class="block text-gray-700 hover:text-indigo-600 transition">About</a></li>
        </ul>
    `;
    mobileMenu.style.display = 'none';
    
    document.querySelector('header nav').appendChild(mobileMenu);

    mobileMenuBtn.addEventListener('click', () => {
        if (mobileMenu.style.display === 'none') {
            mobileMenu.style.display = 'block';
            setTimeout(() => mobileMenu.classList.add('open'), 10);
        } else {
            mobileMenu.classList.remove('open');
            setTimeout(() => mobileMenu.style.display = 'none', 300);
        }
    });

    // Current state
    let selectedCategory = 'chatgpt';
    let generatedPrompts = [];
    let lastTopic = '';

    // Initialize category buttons
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Update selected category
            selectedCategory = btn.dataset.category;
            
            // Update UI
            categoryBtns.forEach(b => {
                if (b.dataset.category === selectedCategory) {
                    b.classList.remove('bg-gray-200', 'text-gray-800');
                    b.classList.add('bg-indigo-600', 'text-white');
                } else {
                    b.classList.remove('bg-indigo-600', 'text-white');
                    b.classList.add('bg-gray-200', 'text-gray-800');
                }
            });
        });
    });

    // Generate prompts function
    function generatePrompts(topic) {
        if (!topic.trim()) {
            showError('Please enter a topic');
            return;
        }

        // Save the topic
        lastTopic = topic;

        // Show loading state
        generateBtn.textContent = 'Generating';
        generateBtn.classList.add('loading');
        generateBtn.disabled = true;

        // Simulate API call with timeout
        setTimeout(() => {
            // Get templates for selected category
            const templates = promptData[selectedCategory].templates;
            
            // Select random prompts (2-3)
            const numberOfPrompts = Math.random() > 0.5 ? 3 : 2;
            const shuffled = [...templates].sort(() => 0.5 - Math.random());
            generatedPrompts = shuffled.slice(0, numberOfPrompts).map(template => {
                return {
                    ...template,
                    generatedContent: generatePrompt(template.template, topic)
                };
            });

            // Display prompts
            displayPrompts();

            // Reset generate button
            generateBtn.textContent = 'Generate Prompts';
            generateBtn.classList.remove('loading');
            generateBtn.disabled = false;

            // Show results section
            resultsSection.classList.remove('hidden');
            
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }, 1500);
    }

    // Display prompts in UI
    function displayPrompts() {
        // Clear previous prompts
        promptsContainer.innerHTML = '';

        // Add each prompt with animation delay
        generatedPrompts.forEach((prompt, index) => {
            const promptCard = document.createElement('div');
            promptCard.className = 'prompt-card bg-white rounded-xl shadow-md overflow-hidden fade-in';
            promptCard.style.animationDelay = `${index * 150}ms`;

            promptCard.innerHTML = `
                <div class="p-6">
                    <div class="flex justify-between items-start mb-4">
                        <h4 class="text-lg font-semibold text-gray-800">${prompt.name}</h4>
                        <span class="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm font-medium">
                            ${capitalizeFirstLetter(selectedCategory)}
                        </span>
                    </div>
                    <div class="bg-gray-50 rounded-lg p-4 mb-4">
                        <p class="text-gray-700 whitespace-pre-line">${prompt.generatedContent}</p>
                    </div>
                    <button class="copy-btn flex items-center gap-2 text-indigo-600 hover:text-indigo-800 font-medium transition" data-prompt="${encodeURIComponent(prompt.generatedContent)}">
                        <i class="far fa-copy"></i> Copy to clipboard
                    </button>
                </div>
            `;

            promptsContainer.appendChild(promptCard);
        });

        // Add event listeners to copy buttons
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', copyToClipboard);
        });
    }

    // Copy to clipboard function
    function copyToClipboard(e) {
        const promptText = decodeURIComponent(e.currentTarget.dataset.prompt);
        
        // Copy to clipboard
        navigator.clipboard.writeText(promptText).then(() => {
            // Show copied state temporarily
            const originalText = e.currentTarget.innerHTML;
            e.currentTarget.innerHTML = '<i class="fas fa-check"></i> Copied!';
            
            setTimeout(() => {
                e.currentTarget.innerHTML = originalText;
            }, 2000);
        });
    }

    // Show error message
    function showError(message) {
        // Create error element if it doesn't exist
        let errorElement = document.getElementById('error-message');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.id = 'error-message';
            errorElement.className = 'bg-red-100 text-red-700 px-4 py-3 rounded-lg mb-4 fade-in';
            const form = document.querySelector('.max-w-4xl.mx-auto.bg-white');
            form.insertBefore(errorElement, form.firstChild);
        }
        
        errorElement.textContent = message;
        
        // Remove error after 3 seconds
        setTimeout(() => {
            errorElement.remove();
        }, 3000);
    }

    // Capitalize first letter helper
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    // Event listeners
    generateBtn.addEventListener('click', () => {
        generatePrompts(topicInput.value);
    });

    // Allow pressing Enter to generate
    topicInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            generatePrompts(topicInput.value);
        }
    });

    // Refresh prompts
    refreshBtn.addEventListener('click', () => {
        generatePrompts(lastTopic);
    });
}); 