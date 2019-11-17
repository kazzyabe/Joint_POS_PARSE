# Joint_POS_PARSE
This is an extenstion of a basic graph-based dependency parser, where the POS tagger and the parser are trained together

# Result
## On dev, 10 iteration
```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     99.26 |     99.26 |     99.26 |     99.26
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |     99.26 |     99.26 |     99.26 |     99.26
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |     85.55 |     85.55 |     85.55 |     85.55
LAS        |     85.55 |     85.55 |     85.55 |     85.55
```