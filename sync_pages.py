#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для синхронизации дублирующихся секций между index.html и страницами проектов.
Автоматически обновляет контакты, описание, навыки, образование, языки, интересы и footer.
"""

import os
import glob
from bs4 import BeautifulSoup, NavigableString
import argparse
from typing import List


class HTMLSyncer:
    def __init__(self, source_file: str = "index.html"):
        self.source_file = source_file
        self.source_soup = None
        
        # Список секций для синхронизации с более точными селекторами
        self.sections_to_sync = [
            {
                'name': 'Контакты',
                'selector': '.resume-contact',
                'parent_selector': None
            },
            {
                'name': 'Описание', 
                'selector': '.resume-intro',
                'parent_selector': None
            },
            {
                'name': 'Навыки',
                'selector': 'aside .skills-section',
                'parent_selector': 'aside'
            },
            {
                'name': 'Образование',
                'selector': 'aside .education-section', 
                'parent_selector': 'aside'
            },
            {
                'name': 'Языки',
                'selector': 'aside .skills-section:has(h3:contains("Языки"))',
                'parent_selector': 'aside'
            },
            {
                'name': 'Интересы',
                'selector': 'aside .skills-section:has(h3:contains("Интересы"))',
                'parent_selector': 'aside'
            },
            {
                'name': 'Footer',
                'selector': '.resume-footer',
                'parent_selector': None
            }
        ]

    def load_source(self) -> bool:
        """Загружает исходный файл"""
        try:
            with open(self.source_file, 'r', encoding='utf-8') as f:
                self.source_soup = BeautifulSoup(f.read(), 'html.parser')
            return True
        except Exception as e:
            print(f"Ошибка при загрузке {self.source_file}: {e}")
            return False

    def get_section_content(self, selector: str) -> BeautifulSoup:
        """Извлекает содержимое секции из исходного файла"""
        if not self.source_soup:
            return None
        
        # Обработка специальных селекторов
        if 'Языки' in selector:
            # Ищем секцию с заголовком "Языки"
            h3_tags = self.source_soup.find_all('h3')
            for h3 in h3_tags:
                if 'Языки' in h3.get_text():
                    return h3.find_parent('section')
        elif 'Интересы' in selector:
            # Ищем секцию с заголовком "Интересы"
            h3_tags = self.source_soup.find_all('h3')
            for h3 in h3_tags:
                if 'Интересы' in h3.get_text():
                    return h3.find_parent('section')
        else:
            element = self.source_soup.select_one(selector)
            return element
        
        return None

    def find_target_files(self) -> List[str]:
        """Находит все HTML файлы кроме исходного"""
        all_files = glob.glob("*.html")
        return [f for f in all_files if f != self.source_file]

    def sync_file(self, target_file: str) -> bool:
        """Синхронизирует один файл"""
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                target_soup = BeautifulSoup(f.read(), 'html.parser')

            changes_made = False
            
            for section_info in self.sections_to_sync:
                source_element = self.get_section_content(section_info['selector'])
                if not source_element:
                    print(f"  Предупреждение: секция {section_info['name']} не найдена в исходном файле")
                    continue

                # Найти соответствующий элемент в целевом файле  
                if 'Языки' in section_info['selector']:
                    h3_tags = target_soup.find_all('h3')
                    target_element = None
                    for h3 in h3_tags:
                        if 'Языки' in h3.get_text():
                            target_element = h3.find_parent('section')
                            break
                elif 'Интересы' in section_info['selector']:
                    h3_tags = target_soup.find_all('h3')
                    target_element = None
                    for h3 in h3_tags:
                        if 'Интересы' in h3.get_text():
                            target_element = h3.find_parent('section')
                            break
                else:
                    target_element = target_soup.select_one(section_info['selector'])

                if target_element:
                    # Создаем копию исходного элемента
                    new_element = BeautifulSoup(str(source_element), 'html.parser').find()
                    target_element.replace_with(new_element)
                    changes_made = True
                    print(f"  ✓ Обновлена секция: {section_info['name']}")
                else:
                    print(f"  ⚠ Секция {section_info['name']} не найдена в {target_file}")

            if changes_made:
                # Записываем обновленный файл
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(str(target_soup))
                return True
            else:
                print(f"  Нет изменений для {target_file}")
                return False

        except Exception as e:
            print(f"Ошибка при синхронизации {target_file}: {e}")
            return False

    def sync_all(self) -> None:
        """Синхронизирует все файлы"""
        if not self.load_source():
            return

        target_files = self.find_target_files()
        if not target_files:
            print("Целевые файлы не найдены")
            return

        print(f"Найдено {len(target_files)} файлов для синхронизации:")
        for file in target_files:
            print(f"  • {file}")

        print("\nНачинаем синхронизацию...")
        
        successful = 0
        for target_file in target_files:
            print(f"\n📄 Обрабатываем {target_file}...")
            if self.sync_file(target_file):
                successful += 1

        print(f"\n✅ Синхронизация завершена!")
        print(f"Успешно обновлено: {successful}/{len(target_files)} файлов")

    def show_sections(self) -> None:
        """Показывает найденные секции в исходном файле"""
        if not self.load_source():
            return
            
        print(f"📋 Секции найденные в {self.source_file}:")
        for section_info in self.sections_to_sync:
            element = self.get_section_content(section_info['selector'])
            status = "✅ Найдена" if element else "❌ Не найдена"
            print(f"  {section_info['name']}: {status}")


def main():
    parser = argparse.ArgumentParser(description="Синхронизация HTML страниц")
    parser.add_argument('--source', default='index.html', help='Исходный файл (по умолчанию: index.html)')
    parser.add_argument('--show-sections', action='store_true', help='Показать найденные секции')
    
    args = parser.parse_args()
    
    syncer = HTMLSyncer(args.source)
    
    if args.show_sections:
        syncer.show_sections()
    else:
        syncer.sync_all()


if __name__ == "__main__":
    main() 