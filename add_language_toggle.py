#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

# Список файлов для обработки (исключаем index.html и ZombieTrain.html так как они уже обработаны)
html_files = [
    'WitchBound.html',
    'RicochetMaster.html', 
    'QuantumStrike.html',
    'pythonbot.html',
    'novel.html',
    'monsterevolution.html',
    'MCP.html',
    'levels.html',
    'DronMl.html',
    'die2win.html'
]

# Переводы для кнопок и общих элементов
translations = {
    'Назад к резюме': 'Back to Resume',
    'Подробнее о проекте': 'Project Details',
    'Стек проекта': 'Project Stack',
    'Описание': 'Description',
    'Навыки': 'Skills',
    'Образование': 'Education',
    'Языки': 'Languages',
    'Интересы': 'Interests',
    'Кроссплатформенная разработка': 'Cross-platform development',
    'Middle Unity-разработчик': 'Middle Unity Developer',
    'Никита Ищенко': 'Nikita Ishchenko',
    'Новочеркасск': 'Novocherkassk',
    'НПИ': 'NPI',
    'Информатика и вычислительная техника (бакалавр)': 'Computer Science and Engineering (Bachelor)',
    '(на уровне чтения документации)': '(documentation reading level)',
    'Нейросети': 'Neural Networks',
    'Боты для Telegram и Discord': 'Telegram and Discord bots',
    '3D-моделирование': '3D modeling',
    'Работоспособность': 'Work capacity',
    'Стрессоустойчивость': 'Stress resistance',
    'Быстрая обучаемость': 'Fast learning',
    'Критическое мышление': 'Critical thinking',
    'Самоорганизация': 'Self-organization',
    'UniTask (асинхронное программирование)': 'UniTask (asynchronous programming)',
    'Сетевые решения': 'Networking Solutions',
    'WebGL платформа': 'WebGL platform',
    'ИИ & ML': 'AI & ML',
    'Roslyn (компиляция C# кода)': 'Roslyn (C# code compilation)',
    'Интеграция OpenAI API': 'OpenAI API integration',
    'UI & Графика': 'UI & Graphics',
    'UI Toolkit (базовый уровень)': 'UI Toolkit (basic level)',
    'Инструменты': 'Tools',
    'Дополнительно': 'Additional',
    'Python (боты, автоматизация)': 'Python (bots, automation)',
    'JavaScript (веб-разработка)': 'JavaScript (web development)',
    'API интеграция': 'API integration',
    'Мультиплатформенная разработка': 'Multiplatform development'
}

def add_language_toggle_to_file(filepath):
    """Добавляет языковое переключение к HTML файлу"""
    print(f"Обрабатываю файл: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Добавляем CSS файл языкового переключения
    if 'language-toggle.css' not in content:
        content = content.replace(
            '<link href="assets/css/dark-mode.css" rel="stylesheet"/>',
            '<link href="assets/css/dark-mode.css" rel="stylesheet"/>\n<link rel="stylesheet" href="assets/css/language-toggle.css">'
        )
    
    # 2. Добавляем кнопку переключения языков
    if 'language-toggle' not in content:
        language_toggle_html = '''
<!-- Language Toggle -->
<div class="language-toggle">
   <span class="lang-icon ru-icon">RU</span>
   <label class="switch">
      <input type="checkbox" id="languageToggle">
      <span class="slider"></span>
   </label>
   <span class="lang-icon en-icon">EN</span>
</div>'''
        
        content = content.replace(
            '</div>\n<div class="area">',
            f'</div>{language_toggle_html}\n<div class="area">'
        )
    
    # 3. Добавляем JS скрипт
    if 'language-toggle.js' not in content:
        content = content.replace(
            '<script src="assets/js/dark-mode.js"></script>',
            '<script src="assets/js/dark-mode.js"></script>\n<script src="assets/js/language-toggle.js"></script>'
        )
    
    # 4. Оборачиваем текст в языковые контейнеры
    for ru_text, en_text in translations.items():
        # Простая замена для базовых элементов
        if ru_text in content and f'<span class="ru-text">{ru_text}</span>' not in content:
            content = content.replace(
                ru_text,
                f'<span class="ru-text">{ru_text}</span>\n   <span class="en-text">{en_text}</span>'
            )
    
    # 5. Специальные случаи для заголовков и структуры
    
    # Оборачиваем имя в header
    content = re.sub(
        r'<h2 class="resume-name mb-0 text-uppercase">([^<]+)</h2>',
        r'<h2 class="resume-name mb-0 text-uppercase">\n   <span class="ru-text">\1</span>\n   <span class="en-text">Nikita Ishchenko</span>\n</h2>',
        content
    )
    
    # Оборачиваем должность
    content = re.sub(
        r'<div class="resume-tagline mb-3 mb-md-0">([^<]+)</div>',
        r'<div class="resume-tagline mb-3 mb-md-0">\n   <span class="ru-text">\1</span>\n   <span class="en-text">Middle Unity Developer</span>\n</div>',
        content
    )
    
    # Оборачиваем город
    content = re.sub(
        r'<i class="fas fa-map-marker-alt fa-fw fa-lg me-2"></i>([^<\n]+)',
        r'<i class="fas fa-map-marker-alt fa-fw fa-lg me-2"></i>\n<span class="ru-text">\1</span>\n<span class="en-text">Novocherkassk</span>',
        content
    )
    
    # Сохраняем файл
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Файл {filepath} успешно обработан")

def main():
    """Основная функция"""
    print("🚀 Начинаю добавление языкового переключения ко всем страницам проектов...")
    
    for filename in html_files:
        if os.path.exists(filename):
            add_language_toggle_to_file(filename)
        else:
            print(f"⚠️ Файл {filename} не найден")
    
    print("\n✅ Обработка завершена! Языковое переключение добавлено ко всем страницам.")
    print("🔧 Теперь все страницы проектов поддерживают переключение между русским и английским языками.")

if __name__ == '__main__':
    main() 