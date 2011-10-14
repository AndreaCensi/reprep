
options="$options --with-id"
# options="$options --trim-errors"
options="--with-coverage --cover-html --cover-html-dir coverage_information --cover-package=reprep"

nosetests $options  $*
