from setuptools import setup, find_packages

setup(
    name="XestorEventosDAM",
    version="1.0",
    description="Aplicación de gestión de eventos con GTK3 y SQLite",
    author="Tu Nombre",
    # Buscamos paquetes DENTRO de la carpeta 'src'
    packages=find_packages(where='src'),
    # Le decimos que la raíz de esos paquetes es la carpeta 'src'
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'PyGObject',
    ],
    entry_points={
        'console_scripts': [
            'gestor-eventos=main:main',
        ],
    },
)