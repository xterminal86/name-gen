```
usage: name-gen.py [-h] [--seed SEED] [--len LEN] [--mode {0,1,2,3}] [--debug] [--names NAMES] [--relaxed]

optional arguments:
  -h, --help        show this help message and exit
  --seed SEED       Plain text file name with names to build letters distribution from (one per line)
  --len LEN         Maximum name length. Default: 6
  --mode {0,1,2,3}  0 - digraphs, 1 - trigraphs, 2 - digraphs / trigraphs, 3 - trigraphs / digraphs. Default: 0
  --debug           Print distributions (e.g. for subsequent hardcoding).
  --names NAMES     How many names to generate. Default: 10
  --relaxed         Relax generation rules (high rate of shitty names!). Default: off

Modes help:

0 - construct name based on distribution of one subsequent letter.
1 - construct name based on distribution of two subsequent letters.
2 - alternate between mode 0 and 1 on each iteration.
3 - alternate between mode 1 and 0 on each iteration.

Most descent results generate with len [ 5 ; 6 ] for mode 0 and 1.
For modes 2 and 3 len can be increased by 1 or 2 values.
```

```
py name-gen.py --mode=0 --len=7

Bredain
Urcheas
Enninna
Pheanka
Ellorew
Etorrer
Oronnga
Ethifel
Ananyll
Frelied
```
