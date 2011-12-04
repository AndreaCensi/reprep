
scripts = [
    ('reprep_demos', 'reprep.demos.manager'),
]


# this is the format for setuptools
console_scripts = map(lambda s: '%s = %s:main' % (s[0], s[1]), scripts)
