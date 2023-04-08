from setuptools import setup, find_packages

setup(
    name='CircleBlock',
    version='1.0.0',
    description='Python package for creating circle-themed block diagrams',
    author='phil',
    author_email='eightynine01@gmail.com',
    packages=find_packages(),
    install_requires=[
        'loguru==0.6.0',
        'watchdog==3.0.0'
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
    ],
    python_requires='>=3.6'
)
