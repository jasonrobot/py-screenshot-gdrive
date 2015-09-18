#!/usr/bin/env python
from distutils.core import setup

setup(name='shoot_up_python',
      version='0.1',
      description='Take screenshots and upload them to Google Drive',
      author='Jason Howell',
      license='gpl2',
      url='https://github.com/jasonrobot/shoot-up-python',
      packages=['shoot_up_python'],
      install_requires=['google-api-python-client',
                        'httplib2',
                        'oauth2client',
                        'pyperclip'],
      entry_points={
          'console_scripts' : ['shoot-up-python=shoot_up_python.command_line:main']
      },
      include_package_data=True,
      package_data={
          '': ['client_secret.json', 'settings.cfg']
      })
