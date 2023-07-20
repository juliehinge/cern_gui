from setuptools import setup

APP = ['main.py']
DATA_FILES = ['gui_figure1.png', 'p.py', 'page_one.py', 'page_two.py', 'page_three.py', 'page_four.py', 'start_page.py']

OPTIONS = {
    'py2app': {
        'packages': ['tkinter', 'pandas', 'numpy', 'tkscrolledframe','ttkthemes'],
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options=OPTIONS,
    setup_requires=['py2app'],
)
