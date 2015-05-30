# Copyright (c) 2015, Matt Layman
"""
tappy is a set of tools for working with the `Test Anything Protocol (TAP)
<http://testanything.org/>`_, a line based test protocol for recording test
data in a standard way.

Follow tappy development on `GitHub <https://github.com/mblayman/tappy>`_.
Developer documentation is on
`Read the Docs <https://tappy.readthedocs.org/>`_.
"""

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist
import sys

__version__ = '1.6'


class BuildPy(build_py):
    """Custom ``build_py`` command to always build mo files for wheels."""

    def run(self):
        # Babel fails hard on Python 3. Let Python 2 make the mo files.
        if sys.version_info < (3, 0, 0):
            self.run_command('compile_catalog')
        # build_py is an old style class so super cannot be used.
        build_py.run(self)


class Sdist(sdist):
    """Custom ``sdist`` command to ensure that mo files are always created."""

    def run(self):
        self.run_command('compile_catalog')
        # sdist is an old style class so super cannot be used.
        sdist.run(self)


def install_requirements():
    requirements = [
        'nose',
        'Pygments',
    ]
    if sys.version_info < (2, 7, 0):
        requirements.append('argparse')

    return requirements

# The docs import setup.py for the version so only call setup when not behaving
# as a module.
if __name__ == '__main__':
    with open('docs/releases.rst', 'r') as f:
        releases = f.read()

    long_description = __doc__ + '\n\n' + releases

    install_requires = install_requirements()
    # Add some developer tools.
    if 'develop' in sys.argv:
        install_requires.extend([
            'Babel',
            'coverage',
            'flake8',
            'mock',
            'requests',
            'Sphinx',
            'tox',
            'twine',
            'wheel',
        ])

    setup(
        name='tap.py',
        version=__version__,
        url='https://github.com/mblayman/tappy',
        license='BSD',
        author='Matt Layman',
        author_email='matthewlayman@gmail.com',
        description='Test Anything Protocol (TAP) tools',
        long_description=long_description,
        packages=find_packages(),
        entry_points={
            'console_scripts': ['tappy = tap.main:main'],
            'nose.plugins.0.10': ['tap = tap.plugin:TAP'],
            'pygments.lexers': ['tap = tap.lexer:TAPLexer'],
        },
        include_package_data=True,
        zip_safe=False,
        platforms='any',
        install_requires=install_requires,
        setup_requires=[
            'Babel',  # sdist compiles po into mo.
        ],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Topic :: Software Development :: Testing',
        ],
        keywords=[
            'TAP',
            'unittest',
        ],
        cmdclass={
            'build_py': BuildPy,
            'sdist': Sdist,
        },
        test_suite='tap.tests',
        tests_require=[
            'mock'
        ]
    )
