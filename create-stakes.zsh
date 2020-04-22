#!/bin/zsh

#for angle in 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21; do python create-circle-stake.py --radius "1/4 1/4 0/1 1/1" --angle "1/1 1/$angle 1/1" --width 10; done

# With golden ratio
python create-circle-stake.py --radius "1/4 1/4 0/1 1/1" --angle "1/1 1/360 1597/987"
python create-circle-stake.py --radius "1/4 1/4 0/1 1/1" --angle "99/100 1/1 987/1597"