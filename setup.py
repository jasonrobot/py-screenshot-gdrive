#!/usr/bin/env python
from distutils.core import setup

setup(name='shoot_up_python',
      version='0.1',
      description='Take screenshots and upload them to Google Drive',
      author='Jason Howell',
      license='gpl2',
      url='https://github.com/jasonrobot/shoot-up-python',
      packages=['shoot_up_python'],
      install_requires=['googleapiclient',
                        'httplib2',
                        'oauthclient2'
                        'pyperclip'])
