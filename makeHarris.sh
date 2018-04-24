#!/bin/bash

./testFormat.sh loci.sql > /dev/null

tail loci.sql.output -n +4 > loci.psv

python3 harris.py

parallel "dot -Tpdf {} > pdf/{/.}.pdf; echo {}" ::: gv/*.gv
# parallel "neato -Tpdf {} > {.}neato.pdf; echo {}" ::: *.gv
# parallel "twopi -Tpdf {} > {.}twopi.pdf; echo {}" ::: *.gv
# parallel "circo -Tpdf {} > {.}circo.pdf; echo {}" ::: *.gv
# parallel "fdp -Tpdf {} > {.}fdp.pdf; echo {}" ::: *.gv
# parallel "sfdp -Tpdf {} > {.}sfdp.pdf; echo {}" ::: *.gv
# parallel "patchwork -Tpdf {} > {.}patchwork.pdf; echo {}" ::: *.gv
# parallel "osage -Tpdf {} > {.}osage.pdf; echo {}" ::: *.gv




