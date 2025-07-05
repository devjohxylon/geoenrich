from setuptools import setup, find_packages

setup(
    name="geoenrich",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "python-dotenv",
    ],
    entry_points={
        "console_scripts": [
            "geoenrich=geoenrich:main",
        ],
    },
)
