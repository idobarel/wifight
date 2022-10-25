from setuptools import setup, find_packages


VERSION = '0.0.1'
DESCRIPTION = 'WIFIGHT will let you crack a WPA wifi network.'
LONG_DESCRIPTION = 'written in python3, WIFIGHT will let you crack a WPA wifi network.'

setup(
    name="wifightpy",
    version=VERSION,
    author="Ido Barel",
    author_email="<vikbarel5@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "WPA", "cyber", "cracking", "networking", "cyber"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ]
)