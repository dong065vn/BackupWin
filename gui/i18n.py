"""Internationalization (i18n) manager for BackupWin"""
import json
from pathlib import Path
from gui.locales.en import en
from gui.locales.vi import vi


class I18n:
    """Internationalization manager"""
    SUPPORTED_LANGUAGES = {'en': 'English', 'vi': 'Tiếng Việt'}
    TRANSLATIONS = {'en': en, 'vi': vi}

    def __init__(self, default_language: str = 'vi'):
        self.current_language = default_language
        self.config_file = Path('.language_config.json')
        self._load_language_preference()

    def _load_language_preference(self):
        try:
            if self.config_file.exists():
                config = json.loads(self.config_file.read_text(encoding='utf-8'))
                if (lang := config.get('language', 'vi')) in self.SUPPORTED_LANGUAGES:
                    self.current_language = lang
        except Exception:
            pass

    def _save_language_preference(self):
        try:
            self.config_file.write_text(json.dumps({'language': self.current_language}, ensure_ascii=False, indent=2), encoding='utf-8')
        except Exception:
            pass

    def set_language(self, language: str) -> bool:
        if language in self.SUPPORTED_LANGUAGES:
            self.current_language = language
            self._save_language_preference()
            return True
        return False

    def get_language(self) -> str:
        return self.current_language

    def t(self, key: str, **kwargs) -> str:
        text = self.TRANSLATIONS.get(self.current_language, self.TRANSLATIONS['en']).get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, ValueError):
                pass
        return text

    def __call__(self, key: str, **kwargs) -> str:
        return self.t(key, **kwargs)


_i18n = I18n()

def get_i18n() -> I18n:
    return _i18n

def t(key: str, **kwargs) -> str:
    return _i18n.t(key, **kwargs)

def set_language(language: str):
    return _i18n.set_language(language)

def get_current_language() -> str:
    return _i18n.get_language()
