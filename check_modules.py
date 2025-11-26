"""
Module Health Check Script
Checks all modules for import errors and common issues
"""
import sys
import importlib
from pathlib import Path

def check_module(module_name):
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        return True, None
    except Exception as e:
        return False, str(e)

def main():
    print("\n" + "="*60)
    print("MODULE HEALTH CHECK")
    print("="*60 + "\n")

    # List of all modules to check
    modules_to_check = [
        # Core app modules
        "app.services.file_search",
        "app.services.backup",
        "app.schemas.backup",

        # GUI modules
        "gui.components",
        "gui.styles",
        "gui.i18n",
        "gui.search_tab_i18n",
        "gui.backup_tab_i18n",
        "gui.consolidate_tab_i18n",
        "gui.organizer_tab_i18n",
        "gui.duplicate_finder_tab_i18n",
        "gui.restore_tab_i18n",

        # Locales
        "gui.locales.en",
        "gui.locales.vi",
    ]

    passed = 0
    failed = 0
    errors = []

    for module_name in modules_to_check:
        success, error = check_module(module_name)

        if success:
            print(f"[OK]   {module_name}")
            passed += 1
        else:
            print(f"[FAIL] {module_name}")
            print(f"       Error: {error[:100]}")
            failed += 1
            errors.append((module_name, error))

    # Summary
    print("\n" + "="*60)
    print(f"SUMMARY: {passed} passed, {failed} failed")
    print("="*60)

    if errors:
        print("\nERRORS FOUND:\n")
        for module_name, error in errors:
            print(f"Module: {module_name}")
            print(f"Error: {error}")
            print("-" * 60)
    else:
        print("\nAll modules imported successfully!")

    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
