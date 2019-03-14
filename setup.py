import sys

from setuptools import setup
from setuptools import find_packages

requirements = ['requests']
if sys.version_info < (2, 7):
    requirements.append('argparse')

setup(name='huntertray',
      version='0.0.2',
      description='ProductHunt in your System Tray',
      long_description='ProductHunt in your System Tray inspired by HackerTray',
      keywords='ProductHunt PH tray system tray icon huntertray',
      url='https://github.com/artiya4u/huntertray',
      author='Artiya Thinkumpang',
      author_email='artiya4u@gmail.com',
      license='MIT',
      packages=find_packages(),
      package_data={
          'huntertray.data': ['hunter-tray.png']
      },
      install_requires=[
          'requests>=2.2.1'
      ],
      entry_points={
          'console_scripts': ['huntertray = huntertray:main'],
      },
      zip_safe=False)
