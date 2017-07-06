 
from setuptools import setup

setup(name='xs-tools',
      version='0.1.0',
      packages=['changelog','pin-generator'],
      entry_points={
          'console_scripts': [
              'changelog = changelog.main:main',
              'xsbuild = pin-generator.main:main'
          ],
      },
      install_requires = ['gooey','wget','subprocess32'],  
      author = "Wei Xie",
      author_email = 'xiewei.fire@gmail.com'
)