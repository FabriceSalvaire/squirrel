#! rm ~/.local/babel/*sqlite

# profile='-m cProfile -o profile.bin -s cumulative'
profile=''
command="python ${profile} ../bin/babel-console --user-script ../user-scripts/import-pdf.py"

ged_path='/home/fabrice/home/ged/mode-emploi-appareils'

# $command --user-script-args="pdf-pool"

# Fixme: realpath
$command --user-script-args="${ged_path}"
