import sys

from setuptools import find_packages, setup


readme = open('README.md', encoding='utf-8') if sys.version_info[0] == 3 else open('README.md')

setup_dict = dict(
    name='yustina',
    version='1.0',
    author='Sergey Syrov, Alexander Akimov',
    author_email='sergelab@gmail.com',
    description='Yustina flask project',
    long_description=readme.read(),
    install_requires=['Flask'],
    packages=find_packages('src'),
    package_dir={'': 'src'}
)

if __name__ == '__main__':
    setup(**setup_dict)
