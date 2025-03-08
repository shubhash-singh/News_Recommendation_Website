class NewsManager {
    constructor() {
        this.currentView = 'top';
        this.init();
    }

    init() {
        // Event listeners for news toggle
        document.getElementById('top-news-btn').addEventListener('click', () => this.switchView('top'));
        document.getElementById('recommended-news-btn').addEventListener('click', () => this.switchView('recommended'));
      
    }

    async fetchTopNews() {
        console.log("Fetching Top News...");
        try {
            const response = await fetch('http://127.0.0.1:8000/top_news/', {
                method: 'GET',
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                const data = await response.json();
                this.displayNews(data.news);
            } else {
                console.error('Failed to fetch top news.');
            }
        } catch (error) {
            console.error('Error fetching top news:', error);
        }
    }

    async fetchRecommendedNews() {
        const email = sessionStorage.getItem('email');
        if (!email) return;

        try {
            const response = await fetch('http://127.0.0.1:8000/recommended_news/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email:email})
            });

            if (response.ok) {
                const data = await response.json();
                this.displayNews(data.news);
            } else {
                console.error('Failed to fetch recommended news.');
            }
        } catch (error) {
            console.error('Error fetching recommended news:', error);
        }
    }

    displayNews(newsItems) {
        const newsContainer = document.getElementById('news-container');
        newsContainer.innerHTML = '';
    
        newsItems.forEach(news => {
            const newsItem = document.createElement('div');
            newsItem.className = 'news-item';
            
            // Create summarized version of content
            const summary = this.createSummary(news.content || news.description || '');
    
            newsItem.innerHTML = `                        
                <div class="image-container">
                    <img src="${news.image || 'placeholder.jpg'}" alt="News Image">
                    <button class="love-btn" data-url="${news.url}">🤍</button>
                </div>
                <div class="news-item-content">
                    <h3><a href="${news.url}" target="_blank" class="news-title" data-url="${news.url}">${news.title}</a></h3>
                    <p class="publisher"><strong>Published by:</strong> ${news.domain || 'Unknown'}</p>
                    <p class="bias"><strong>Bias:</strong> ${news.Bias || 'Unknown'}</p>
                    <p class="factual-reporting"><strong>Factual Reporting:</strong> ${news.Factual_Reporting || 'Unknown'}</p>
                    <p class="credibility"><strong>Credibility:</strong> ${news.Credibility || 'Unknown'}</p>
                    <p class="summary">${news.summary}</p>

                    <!-- Polarity Slider -->
                        <div class="slider-container">
                            <label><strong>Polarity:</strong></label>
                            <div class="slider-wrapper">
                                <span class="slider-label">-ve</span>
                                <input type="range" id="polarity-slider" min="-1" max="1" step="0.01" value="${news.polarity}" disabled>
                                <span class="slider-label">+ve</span>
                            </div>
                        </div>

                        <!-- Subjectivity Slider -->
                        <div class="slider-container">
                            <label><strong>Subjectivity:</strong></label>
                            <div class="slider-wrapper">
                                <span class="slider-label">Opinion</span>
                                <input type="range" id="subjectivity-slider" min="-1" max="1" step="0.01" value="${news.subjectivity}" disabled>
                                <span class="slider-label">Factual</span>
                            </div>
                        </div>

                </div>
`;

    
            // Check if user is logged in
            const isLoggedIn = !!sessionStorage.getItem('email');
    
            // Event listener for love button
            const loveBtn = newsItem.querySelector('.love-btn');
            loveBtn.addEventListener('click', () => {
                if (isLoggedIn) {
                    this.handleLove(news.url);
                } else {
                    alert('Please login to save news.');
                }
            });
    
            // Event listener for news title click
            const newsTitle = newsItem.querySelector('.news-title');
            newsTitle.addEventListener('click', (event) => {
                if (isLoggedIn) {
                    this.handleLove(news.url);
                } else {
                    alert('Please login to open the Full article.');
                    event.preventDefault(); // Prevent navigation if not logged in
                }
            });    
            newsContainer.appendChild(newsItem);
        });
    }
    


    createSummary(content) {
        // Create a summary of about 100 characters
        return content.length > 100 ? content.substring(0, 100) + '...' : content;
    }

    async handleLove(newsUrl) {
        const email = sessionStorage.getItem('email');
        if (!email) {
            alert('Please login to save news.');
            return;
        }
        try {
            const response = await fetch('http://127.0.0.1:8000/like_news/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({email : email, url: newsUrl })
            });

            if (response.ok) {
                alert('News saved successfully!');
            } else {
                alert('Failed to save news.');
            }
        } catch (error) {
            console.error('Error saving news:', error);
            alert('An error occurred while saving the news.');
        }
    }

    switchView(view) {
        this.currentView = view;
        
        // Update button states
        document.getElementById('top-news-btn').classList.toggle('active', view === 'top');
        document.getElementById('recommended-news-btn').classList.toggle('active', view === 'recommended');

        // Fetch appropriate news
        if (view === 'top') {
            this.fetchTopNews();
        } else {
            this.fetchRecommendedNews();
        }
    }

   

}

const newsManager = new NewsManager();