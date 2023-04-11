from setuptools import setup, find_packages

setup(
    name='CircleBlock',
    version='1.1.0',
    description='Python package for creating circle-themed block diagrams',
    author='phil',
    author_email='eightynine01@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'watchdog',
        'typer',
        'daemonocle'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'ccbk=circleblock.circleblock_cli:app'
        ]
    }
)
# pipenv install -e .
# pipenv run ccbk