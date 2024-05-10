from setuptools import setup, find_packages

setup(
    name='DRAGEN_Launch_Manager',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pyyaml',  # Assuming you're using YAML configurations
        # Add other dependencies here, but remember tkinter might not be available via pip
    ],
    entry_points={
        'console_scripts': [
            'dragen-launcher=src.main:main',  # Assuming your main function is in src/main.py and named main
        ],
    },
    python_requires='>=3.6',
    include_package_data=True,
    zip_safe=False
)