// Main application initialization
document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    const profileName = document.getElementById('profile-name');
    const profileEmail= document.getElementById('profile-email');
    

     document.addEventListener("click", function (event) {
        if (event.target.classList.contains("love-btn")) {
            event.target.classList.toggle("active");
            event.target.textContent = event.target.classList.contains("active") ? "❤️" : "🤍";
        }
    });

    
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
    
    const email = sessionStorage.getItem('email');
    const name = sessionStorage.getItem('name');
    if(name){
        profileName.textContent = name;
    }
    if(email){
        profileEmail.textContent = email;
    }

    


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

