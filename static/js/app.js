// Main application initialization
document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    
    menuToggle.addEventListener('click', () => {
        sidebar.classList.toggle('active');
    });

    // Close sidebar when clicking a link (mobile)
    sidebar.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                sidebar.classList.remove('active');
            }
        });
    });

    // Close modals when clicking outside
    window.addEventListener('click', (e) => {
        const authModal = document.getElementById('auth-modal');
        const categoriesModal = document.getElementById('categories-modal');
        
        if (e.target === authModal) {
            authModal.classList.remove('active');
        }
        
        if (e.target === categoriesModal) {
            categoriesModal.classList.remove('active');
        }
    });

    // Handle navigation
    document.getElementById('home-link').addEventListener('click', (e) => {
        e.preventDefault();
        newsManager.switchView('top');
    });

    // Initial news load
    newsManager.fetchTopNews();
});