// Language button functionality
let currentLanguage = 'tn'; // Default language

const languageNames = {
    'tn': 'Tunisian',
    'en': 'English',
    'fr': 'Français',
    'ca': 'Canadian English',
    'ar': 'العربية',
    'es': 'Español'
};

function getPreferredLanguage() {
    // First, try to get language from URL path (e.g., /cv/tn/ -> 'tn')
    const pathSegments = window.location.pathname.split('/');
    const urlLang = pathSegments.find(segment => ['tn', 'en', 'fr', 'ca', 'ar', 'es'].includes(segment));
    if (urlLang) {
        return urlLang;
    }

    // Then, check localStorage
    const savedLanguage = localStorage.getItem('preferredLanguage');
    if (savedLanguage) {
        return savedLanguage;
    }

    // Finally, browser language
    const browserLanguage = navigator.language.split('-')[0];
    return browserLanguage || 'en'; // Fallback to English
}

function changeLanguage(language) {
    currentLanguage = language;
    localStorage.setItem('preferredLanguage', language);
    document.getElementById('languageDropdown').classList.remove('show');
    updateActiveLanguage();
}

function toggleLanguageDropdown() {
    const dropdown = document.getElementById('languageDropdown');
    dropdown.classList.toggle('show');
}

function updateLanguageAndRedirect(selectElement) {
    const selectedOption = selectElement.options[selectElement.selectedIndex];
    const languageName = selectedOption.getAttribute('data-lang');
    const languageSpan = document.getElementById('languageSpan');
    
    if (languageSpan) {
        languageSpan.textContent = '  language ' + languageName;
    }
    
    if (selectedOption.value) {
        window.location.href = selectedOption.value;
    }
}

function initializeLanguageUI() {
    const pathSegments = window.location.pathname.split('/');
    const currentLang = pathSegments.find(segment => ['tn', 'en', 'fr', 'ca', 'ar', 'es'].includes(segment)) || 'tn';
    
    // Update select value
    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        languageSelect.value = languageSelect.querySelector(`option[value*='/${currentLang}/']`)?.value || '';
    }
    
    // Update span with current language
    const languageSpan = document.getElementById('languageSpan');
    const selectedOption = languageSelect?.querySelector('option:checked');
    if (languageSpan && selectedOption) {
        const languageName = selectedOption.getAttribute('data-lang');
        languageSpan.textContent = '  language ' + languageName;
    }
}

function updateActiveLanguage() {
    document.querySelectorAll('.language-option').forEach(option => {
        option.classList.remove('active');
        if (option.getAttribute('data-lang') === currentLanguage) {
            option.classList.add('active');
        }
    });

    // Update the language button span to show the current language name
    const languageSpan = document.querySelector('[data-i18n="buttons.changeLanguage"]');
    if (languageSpan) {
        languageSpan.textContent = 'language ' + (languageNames[currentLanguage] || 'Change Language');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    currentLanguage = getPreferredLanguage();
    updateActiveLanguage();
    initializeLanguageUI();

    // Close dropdown if clicked outside
    document.addEventListener('click', (event) => {
        const dropdown = document.getElementById('languageDropdown');
        const button = document.querySelector('.language-btn');
        if (dropdown && button && !dropdown.contains(event.target) && !button.contains(event.target)) {
            dropdown.classList.remove('show');
        }
    });
});




// another pdf button 
const downloadBtn = document.querySelector(".download-btn");

downloadBtn.addEventListener("click", () => {
  print();
});