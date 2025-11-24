"""Internationalization (i18n) manager for BackupWin"""
import json
import os
from pathlib import Path
from typing import Dict, Optional
from gui.locales.en import en
from gui.locales.vi import vi


class I18n:
    """Internationalization manager"""

    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'vi': 'Tiếng Việt'
    }

    TRANSLATIONS = {
        'en': en,
        'vi': vi
    }

    def __init__(self, default_language: str = 'en'):
        self.current_language = default_language
        self.config_file = Path('.language_config.json')
        self._load_language_preference()

    def _load_language_preference(self):
        """Load saved language preference"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    saved_lang = config.get('language', 'en')
                    if saved_lang in self.SUPPORTED_LANGUAGES:
                        self.current_language = saved_lang
        except Exception:
            pass  # Use default if can't load

    def _save_language_preference(self):
        """Save language preference"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({'language': self.current_language}, f, ensure_ascii=False, indent=2)
        except Exception:
            pass  # Ignore save errors

    def set_language(self, language: str):
        """Set current language"""
        if language in self.SUPPORTED_LANGUAGES:
            self.current_language = language
            self._save_language_preference()
            return True
        return False

    def get_language(self) -> str:
        """Get current language"""
        return self.current_language

    def get_language_name(self, lang_code: Optional[str] = None) -> str:
        """Get language display name"""
        code = lang_code or self.current_language
        return self.SUPPORTED_LANGUAGES.get(code, 'English')

    def t(self, key: str, **kwargs) -> str:
        """
        Translate a key to current language

        Args:
            key: Translation key
            **kwargs: Format arguments for the translation string

        Returns:
            Translated string
        """
        translations = self.TRANSLATIONS.get(self.current_language, self.TRANSLATIONS['en'])
        text = translations.get(key, key)

        # Format the string if kwargs provided
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError):
                pass  # Return unformatted if error

        return text

    def __call__(self, key: str, **kwargs) -> str:
        """Shortcut for t() method"""
        return self.t(key, **kwargs)


# Global i18n instance
_i18n = I18n()


def get_i18n() -> I18n:
    """Get global i18n instance"""
    return _i18n


def t(key: str, **kwargs) -> str:
    """Shortcut function for translation"""
    return _i18n.t(key, **kwargs)


def set_language(language: str):
    """Set global language"""
    return _i18n.set_language(language)


def get_current_language() -> str:
    """Get current language"""
    return _i18n.get_language()
