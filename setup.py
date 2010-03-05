from setuptools import setup, find_packages

setup(
    name="DocUtils-plainhtml",
    description="Plain HTML writer for docutils",
    version="0.1",
    license="BSD License",
    author="Alex Morega",
    author_email="public@grep.ro",
    #packages=find_packages(),
    modules=['plain_html_writer.py'],
    install_requires=['docutils'],
    entry_points={
        'console_scripts': [
            'rst2plainhtml = plain_html_writer:main',
        ],
    },
)
