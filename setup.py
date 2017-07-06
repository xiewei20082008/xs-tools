 
from setuptools import setup

setup(name='xs-tools',
      version='0.1.0',
      packages=['changelog','pinGenerator'],
      install_requires = ['gooey','wget','subprocess32'],
      entry_points={
          'console_scripts': [
              'changelog = changelog.main:main',
			  'xsbuild = pinGenerator.main:main'
          ]
      },
      author = "Wei Xie",
      author_email = 'xiewei.fire@gmail.com'
)