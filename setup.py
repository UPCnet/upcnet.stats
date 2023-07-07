# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '1.3'

README = open("README.rst").read()
HISTORY = open(os.path.join("docs", "HISTORY.rst")).read()

setup(name='upcnet.stats',
      version=version,
      description="",
      long_description=README + "\n" + HISTORY,
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='',
      author='UPCnet Plone Team',
      author_email='plone.team@upcnet.es',
      url='https://github.com/upcnet/upcnet.stats',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['upcnet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
