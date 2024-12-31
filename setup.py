from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': ['telebot']}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('main.py', base=base)
]

setup(name='Clube dos Investidores[Grupo Gratuito]',
      version = '0.1',
      description = 'Sample Project for Testing',
      options = {'build_exe': build_options},
      executables = executables)

