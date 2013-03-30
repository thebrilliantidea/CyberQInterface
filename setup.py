from setuptools import setup, find_packages

try:
    import multiprocessing
except ImportError:
    pass

setup(
    #Package information
    name = "CyberQInterface",
    description = "Package of interface tools for the BBQGuru CyberQ Pit Temperature Controller",
    version = "1.0",
    license = "BSD New",
    url = "https://github.com/thebrilliantidea/CyberQInterface",   
    author = "Bryan Kemp",
    author_email = "bryan@thebrilliantidea.com",
    #scripts = [''],
    
    #Package metadata
    keywords = "cyberq api bbq bbqguru",
    install_requires=['distribute', 'lxml', 'requests'],
    test_suite = "nose.collector",
    tests_require=['nose>=1.0.0', 'mock>=1.0.0', 'coverage'],
    packages = find_packages(),
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        #'': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        #'hello': ['*.msg'],
    },
     # could also include long_description, download_url, classifiers, etc.
    )
