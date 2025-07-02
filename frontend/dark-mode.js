// dark-mode.js - Système de mode sombre complet

// Variables pour le mode sombre
let isDarkMode = false;

// Fonction d'initialisation du mode sombre
function initDarkMode() {
    // Vérifier la préférence sauvegardée
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Appliquer le thème sauvegardé ou la préférence système
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        enableDarkMode();
    } else {
        disableDarkMode();
    }
    
    // Créer le bouton toggle
    createDarkModeToggle();
    
    // Écouter les changements de préférence système
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            if (e.matches) {
                enableDarkMode();
            } else {
                disableDarkMode();
            }
        }
    });
}

// Créer le bouton toggle
function createDarkModeToggle() {
    const toggleButton = document.createElement('button');
    toggleButton.className = 'dark-mode-toggle';
    toggleButton.title = 'Basculer le mode sombre';
    toggleButton.setAttribute('aria-label', 'Basculer le mode sombre');
    
    updateToggleIcon(toggleButton);
    
    toggleButton.addEventListener('click', toggleDarkMode);
    
    // Ajouter le bouton au body
    document.body.appendChild(toggleButton);
}

// Mettre à jour l'icône du bouton
function updateToggleIcon(button) {
    const icon = document.createElement('i');
    
    if (isDarkMode) {
        icon.className = 'fas fa-sun';
        button.title = 'Passer en mode clair';
    } else {
        icon.className = 'fas fa-moon';
        button.title = 'Passer en mode sombre';
    }
    
    button.innerHTML = '';
    button.appendChild(icon);
}

// Activer le mode sombre
function enableDarkMode() {
    isDarkMode = true;
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
    
    // Mettre à jour l'icône si le bouton existe
    const toggleButton = document.querySelector('.dark-mode-toggle');
    if (toggleButton) {
        updateToggleIcon(toggleButton);
        toggleButton.classList.add('rotating');
        setTimeout(() => {
            toggleButton.classList.remove('rotating');
        }, 300);
    }
    
    // Notification optionnelle
    if (window.showNotification) {
        showNotification('Mode sombre activé', 'success');
    }
    
    console.log('🌙 Mode sombre activé');
}

// Désactiver le mode sombre
function disableDarkMode() {
    isDarkMode = false;
    document.documentElement.setAttribute('data-theme', 'light');
    localStorage.setItem('theme', 'light');
    
    // Mettre à jour l'icône si le bouton existe
    const toggleButton = document.querySelector('.dark-mode-toggle');
    if (toggleButton) {
        updateToggleIcon(toggleButton);
        toggleButton.classList.add('rotating');
        setTimeout(() => {
            toggleButton.classList.remove('rotating');
        }, 300);
    }
    
    // Notification optionnelle
    if (window.showNotification) {
        showNotification('Mode clair activé', 'success');
    }
    
    console.log('☀️ Mode clair activé');
}

// Basculer entre les modes
function toggleDarkMode() {
    const toggleButton = document.querySelector('.dark-mode-toggle');
    
    // Animation de clic
    if (toggleButton) {
        toggleButton.style.transform = 'scale(0.95)';
        setTimeout(() => {
            toggleButton.style.transform = '';
        }, 150);
    }
    
    // Feedback tactile sur mobile
    if ('vibrate' in navigator) {
        navigator.vibrate(50);
    }
    
    if (isDarkMode) {
        disableDarkMode();
    } else {
        enableDarkMode();
    }
}

// Raccourci clavier (Ctrl/Cmd + D)
function initKeyboardShortcut() {
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
            e.preventDefault();
            toggleDarkMode();
        }
    });
}

// Fonction utilitaire pour obtenir le thème actuel
function getCurrentTheme() {
    return isDarkMode ? 'dark' : 'light';
}

// Fonction utilitaire pour forcer un thème
function setTheme(theme) {
    if (theme === 'dark') {
        enableDarkMode();
    } else {
        disableDarkMode();
    }
}

// Initialisation automatique quand le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initDarkMode();
        initKeyboardShortcut();
    });
} else {
    initDarkMode();
    initKeyboardShortcut();
}

// Exporter les fonctions pour usage externe
window.darkMode = {
    toggle: toggleDarkMode,
    enable: enableDarkMode,
    disable: disableDarkMode,
    getCurrentTheme: getCurrentTheme,
    setTheme: setTheme,
    isDark: () => isDarkMode
};

console.log('🎨 Dark Mode system initialized');
console.log('💡 Raccourci: Ctrl/Cmd + D pour basculer');