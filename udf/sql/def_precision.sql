SELECT mention_id
    , concept_expression
    , explain_text
    , expectation

  FROM has_definition_inference natural join definition_mention

 WHERE  expectation >= 0.6

 ORDER BY random()
 LIMIT 100