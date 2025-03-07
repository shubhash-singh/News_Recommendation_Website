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
        const token = sessionStorage.getItem('token');
        if (!token) return;

        try {
            const response = await fetch('http://127.0.0.1:8000/recommended_news/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                }
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
                <img src="${news.urlToImage || 'placeholder.jpg'}" alt="News Image">
                <div class="news-item-content">
                    <h3><a href="${news.url}" target="_blank">${news.title}</a></h3>
                    <p class="date">${new Date(news.publishedAt).toLocaleString()}</p>
                    <p class="summary">${summary}</p>
                    <button class="love-btn" data-url="${news.url}">❤</button>
                </div>
            `;

            // Add love button event listener
            const loveBtn = newsItem.querySelector('.love-btn');
            loveBtn.addEventListener('click', () => this.handleLove(news.url));

            newsContainer.appendChild(newsItem);
        });
    }

    createSummary(content) {
        // Create a summary of about 100 characters
        return content.length > 100 ? content.substring(0, 100) + '...' : content;
    }

    async handleLove(newsUrl) {
        const token = sessionStorage.getItem('token');
        if (!token) {
            alert('Please login to save news.');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:8000/save_news/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ url: newsUrl })
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