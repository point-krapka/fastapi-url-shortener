document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('login-form');
    const loginInput = document.getElementById('login');
    const passwordInput = document.getElementById('password');
    const loginError = document.getElementById('login-error');
    const passwordError = document.getElementById('password-error');
    const loginButton = document.getElementById('login-button');
    const buttonText = document.querySelector('.button-text');
    const loader = document.getElementById('loader');
    const feedbackDiv = document.getElementById('form-feedback');

    const validateField = (value, fieldName) => {
        const pattern = /^[a-zA-Z0-9_]+$/;
        
        if (!value || value.length === 0) {
            return `${fieldName} is required`;
        }
        if (value.length < 5) {
            return `${fieldName} must be at least 5 characters`;
        }
        if (value.length > 16) {
            return `${fieldName} must not exceed 16 characters`;
        }
        if (!pattern.test(value)) {
            return `${fieldName} can only contain letters, numbers, and underscore`;
        }
        return '';
    };

    const clearErrors = () => {
        loginError.textContent = '';
        passwordError.textContent = '';
        loginInput.classList.remove('error');
        passwordInput.classList.remove('error');
        feedbackDiv.style.display = 'none';
        feedbackDiv.className = 'feedback-message';
        feedbackDiv.textContent = '';
    };

    const showFieldError = (input, errorElement, message) => {
        input.classList.add('error');
        errorElement.textContent = message;
        
        input.style.animation = 'shake 0.5s ease';
        setTimeout(() => {
            input.style.animation = '';
        }, 500);
    };

    const showFeedback = (message, type) => {
        feedbackDiv.textContent = message;
        feedbackDiv.className = `feedback-message ${type}`;
        feedbackDiv.style.display = 'block';
        
        if (type === 'success') {
            setTimeout(() => {
                feedbackDiv.style.display = 'none';
            }, 5000);
        }
    };

    const setLoadingState = (isLoading) => {
        if (isLoading) {
            loginButton.disabled = true;
            buttonText.style.opacity = '0';
            loader.style.display = 'inline-block';
        } else {
            loginButton.disabled = false;
            buttonText.style.opacity = '1';
            loader.style.display = 'none';
        }
    };

    if (!document.querySelector('#shake-animation')) {
        const style = document.createElement('style');
        style.id = 'shake-animation';
        style.textContent = `
            @keyframes shake {
                0%, 100% { transform: translateX(0); }
                10%, 30%, 50%, 70%, 90% { transform: translateX(-2px); }
                20%, 40%, 60%, 80% { transform: translateX(2px); }
            }
        `;
        document.head.appendChild(style);
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        clearErrors();

        const login = loginInput.value.trim();
        const password = passwordInput.value;

        const loginErrorMsg = validateField(login, 'Username');
        const passwordErrorMsg = validateField(password, 'Password');

        let hasError = false;

        if (loginErrorMsg) {
            showFieldError(loginInput, loginError, loginErrorMsg);
            hasError = true;
        }

        if (passwordErrorMsg) {
            showFieldError(passwordInput, passwordError, passwordErrorMsg);
            hasError = true;
        }

        if (hasError) {
            return;
        }

        setLoadingState(true);

        try {
            const response = await fetch('/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ login, password }),
            });

            if (response.status === 200) {
                const userData = await response.json();
                showFeedback('Login successful! Redirecting...', 'success');
                setTimeout(() => {
                    window.location.href = '/';
                }, 1500);
                
            } else if (response.status === 401) {
                showFeedback('Incorrect username or password', 'error');
                showFieldError(loginInput, loginError, 'Invalid credentials');
                showFieldError(passwordInput, passwordError, 'Invalid credentials');
                
            } else if (response.status === 422) {
                try {
                    const errorData = await response.json();
                    
                    if (errorData.detail && Array.isArray(errorData.detail)) {
                        errorData.detail.forEach(err => {
                            const field = err.loc[err.loc.length - 1];
                            const errorMsg = err.msg || 'Invalid value';
                            
                            if (field === 'login') {
                                showFieldError(loginInput, loginError, errorMsg);
                            } else if (field === 'password') {
                                showFieldError(passwordInput, passwordError, errorMsg);
                            }
                        });
                    } else {
                        showFeedback('Validation error. Please check your input.', 'error');
                    }
                } catch (e) {
                    showFeedback('Validation error', 'error');
                }
                
            } else {
                showFeedback('An error occurred. Please try again later.', 'error');
            }
            
        } catch (error) {
            console.error('Network error:', error);
            showFeedback('Network error. Please check your connection.', 'error');
            
        } finally {
            setLoadingState(false);
        }
    });

    loginInput.addEventListener('input', () => {
        if (loginInput.classList.contains('error')) {
            const errorMsg = validateField(loginInput.value.trim(), 'Username');
            if (!errorMsg) {
                loginInput.classList.remove('error');
                loginError.textContent = '';
            }
        }
    });

    passwordInput.addEventListener('input', () => {
        if (passwordInput.classList.contains('error')) {
            const errorMsg = validateField(passwordInput.value, 'Password');
            if (!errorMsg) {
                passwordInput.classList.remove('error');
                passwordError.textContent = '';
            }
        }
    });

    loginInput.addEventListener('focus', () => {
        loginInput.classList.remove('error');
        loginError.textContent = '';
    });

    passwordInput.addEventListener('focus', () => {
        passwordInput.classList.remove('error');
        passwordError.textContent = '';
    });

    const inputs = document.querySelectorAll('input');
    inputs.forEach(input => {
        input.addEventListener('blur', () => {
            if (input.value.trim() !== '') {
                input.style.borderColor = '#6366f1';
            } else {
                input.style.borderColor = '#e5e7eb';
            }
        });
    });
});