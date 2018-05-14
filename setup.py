# Copyright (c) 2018, Matt Layman and contributors
"""
tappy is a set of tools for working with the `Test Anything Protocol (TAP)
<http://testanything.org/>`_, a line based test protocol for recording test
data in a standard way.

Follow tappy development on `GitHub <https://github.com/python-tap/tappy>`_.
Developer documentation is on
`Read the Docs <https://tappy.readthedocs.io/>`_.
"""

from setuptools import find_packages, setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist

import tap


class BuildPy(build_py):
    """Custom ``build_py`` command to always build mo files for wheels."""

    def run(self):
        self.run_command('compile_catalog')
        # build_py is an old style class so super cannot be used.
        build_py.run(self)


class Sdist(sdist):
    """Custom ``sdist`` command to ensure that mo files are always created."""

    def run(self):
        self.run_command('compile_catalog')
        # sdist is an old style class so super cannot be used.
        sdist.run(self)


# The docs import setup.py for the version so only call setup when not behaving
# as a module.
if __name__ == '__main__':
    with open('docs/releases.rst', 'r') as f:
        releases = f.read()

    long_description = __doc__ + '\n\n' + releases

    setup(
        name='tap.py',
        version=tap.__version__,
        url='https://github.com/python-tap/tappy',
        license='BSD',
        author='Matt Layman',
        author_email='matthewlayman@gmail.com',
        description='Test Anything Protocol (TAP) tools',
        long_description=long_description,
        packages=find_packages(),
        entry_points={
            'console_scripts': [
                'tappy = tap.main:main',
                'tap = tap.main:main',
            ],
        },
        include_package_data=True,
        zip_safe=False,
        platforms='any',
        install_requires=[],
        extras_require={
            'yaml': [
                'more-itertools',
                'PyYAML',
            ],
        },
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
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
