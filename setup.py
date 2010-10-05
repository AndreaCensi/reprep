from setuptools import setup, find_packages

setup(name='reprep',
      version='0.9',
      package_dir={'':'src'},
      packages=find_packages(),
      install_requires=['numpy'],
      package_data={'': ['*.js','*.gif','*.jpg','*.cur','*.css']},
      url='http://AndreaCensi.github.com/reprep/',
      author='Andrea Censi',
      author_email='andrea@cds.caltech.edu',
      license="LGPL",
      keywords="report reproducible research tables html latex",
)

