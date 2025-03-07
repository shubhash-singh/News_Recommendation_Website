class AuthManager {
    constructor() {
        this.isLoggedIn = false;
        this.init();
    }

    init() {
        // Check if user is logged in
        const token = sessionStorage.getItem('token');
        this.isLoggedIn = !!token;
        this.updateUI();

        // Event Listeners
        document.getElementById('auth-btn').addEventListener('click', () => this.toggleAuthModal());
        document.getElementById('logout-link').addEventListener('click', (e) => {
            e.preventDefault();
            this.logout();
        });

        // Auth forms
        const loginForm = document.getElementById('login-form');
        const signupForm = document.getElementById('signup-form');
        
        loginForm.addEventListener('submit', (e) => this.handleLogin(e));
        signupForm.addEventListener('submit', (e) => this.handleSignup(e));

        // Tab switching
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', () => this.switchTab(btn.dataset.tab));
        });
    }

    async handleLogin(e) {
        e.preventDefault();
        const form = e.target;
        const email = form.querySelector('input[type="text"]').value;
        const password = form.querySelector('input[type="password"]').value;
        const errorDiv = form.querySelector('.error-message');

        try {
            const response = await fetch('http://127.0.0.1:8000/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });

            if (response.ok) {
                const data = await response.json();
                sessionStorage.setItem('token', data.token);
                this.isLoggedIn = true;
                this.updateUI();
                this.closeAuthModal();
                errorDiv.textContent = '';

                // const user_data = 
            } else {
                const error = await response.json();
                errorDiv.textContent = error.message || 'Login failed. Please check your credentials.';
            }
        } catch (error) {
            console.error('Login error:', error);
            errorDiv.textContent = 'An error occurred during login.';
        }
    }

    async handleSignup(e) {
        e.preventDefault();
        const form = e.target;
        const name = form.querySelector('input[placeholder="Name"]').value;
        const email = form.querySelector('input[placeholder="Username"]').value;
        const password = form.querySelector('input[placeholder="Password"]').value;
        const errorDiv = form.querySelector('.error-message');

        try {
            const response = await fetch('http://127.0.0.1:8000/signup/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, email, password })
            });

            if (response.ok) {
                const data = await response.json();
                sessionStorage.setItem('token', data.token);
                this.isLoggedIn = true;
                this.updateUI();
                this.closeAuthModal();
                errorDiv.textContent = '';
                
                // Show categories selection for new users
                categoriesManager.showCategoriesModal();
            } else {
                const error = await response.json();
                errorDiv.textContent = error.message || 'Signup failed. Please try again.';
            }
        } catch (error) {
            console.error('Signup error:', error);
            errorDiv.textContent = 'An error occurred during signup.';
        }
    }

    logout() {
        sessionStorage.removeItem('token');
        this.isLoggedIn = false;
        this.updateUI();
        location.reload();
    }

    updateUI() {
        const authBtn = document.getElementById('auth-btn');
        authBtn.textContent = this.isLoggedIn ? 'Profile' : 'Login / Signup';
        
        // Show/hide auth-required elements
        document.querySelectorAll('.auth-required').forEach(el => {
            el.classList.toggle('hidden', !this.isLoggedIn);
        });
        
        // Show/hide recommended news button based on login status
        const recommendedBtn = document.getElementById('recommended-news-btn');
        recommendedBtn.classList.toggle('hidden', !this.isLoggedIn);
    }

    toggleAuthModal() {
        const modal = document.getElementById('auth-modal');
        modal.classList.toggle('active');
    }

    closeAuthModal() {
        const modal = document.getElementById('auth-modal');
        modal.classList.remove('active');
    }

    switchTab(tab) {
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tab);
        });
        
        document.getElementById('login-form').classList.toggle('hidden', tab !== 'login');
        document.getElementById('signup-form').classList.toggle('hidden', tab !== 'signup');

        // Clear error messages when switching tabs
        document.querySelectorAll('.error-message').forEach(el => {
            el.textContent = '';
        });
    }
}

const authManager = new AuthManager();