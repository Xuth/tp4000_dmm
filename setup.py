import os.path
from setuptools import setup, find_packages


from fs9721 import __version__


requirements_path = os.path.join(
    os.path.dirname(__file__),
    'requirements.txt',
)
try:
    from pip.req import parse_requirements
    requirements = [
        str(req.req) for req in parse_requirements(requirements_path)
    ]
except ImportError:
    requirements = []
    with open(requirements_path, 'r') as in_:
        requirements = [
            req for req in in_.readlines()
            if not req.startswith('-')
            and not req.startswith('#')
        ]


setup(
    name='fs9721',
    version=__version__,
    url='http://github.com/coddingtonbear/python-fs9721/',
    description='',
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: System :: Hardware',
        'Topic :: System :: Hardware :: Hardware Drivers',
    ],
    include_package_data=True,
    install_requires=requirements,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'fs9721 = fs9721.cmdline:main'
        ]
    },
)
