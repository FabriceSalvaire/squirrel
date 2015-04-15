####################################################################################################

rm ~/.local/babel/*sqlite

profile='-m cProfile -o profile.bin -s cumulative'
command="python $profile ../bin/babel-console --user-script ../user-scripts/import-pdf.py"

# $command --user-script-args="pdf-pool"

# Fixme: realpath
$command --user-script-args="/home/gv/fabrice/ged/racine"

####################################################################################################
# 
# End
# 
####################################################################################################
