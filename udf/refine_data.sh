#! /usr/bin/env bash
# A shell script that runs Bazaar/Parser over documents passed as input TSV lines
#
# $ deepdive env udf/nlp_markup.sh doc_id _ _ content _
##
set -euo pipefail
cd "$(dirname "$0")"

: ${VN_NLP_HOME:=$PWD/vn-nlp-deepdive}
[[ -x "$VN_NLP_HOME" ]] || {
    echo "No Bazaar set up at: $VN_NLP_HOME"
    exit 2
} >&2

java -Xmx4g -Dfile.encoding=UTF-8 -cp "$VN_NLP_HOME/build/jar/vn-nlp-deepdive-0.1.jar:$VN_NLP_HOME/lib/*" com.hust.bientuananh.vnnlp.App -refine $@