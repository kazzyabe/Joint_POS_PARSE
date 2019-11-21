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

# After the addition of features from MIRA paper
## dev
```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     99.25 |     99.25 |     99.25 |     99.25
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |     99.25 |     99.25 |     99.25 |     99.25
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |     91.12 |     91.12 |     91.12 |     91.12
LAS        |     91.12 |     91.12 |     91.12 |     91.12
```
## train
### learning curve
```
Iter 0: 111515/204585=54.50790624923626

Iter 1: 130117/204585=63.600459466725326

Iter 2: 140982/204585=68.91121049930346

Iter 3: 145988/204585=71.3581152088374

Iter 4: 149333/204585=72.99313243883961

Iter 5: 151418/204585=74.01226873915488

Iter 6: 153436/204585=74.99865581543123

Iter 7: 155814/204585=76.16100887161815

Iter 8: 155916/204585=76.21086589925947

Iter 9: 155844/204585=76.17567270327737
```
### res
```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     98.46 |     98.46 |     98.46 |     98.46
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |     98.46 |     98.46 |     98.46 |     98.46
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |     83.09 |     83.09 |     83.09 |     83.09
LAS        |     83.09 |     83.09 |     83.09 |     83.09
```

# smaller data around 100k
# Japanese 7 iteration UD_Japanese-GSD
## learning curve
```

Iter 0: 113208/160204=70.66490224963172

Iter 1: 126973/160204=79.25707223290304

Iter 2: 132491/160204=82.70143067588825

Iter 3: 135471/160204=84.56155901225937

Iter 4: 137466/160204=85.80684627100446

Iter 5: 137525/160204=85.84367431524807

Iter 6: 139448/160204=87.04401887593318
```
## train
```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     97.13 |     97.13 |     97.13 |     97.13
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |     97.13 |     97.13 |     97.13 |     97.13
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |     90.10 |     90.10 |     90.10 |     90.10
LAS        |     90.10 |     90.10 |     90.10 |     90.10
```

## test
```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     92.00 |     92.00 |     92.00 |     92.00
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |     92.00 |     92.00 |     92.00 |     92.00
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |     76.71 |     76.71 |     76.71 |     76.71
LAS        |     76.71 |     76.71 |     76.71 |     76.71
```

# English
## learning curve
```

Iter 0: 34511/69760=49.471043577981646

Iter 1: 42727/69760=61.248566513761475

Iter 2: 47246/69760=67.72649082568807

Iter 3: 49913/69760=71.5495986238532

Iter 4: 51523/69760=73.8575114678899

Iter 5: 52861/69760=75.77551605504587

Iter 6: 53632/69760=76.88073394495413
```
## train 7 iteration
```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     98.07 |     98.07 |     98.07 |     98.07
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |     98.07 |     98.07 |     98.07 |     98.07
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |     83.26 |     83.26 |     83.26 |     83.26
LAS        |     83.26 |     83.26 |     83.26 |     83.26
```
## test
```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     89.50 |     89.50 |     89.50 |     89.50
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |     89.50 |     89.50 |     89.50 |     89.50
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |     59.83 |     59.83 |     59.83 |     59.83
LAS        |     59.83 |     59.83 |     59.83 |     59.83
```

# Urdu
## learning curve
```
Iter 0: 61810/108690=56.86815714417149

Iter 1: 69404/108690=63.85500046002392

Iter 2: 72503/108690=66.70622872389364

Iter 3: 73881/108690=67.97405465084184

Iter 4: 76001/108690=69.924556076916

Iter 5: 76524/108690=70.40574109853712

Iter 6: 77316/108690=71.13441898978748
```
```
Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     94.13 |     94.13 |     94.13 |     94.13
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |     94.13 |     94.13 |     94.13 |     94.13
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |     76.35 |     76.35 |     76.35 |     76.35
LAS        |     76.35 |     76.35 |     76.35 |     76.35
```

## chinese
```

Iter 0: 33585/98616=34.05633974202969

Iter 1: 44887/98616=45.51695465238906

Iter 2: 50332/98616=51.03837105540683

Iter 3: 53967/98616=54.724385495254324

Iter 4: 56085/98616=56.872110002433686

Iter 5: 57228/98616=58.031151131662206

Iter 6: 58364/98616=59.183094021254156

Metrics    | Precision |    Recall |  F1 Score | AligndAcc
-----------+-----------+-----------+-----------+-----------
Tokens     |    100.00 |    100.00 |    100.00 |
Sentences  |    100.00 |    100.00 |    100.00 |
Words      |    100.00 |    100.00 |    100.00 |
UPOS       |     97.99 |     97.99 |     97.99 |     97.99
XPOS       |    100.00 |    100.00 |    100.00 |    100.00
Feats      |    100.00 |    100.00 |    100.00 |    100.00
AllTags    |     97.99 |     97.99 |     97.99 |     97.99
Lemmas     |    100.00 |    100.00 |    100.00 |    100.00
UAS        |     65.58 |     65.58 |     65.58 |     65.58
LAS        |     65.58 |     65.58 |     65.58 |     65.58
```