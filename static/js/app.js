// DOM Elements
document.addEventListener('DOMContentLoaded', () => {
    // Main elements
    const topicInput = document.getElementById('topic');
    const generateBtn = document.getElementById('generate-btn');
    const resultsSection = document.getElementById('results-section');
    const promptsContainer = document.getElementById('prompts-container');
    const refreshBtn = document.getElementById('refresh-btn');
    const categoryBtns = document.querySelectorAll('.category-btn');
    const suggestionsContainer = document.getElementById('suggestions');
    const trendingTopicsContainer = document.getElementById('trending-topics');

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
    let selectedCategory = categoryBtns.length > 0 ? categoryBtns[0].dataset.category : 'chatgpt';
    let generatedPrompts = [];
    let lastTopic = '';
    let typingTimer;
    const doneTypingInterval = 500; // ms

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

            // Fetch keyword suggestions for this category if there's text in the input
            if (topicInput.value.trim().length > 0) {
                fetchSuggestions(topicInput.value);
            }
            
            // Update trending topics for this category
            fetchTrendingTopics(selectedCategory);
        });
    });

    // Load trending topics on page load
    fetchTrendingTopics();

    // Input events for keyword suggestions
    topicInput.addEventListener('keyup', () => {
        clearTimeout(typingTimer);
        if (topicInput.value.trim().length > 2) {
            typingTimer = setTimeout(fetchSuggestions, doneTypingInterval);
        } else {
            suggestionsContainer.classList.add('hidden');
        }
    });

    topicInput.addEventListener('focus', () => {
        if (topicInput.value.trim().length > 2) {
            fetchSuggestions();
        }
    });

    // Close suggestions when clicking outside
    document.addEventListener('click', (e) => {
        if (!topicInput.contains(e.target) && !suggestionsContainer.contains(e.target)) {
            suggestionsContainer.classList.add('hidden');
        }
    });

    // Fetch trending topics
    function fetchTrendingTopics(category = null) {
        let url = '/api/trending/';
        if (category) {
            url += `?category=${category}`;
        }
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                renderTrendingTopics(data.topics || []);
            })
            .catch(error => {
                console.error('Error fetching trending topics:', error);
                // Show error in trending section
                trendingTopicsContainer.innerHTML = `
                    <div class="px-3 py-1 bg-red-100 text-red-700 text-sm rounded-md">
                        Failed to load trending topics
                    </div>
                `;
            });
    }

    // Render trending topics
    function renderTrendingTopics(topics) {
        if (!topics || topics.length === 0) {
            trendingTopicsContainer.innerHTML = `
                <div class="px-3 py-1 bg-gray-100 text-gray-500 text-sm rounded-md">
                    No trending topics found
                </div>
            `;
            return;
        }
        
        trendingTopicsContainer.innerHTML = '';
        
        topics.forEach(topic => {
            const topicBtn = document.createElement('button');
            topicBtn.className = 'px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-800 text-sm rounded-md flex items-center transition';
            
            // Get the proper category name for color
            let categoryColor;
            switch(topic.category_slug) {
                case 'chatgpt':
                    categoryColor = 'bg-blue-100 text-blue-800';
                    break;
                case 'midjourney':
                    categoryColor = 'bg-purple-100 text-purple-800';
                    break;
                case 'blogging-seo':
                    categoryColor = 'bg-green-100 text-green-800';
                    break;
                case 'coding':
                    categoryColor = 'bg-yellow-100 text-yellow-800';
                    break;
                case 'social-media':
                    categoryColor = 'bg-pink-100 text-pink-800';
                    break;
                default:
                    categoryColor = 'bg-gray-100 text-gray-800';
            }
            
            topicBtn.innerHTML = `
                ${topic.text}
                <span class="ml-1 px-1.5 py-0.5 text-xs rounded ${categoryColor}">${topic.popularity}</span>
            `;
            
            topicBtn.addEventListener('click', () => {
                // Set the topic in the input
                topicInput.value = topic.text;
                
                // Update the category if needed
                if (topic.category_slug !== selectedCategory) {
                    const categoryBtn = document.querySelector(`[data-category="${topic.category_slug}"]`);
                    if (categoryBtn) {
                        categoryBtn.click();
                    }
                }
                
                // Focus the input
                topicInput.focus();
            });
            
            trendingTopicsContainer.appendChild(topicBtn);
        });
    }

    // Fetch keyword suggestions
    function fetchSuggestions() {
        const query = topicInput.value.trim();
        if (query.length < 3) return;

        fetch(`/api/keywords/?category=${selectedCategory}&query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                if (data.suggestions && data.suggestions.length > 0) {
                    renderSuggestions(data.suggestions);
                } else {
                    suggestionsContainer.classList.add('hidden');
                }
            })
            .catch(error => {
                console.error('Error fetching suggestions:', error);
            });
    }

    // Render suggestions in the dropdown
    function renderSuggestions(suggestions) {
        suggestionsContainer.innerHTML = '';
        
        suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.innerHTML = `
                ${suggestion.text} 
                <span class="popularity">(${suggestion.popularity})</span>
            `;
            
            item.addEventListener('click', () => {
                topicInput.value = suggestion.text;
                suggestionsContainer.classList.add('hidden');
            });
            
            suggestionsContainer.appendChild(item);
        });
        
        suggestionsContainer.classList.remove('hidden');
    }

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

        // Make API request
        fetch('/api/generate-prompts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: JSON.stringify({
                topic: topic,
                category: selectedCategory
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                return;
            }

            // Store generated prompts
            generatedPrompts = data.prompts;
            
            // Display prompts
            displayPrompts();

            // Show results section
            resultsSection.classList.remove('hidden');
            
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });
            
            // Update trending topics as they may have changed
            fetchTrendingTopics();
        })
        .catch(error => {
            showError('Failed to generate prompts. Please try again.');
            console.error('Error:', error);
        })
        .finally(() => {
            // Reset generate button
            generateBtn.textContent = 'Generate Prompts';
            generateBtn.classList.remove('loading');
            generateBtn.disabled = false;
        });
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