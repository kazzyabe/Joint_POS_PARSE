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
## on train, 10 iteration
```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     98.63 |     98.63 |     98.63 |     98.63
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |     98.63 |     98.63 |     98.63 |     98.63
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |     79.38 |     79.38 |     79.38 |     79.38
LAS        |     79.38 |     79.38 |     79.38 |     79.38
```
## on test
```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     93.09 |     93.09 |     93.09 |     93.09
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |     93.09 |     93.09 |     93.09 |     93.09
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |     64.58 |     64.58 |     64.58 |     64.58
LAS        |     64.58 |     64.58 |     64.58 |     64.58
```