#!/usr/bin/env bash

deepdive redo articles

deepdive redo parts
deepdive redo chapters
deepdive redo sections
deepdive redo laws
deepdive redo items
deepdive redo points
# 
deepdive redo header_doc
deepdive redo law_has_modification
deepdive redo type_modify_law_0
deepdive redo type_modify_law_1
deepdive redo type_modify_law_2
deepdive redo type_modify_law
deepdive redo extract_modify
deepdive redo link_modify_articles
deepdive redo index_modify_positions

cd udf/AutoPhrase/
rm -r results
bash auto_phrase.sh
cd ../../
deepdive redo phrases
deepdive redo content_phrases
deepdive redo sentences

# deepdive redo legal_penalty_mention
# deepdive redo name_crime_mention
# deepdive redo crime_mention

deepdive redo definition_mention
deepdive redo definition_features
deepdive redo definition_label__0
deepdive redo definition_label
deepdive redo has_definition
deepdive redo probabilities
deepdive redo calibration-plots
