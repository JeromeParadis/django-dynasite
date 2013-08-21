from distutils.core import setup

setup(
    name="django-dynasite",
    version=__import__("dynasite").__version__,
    description="Tools to dynamically manage multiple Django Web sites in a single app the way you need to.",
    long_description=open("docs/usage.txt").read(),
    author="Jerome Paradis",
    author_email="jparadis@paradivision.com",
    url="http://github.com/JeromeParadis/django-dynasite",
    license='LICENSE.txt',
    packages=[
        "dynasite",
    ],
    package_dir={"dynasite": "dynasite"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    install_requires=[
        "Django >= 1.4.1",
    ],
    package_data={'dynasite': [] },
)
