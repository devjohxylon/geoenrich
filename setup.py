from setuptools import setup, find_packages

setup(
    name="geoenrich",
    version="0.1.0",
    author="John Lohse",
    author_email="your.email@example.com",
    url="https://github.com/devjohxylon/geoenrich",
    description="CLI to enrich CSVs of IPs or coords with geo data",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=["pandas","requests","python-dotenv"],
    entry_points={"console_scripts": ["geoenrich=geoenrich:main"]},
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
