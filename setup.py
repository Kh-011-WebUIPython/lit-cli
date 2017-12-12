"""
MIT License

Copyright (c) 2017 SoftServe Academy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import codecs
import os
import sys

from shutil import rmtree
from setuptools import setup, find_packages, Command

if sys.version_info[0] == 2:
    sys.exit('Sorry, Python < 3 is not supported')

if sys.version_info[0] == 3 and sys.version_info[1] < 5:
    sys.exit('Sorry, Python < 3.5 is not supported')

here = os.path.abspath(os.path.dirname(__file__))

NAME = 'litvcs'
DESCRIPTION = 'The project “LIT” is a version control system.'
URL = 'https://github.com/Kh-011-WebUIPython/lit-cli'
EMAIL = 'maxkrivich@gmail.com'
AUTHOR = 'Maxim Krivich'

ABOUT = {}
with open(os.path.join(here, 'lit', '__version__.py')) as f:
    exec(f.read(), ABOUT)

readme_file = os.path.join(here, 'README.md')
try:
    # Use python-3 to publish new version on PyPI
    from m2r import parse_from_file

    LONG_DESCRIPTION = parse_from_file(readme_file)
except (ImportError, UnicodeDecodeError):
    with codecs.open(readme_file, encoding='utf-8') as f:
        LONG_DESCRIPTION = f.read()

with codecs.open(os.path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    REQUIREMENTS = f.read().splitlines()

if sys.platform not in ('linux', 'linux2'):
    sys.exit('Sorry, litvcs is not supported %s ' % sys.platform)


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.sep.join(('.', 'dist')))
        except:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name=NAME,
    version=ABOUT['__version__'],
    url=URL,
    license='MIT',
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=REQUIREMENTS,
    packages=['lit','lit.file', 'lit.diff', 'lit.command'],#find_packages(exclude=('tests',)),
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'lit = lit.cli:main',
        ],
    },
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
        # 'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    cmdclass={
        'publish': PublishCommand,
    }
)
