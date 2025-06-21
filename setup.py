# Setup script for PyPI packaging of Cascade compiler/interpreter

from setuptools import setup, find_packages

setup(
    name='cascade-lang',
    version='0.1.0',
    description='Cascade language compiler/interpreter',
    author='Your Name',
    author_email='you@example.com',
    url='https://github.com/yourname/cascade',
    packages=find_packages(),
    install_requires=[
        "pygls", # Required for LSP server
    ],
    entry_points={
        'console_scripts': [
            'cascade=compiler.cli:main'
        ],
    },
    package_data={
        'compiler': ['*.pegjs', '*.json'],
    },
    include_package_data=True,
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ]
)