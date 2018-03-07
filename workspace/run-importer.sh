#! /usr/bin/bash

# rm ~/.local/babel/*sqlite
pushd ~/.local/babel
rm document-database.sqlite
rm -rf whoosh-database
popd

# profile='-m cProfile -o profile.bin -s cumulative'
profile=''

command="python ${profile} ../bin/babel-console --user-script ../user-scripts/import-pdf.py"

ged_path='/home/fabrice/home/ged/mode-emploi-appareils'

$command --user-script-args="${ged_path}"
