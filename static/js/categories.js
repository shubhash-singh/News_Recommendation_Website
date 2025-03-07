class CategoriesManager {
    constructor() {
        this.categories = [
            'Business', 'Technology', 'Entertainment', 'Sports', 'Science',
            'Health', 'Politics', 'World', 'Environment', 'Education',
            'Fashion', 'Food', 'Travel', 'Art', 'Music',
            'Movies', 'Books', 'Gaming', 'Automotive', 'Real Estate'
        ];
        this.selectedCategories = new Set();
        this.init();
    }

    init() {
        document.getElementById('categories-link').addEventListener('click', (e) => {
            e.preventDefault();
            this.showCategoriesModal();
        });

        document.getElementById('update-categories-btn').addEventListener('click', () => {
            this.updateCategories();
        });

        this.populateCategoriesGrid();
    }

    populateCategoriesGrid() {
        const grid = document.getElementById('categories-grid');
        grid.innerHTML = '';

        this.categories.forEach(category => {
            const categoryItem = document.createElement('div');
            categoryItem.className = 'category-item';
            categoryItem.textContent = category;
            
            if (this.selectedCategories.has(category)) {
                categoryItem.classList.add('selected');
            }

            categoryItem.addEventListener('click', () => this.toggleCategory(categoryItem, category));
            grid.appendChild(categoryItem);
        });
    }

    toggleCategory(element, category) {
        element.classList.toggle('selected');
        if (this.selectedCategories.has(category)) {
            this.selectedCategories.delete(category);
        } else {
            this.selectedCategories.add(category);
        }
    }

    showCategoriesModal() {
        const modal = document.getElementById('categories-modal');
        modal.classList.add('active');
    }

    closeCategoriesModal() {
        const modal = document.getElementById('categories-modal');
        modal.classList.remove('active');
    }

    async updateCategories() {
        const token = sessionStorage.getItem('token');
        const email = sessionStorage.getItem('email'); // Retrieve email from session storage
    
        if (!token || !email) {
            alert('Please login to update categories.');
            return;
        }
    
        try {
            const response = await fetch('http://127.0.0.1:8000/update_categories/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    email: email, 
                    topics: Array.from(this.selectedCategories) // Convert Set to an array
                })
            });
    
            const data = await response.json(); // Parse JSON response
    
            if (response.ok && data.success === true) { // Check if success = true
                alert('Categories updated successfully!');
                this.closeCategoriesModal();
                
                // Refresh recommended news if we're viewing them
                if (newsManager.currentView === 'recommended') {
                    newsManager.fetchRecommendedNews();
                }
            } else {
                alert('Failed to update categories.');
            }
        } catch (error) {
            console.error('Error updating categories:', error);
            alert('An error occurred while updating categories.');
        }
    }
}    
const categoriesManager = new CategoriesManager();