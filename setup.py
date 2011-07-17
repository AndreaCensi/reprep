from setuptools import setup, find_packages

#'*.js', '*.gif', '*.jpg', '*.cur', '*.css'
#package_data = {'reprep': ['static/PopBox/*']}

#package_data = {'': ['*.js']}
package_data = {'':['*.*']}

setup(name='reprep',
      version='0.10.0',
      package_dir={'':'src'},
      packages=find_packages('src'),
      install_requires=['docutils', 'PyContracts'],
      
      package_data=package_data,
      url='http://AndreaCensi.github.com/reprep/',
      author='Andrea Censi',
      author_email='andrea@cds.caltech.edu',
      license="LGPL",
      keywords="report reproducible research tables html latex",
)

