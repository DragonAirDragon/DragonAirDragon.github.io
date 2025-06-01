document.addEventListener('DOMContentLoaded', function() {
    const savedLanguage = localStorage.getItem('language');
    const browserLanguage = navigator.language.startsWith('en') ? 'en' : 'ru';
    
    // Устанавливаем язык: сохраненный -> язык браузера -> русский по умолчанию
    const currentLanguage = savedLanguage || browserLanguage;
    
    if (currentLanguage === 'en') {
        document.body.classList.add('lang-en');
        document.getElementById('languageToggle').checked = true;
    } else {
        document.body.classList.add('lang-ru');
        document.getElementById('languageToggle').checked = false;
    }
    
    document.getElementById('languageToggle').addEventListener('change', function() {
        if (this.checked) {
            // Переключение на английский
            document.body.classList.remove('lang-ru');
            document.body.classList.add('lang-en');
            localStorage.setItem('language', 'en');
        } else {
            // Переключение на русский
            document.body.classList.remove('lang-en');
            document.body.classList.add('lang-ru');
            localStorage.setItem('language', 'ru');
        }
    });
}); 