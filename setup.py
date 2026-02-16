from setuptools import setup, find_packages

setup(
    name="XestorEventos",
    version="1.0",
    description="Aplicación de xestión de eventos con GTK3 e SQLite",
    author="Adrián",
    packages=find_packages(),
    install_requires=[
        'PyGObject',
    ],
    entry_points={
        'console_scripts': [
            'xestor-eventos=src.main:main',
        ],
    },
)