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
    const quickQuestionsToggle = document.getElementById('quick-questions-toggle');
    const recentSearchesContainer = document.getElementById('recent-searches');

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
    let recentSearches = getRecentSearches();
    let typingTimer;
    const doneTypingInterval = 500; // ms

    // Load recent searches on page load
    displayRecentSearches();

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

        // Save the topic to recent searches
        saveRecentSearch(topic, selectedCategory);
        displayRecentSearches();

        // Save the topic
        lastTopic = topic;

        // Show loading state
        generateBtn.textContent = 'Generating';
        generateBtn.classList.add('loading');
        generateBtn.disabled = true;

        // Check if we're in quick questions mode
        const isQuickQuestionsMode = quickQuestionsToggle.checked;
        
        // Determine which API endpoint to use
        const apiEndpoint = isQuickQuestionsMode 
            ? '/api/generate-question-prompts/' 
            : '/api/generate-prompts/';

        // Prepare request data based on mode
        const requestData = isQuickQuestionsMode 
            ? { topic } 
            : { topic, category: selectedCategory };

        // Make API request
        fetch(apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN
            },
            body: JSON.stringify(requestData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                showError(data.error);
                return;
            }

            // Store generated prompts
            generatedPrompts = data.prompts;
            
            // Display prompts (with a flag to indicate if these are question prompts)
            displayPrompts(isQuickQuestionsMode);

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
    function displayPrompts(isQuestionPrompts = false) {
        // Clear previous prompts
        promptsContainer.innerHTML = '';

        // Add each prompt with animation delay
        generatedPrompts.forEach((prompt, index) => {
            const promptCard = document.createElement('div');
            promptCard.className = `prompt-card ${isQuestionPrompts ? 'question-prompt-card' : ''} bg-white rounded-xl shadow-md overflow-hidden fade-in`;
            promptCard.style.animationDelay = `${index * 150}ms`;

            promptCard.innerHTML = `
                <div class="p-6">
                    <div class="flex justify-between items-start mb-4">
                        <h4 class="text-lg font-semibold text-gray-800">${prompt.name}</h4>
                        <span class="px-3 py-1 ${isQuestionPrompts ? 'bg-indigo-100 text-indigo-800' : 'bg-indigo-100 text-indigo-800'} rounded-full text-sm font-medium">
                            ${isQuestionPrompts ? 'Question' : capitalizeFirstLetter(selectedCategory)}
                        </span>
                    </div>
                    <div class="bg-gray-50 rounded-lg p-4 mb-4">
                        <p class="text-gray-700 whitespace-pre-line">${prompt.generatedContent}</p>
                    </div>
                    <div class="flex items-center justify-between">
                        <button class="copy-btn flex items-center gap-2 text-indigo-600 hover:text-indigo-800 font-medium transition" data-prompt="${encodeURIComponent(prompt.generatedContent)}">
                            <i class="far fa-copy"></i> Copy
                        </button>
                        <div class="flex items-center gap-2">
                            <button class="share-btn flex items-center gap-1 text-green-600 hover:text-green-800 font-medium transition text-sm" data-prompt="${encodeURIComponent(prompt.generatedContent)}" data-title="${encodeURIComponent(prompt.name)}">
                                <i class="fas fa-share-alt"></i> Share
                            </button>
                            <button class="like-btn flex items-center gap-1 text-red-500 hover:text-red-700 font-medium transition text-sm">
                                <i class="far fa-heart"></i> <span class="like-count">0</span>
                            </button>
                        </div>
                    </div>
                </div>
            `;

            promptsContainer.appendChild(promptCard);
        });

        // Add event listeners to copy buttons
        document.querySelectorAll('.copy-btn').forEach(btn => {
            btn.addEventListener('click', copyToClipboard);
        });
        
        // Add event listeners to share buttons
        document.querySelectorAll('.share-btn').forEach(btn => {
            btn.addEventListener('click', sharePrompt);
        });
        
        // Add event listeners to like buttons
        document.querySelectorAll('.like-btn').forEach(btn => {
            btn.addEventListener('click', likePrompt);
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

    // Share a prompt
    function sharePrompt(e) {
        const promptText = decodeURIComponent(e.currentTarget.dataset.prompt);
        const promptTitle = decodeURIComponent(e.currentTarget.dataset.title);
        
        // Create share options
        const shareOptions = document.createElement('div');
        shareOptions.className = 'absolute right-0 bg-white shadow-lg rounded-lg p-3 z-10 flex flex-col gap-2 share-options fade-in';
        shareOptions.style.top = '100%';
        shareOptions.style.marginTop = '8px';
        
        // Add share options
        shareOptions.innerHTML = `
            <button class="twitter-share flex items-center gap-2 text-blue-400 hover:text-blue-600 transition py-1 px-2 rounded hover:bg-gray-50">
                <i class="fab fa-twitter"></i> Twitter
            </button>
            <button class="facebook-share flex items-center gap-2 text-blue-600 hover:text-blue-800 transition py-1 px-2 rounded hover:bg-gray-50">
                <i class="fab fa-facebook"></i> Facebook
            </button>
            <button class="linkedin-share flex items-center gap-2 text-blue-700 hover:text-blue-900 transition py-1 px-2 rounded hover:bg-gray-50">
                <i class="fab fa-linkedin"></i> LinkedIn
            </button>
            <button class="whatsapp-share flex items-center gap-2 text-green-500 hover:text-green-700 transition py-1 px-2 rounded hover:bg-gray-50">
                <i class="fab fa-whatsapp"></i> WhatsApp
            </button>
            <div class="h-px bg-gray-200 my-1"></div>
            <button class="cancel-share flex items-center gap-2 text-gray-500 hover:text-gray-700 transition py-1 px-2 rounded hover:bg-gray-50">
                <i class="fas fa-times"></i> Cancel
            </button>
        `;
        
        // Position the share options
        e.currentTarget.parentElement.style.position = 'relative';
        e.currentTarget.parentElement.appendChild(shareOptions);
        
        // Handle share clicks
        shareOptions.querySelector('.twitter-share').addEventListener('click', () => {
            window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(`${promptTitle}: ${promptText}`)}%0A%0AGenerated by @promptgenius_ai`);
            shareOptions.remove();
        });
        
        shareOptions.querySelector('.facebook-share').addEventListener('click', () => {
            window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.href)}&quote=${encodeURIComponent(`${promptTitle}: ${promptText}`)}`);
            shareOptions.remove();
        });
        
        shareOptions.querySelector('.linkedin-share').addEventListener('click', () => {
            window.open(`https://www.linkedin.com/shareArticle?mini=true&url=${encodeURIComponent(window.location.href)}&title=${encodeURIComponent(promptTitle)}&summary=${encodeURIComponent(promptText)}`);
            shareOptions.remove();
        });
        
        shareOptions.querySelector('.whatsapp-share').addEventListener('click', () => {
            window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(`${promptTitle}: ${promptText}`)}%0A%0AGenerated by AI Prompt Generator`);
            shareOptions.remove();
        });
        
        shareOptions.querySelector('.cancel-share').addEventListener('click', () => {
            shareOptions.remove();
        });
        
        // Close share options when clicking outside
        document.addEventListener('click', function closeShareOptions(event) {
            if (!shareOptions.contains(event.target) && !e.currentTarget.contains(event.target)) {
                shareOptions.remove();
                document.removeEventListener('click', closeShareOptions);
            }
        });
    }
    
    // Like a prompt
    function likePrompt(e) {
        const likeCount = e.currentTarget.querySelector('.like-count');
        const currentLikes = parseInt(likeCount.textContent);
        
        // Toggle like status
        if (e.currentTarget.classList.contains('liked')) {
            e.currentTarget.classList.remove('liked');
            e.currentTarget.querySelector('i').className = 'far fa-heart';
            likeCount.textContent = currentLikes - 1;
        } else {
            e.currentTarget.classList.add('liked');
            e.currentTarget.querySelector('i').className = 'fas fa-heart';
            likeCount.textContent = currentLikes + 1;
            
            // Add heart animation
            const heart = document.createElement('span');
            heart.className = 'floating-heart';
            heart.innerHTML = '❤️';
            heart.style.left = `${Math.random() * 40 + 30}%`;
            e.currentTarget.appendChild(heart);
            
            setTimeout(() => {
                heart.remove();
            }, 1000);
        }
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

    // Get recent searches from localStorage
    function getRecentSearches() {
        try {
            const saved = localStorage.getItem('recentSearches');
            return saved ? JSON.parse(saved) : [];
        } catch (e) {
            console.error('Error retrieving recent searches:', e);
            return [];
        }
    }

    // Save a search to localStorage
    function saveRecentSearch(topic, category) {
        try {
            // Get current searches
            let searches = getRecentSearches();
            
            // Check if this search already exists
            const existingIndex = searches.findIndex(s => s.topic.toLowerCase() === topic.toLowerCase());
            if (existingIndex >= 0) {
                // Remove it so we can add it to the front
                searches.splice(existingIndex, 1);
            }
            
            // Add new search at the beginning
            searches.unshift({ 
                topic, 
                category,
                timestamp: new Date().toISOString()
            });
            
            // Keep only the 10 most recent
            searches = searches.slice(0, 10);
            
            // Save back to localStorage
            localStorage.setItem('recentSearches', JSON.stringify(searches));
            recentSearches = searches;
        } catch (e) {
            console.error('Error saving recent search:', e);
        }
    }

    // Display recent searches in the UI
    function displayRecentSearches() {
        if (!recentSearches || recentSearches.length === 0) {
            recentSearchesContainer.innerHTML = `
                <div class="px-3 py-1 bg-gray-100 text-gray-500 text-sm rounded-md">
                    No recent searches
                </div>
            `;
            return;
        }
        
        recentSearchesContainer.innerHTML = '';
        
        recentSearches.slice(0, 5).forEach((search, index) => {
            const searchBtn = document.createElement('button');
            searchBtn.className = 'px-3 py-1 bg-gray-100 hover:bg-gray-200 text-gray-800 text-sm rounded-md flex items-center transition';
            searchBtn.style.setProperty('--index', index);
            
            // Find the proper category for color
            let categoryName = 'General';
            let categorySlug = search.category || 'chatgpt';
            
            // Try to find the category button to get its text
            const categoryBtn = document.querySelector(`[data-category="${categorySlug}"]`);
            if (categoryBtn) {
                categoryName = categoryBtn.textContent.trim();
            }
            
            searchBtn.innerHTML = `
                <i class="fas fa-history text-gray-400 mr-1"></i>
                ${search.topic}
            `;
            
            searchBtn.addEventListener('click', () => {
                // Set the topic in the input
                topicInput.value = search.topic;
                
                // Update the category if needed
                if (categorySlug && categorySlug !== selectedCategory) {
                    const categoryBtn = document.querySelector(`[data-category="${categorySlug}"]`);
                    if (categoryBtn) {
                        categoryBtn.click();
                    }
                }
                
                // Focus the input
                topicInput.focus();
            });
            
            recentSearchesContainer.appendChild(searchBtn);
        });
        
        // Add a clear history button if there are searches
        if (recentSearches.length > 0) {
            const clearBtn = document.createElement('button');
            clearBtn.className = 'px-2 py-1 bg-red-50 hover:bg-red-100 text-red-600 text-xs rounded-md flex items-center transition ml-auto';
            clearBtn.innerHTML = `
                <i class="fas fa-trash-alt mr-1"></i>
                Clear
            `;
            clearBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                clearRecentSearches();
            });
            recentSearchesContainer.appendChild(clearBtn);
        }
    }

    // Clear all recent searches
    function clearRecentSearches() {
        try {
            localStorage.removeItem('recentSearches');
            recentSearches = [];
            displayRecentSearches();
        } catch (e) {
            console.error('Error clearing recent searches:', e);
        }
    }
}); 