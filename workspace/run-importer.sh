#! /usr/bin/bash

clear

test_dir='workspace/local-for-test'
# rm -rf ${test_dir}
# mkdir -f ${test_dir}
pushd ${test_dir}
rm document-database.sqlite
rm -rf whoosh-database
popd

# profile='-m cProfile -o profile.bin -s cumulative'
profile=''

python ${profile} ./bin/babel-console --config ${test_dir}/config.py index
