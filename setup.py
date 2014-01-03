from setuptools import setup, find_packages

scripts = [
    ('reprep_demos', 'reprep.demos.manager'),
]

# this is the format for setuptools
console_scripts = map(lambda s: '%s = %s:main' % (s[0], s[1]), scripts)

package_data = {'':['*.*']}

version = '2.3dev1'

setup(name='reprep',
      version=version,
      package_dir={'':'src'},
      packages=find_packages('src'),
      install_requires=[
            'docutils',
            'PyContracts>=1.2,<2',
      ],
      package_data=package_data,
      url='http://AndreaCensi.github.com/reprep/',
      author='Andrea Censi',
      author_email='censi@mit.edu',
      license="LGPL",
      keywords="report reproducible research tables html latex",
      download_url='http://github.com/AndreaCensi/reprep/tarball/%s' % version,
      entry_points={ 'console_scripts': console_scripts},
)

