from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='falchy',
      version='0.1',
      description=' Core Library for FalchyRest and FalchyAuth projects ',
      long_description=readme(),
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5'
      ],
      keywords='Falcon REST Python3 ',
      url='http://github.com/storborg/funniest',
      author='Morfat Mosoti',
      author_email='morfatmosoti@gmail.com',
      license='MIT',
      packages=['falchy'],
      install_requires=[
          'SQLAlchemy','mysqlclient','serpy','falcon','jwcrypto'
      ],
      include_package_data=True,
      zip_safe=False)