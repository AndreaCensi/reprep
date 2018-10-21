from setuptools import setup, find_packages


def get_version(filename):
    import ast
    version = None
    with open(filename) as f:
        for line in f:
            if line.startswith('__version__'):
                version = ast.parse(line).body[0].value.s
                break
        else:
            raise ValueError('No version found in %r.' % filename)
    if version is None:
        raise ValueError(filename)
    return version


version = get_version('src/reprep/__init__.py')

scripts = [
    ('reprep_demos', 'reprep.demos.manager'),
]

# this is the format for setuptools
console_scripts = map(lambda s: '%s = %s:main' % (s[0], s[1]), scripts)

package_data = {'': ['*.*']}

setup(name='reprep',
      version=version,
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      install_requires=[
          'docutils',
          'PyContracts>=1.8.5',
          'numpy',
          'Pillow',
          'matplotlib',
          'six',
      ],
      package_data=package_data,
      url='http://AndreaCensi.github.com/reprep/',
      author='Andrea Censi',
      description='Reproducible Reports',
      author_email='censi@mit.edu',
      license="LGPL",
      keywords="report reproducible research tables html latex",
      download_url='http://github.com/AndreaCensi/reprep/tarball/%s' % version,
      entry_points={'console_scripts': console_scripts},
      zip_safe=False,  # because of resources
      )
