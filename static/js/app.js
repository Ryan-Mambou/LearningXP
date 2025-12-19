// API Base URL
const API_BASE_URL = window.location.origin;

// State
let users = [];

// DOM Elements
const userForm = document.getElementById('userForm');
const usersList = document.getElementById('usersList');
const healthStatus = document.getElementById('healthStatus');
const statusIndicator = document.getElementById('statusIndicator');
const statusText = document.getElementById('statusText');

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    loadUsers();
    checkHealth();
    
    // Refresh users every 5 seconds
    setInterval(loadUsers, 5000);
    setInterval(checkHealth, 10000);
});

// Load users from API
async function loadUsers() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/users`);
        if (!response.ok) {
            throw new Error('Failed to load users');
        }
        const data = await response.json();
        users = data.users || [];
        renderUsers();
    } catch (error) {
        console.error('Error loading users:', error);
        usersList.innerHTML = '<p class="error">Erreur lors du chargement des utilisateurs</p>';
    }
}

// Render users list
function renderUsers() {
    if (users.length === 0) {
        usersList.innerHTML = '<p class="loading">Aucun utilisateur pour le moment</p>';
        return;
    }

    usersList.innerHTML = users.map(user => `
        <div class="user-item">
            <div class="user-info">
                <div class="user-name">${escapeHtml(user.name)}</div>
                <div class="user-email">${escapeHtml(user.email)}</div>
            </div>
            <span class="user-id">#${user.id}</span>
        </div>
    `).join('');
}

// Handle form submission
userForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    
    const userData = {
        name: nameInput.value.trim(),
        email: emailInput.value.trim()
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/users`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to create user');
        }

        const newUser = await response.json();
        showMessage(`Utilisateur "${newUser.name}" ajouté avec succès!`, 'success');
        
        // Reset form
        nameInput.value = '';
        emailInput.value = '';
        
        // Reload users
        loadUsers();
    } catch (error) {
        console.error('Error creating user:', error);
        showMessage(`Erreur: ${error.message}`, 'error');
    }
});

// Check health status
async function checkHealth() {
    statusIndicator.className = 'status-indicator checking';
    statusText.textContent = 'Vérification...';

    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        if (response.ok) {
            const data = await response.json();
            statusIndicator.className = 'status-indicator healthy';
            statusText.textContent = `Statut: ${data.status || 'healthy'}`;
        } else {
            throw new Error('Health check failed');
        }
    } catch (error) {
        console.error('Health check error:', error);
        statusIndicator.className = 'status-indicator unhealthy';
        statusText.textContent = 'Statut: unhealthy';
    }
}

// Show message
function showMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = type;
    messageDiv.textContent = message;
    
    const formSection = userForm.closest('.form-section');
    formSection.appendChild(messageDiv);
    
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

