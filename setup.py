from setuptools import setup, find_packages

setup(
  name='c2m2-assessment',
  version='0.0.1',
  url='https://github.com/nih-cfde/c2m2-assessment',
  author='Daniel J. B. Clarke',
  author_email='danieljbclarkemssm@gmail.com',
  long_description=open('README.md', 'r').read(),
  install_requires=list(map(str.strip, open('requirements.txt', 'r').readlines())),
  packages=find_packages(),
  entry_points={
    'console_scripts': ['c2m2-assessment=c2m2_assessment.__main__:cli'],
  }
)