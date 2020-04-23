#!/bin/zsh
VIEW="cartesian"

#sine wave
for period in 3 5 7 11
do
    python create-sine-wave-stake.py --amplitude "1/4 1/4 0/1 1/1" --period "$period/1 1/20 1/1" --view "$VIEW"
done

exit 0

#Circles
for angle in 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21
    do python create-circle-stake.py --radius "1/4 1/4 0/1 1/1" --angle "1/1 1/$angle 1/1" --width 10 --view "$VIEW"
done

# With golden ratio
python create-circle-stake.py --radius "1/4 1/4 0/1 1/1" --angle "1/1 1/360 1597/987" --view "$VIEW"
python create-circle-stake.py --radius "1/4 1/4 0/1 1/1" --angle "99/100 1/1 987/1597" --view "$VIEW"

# Linear spirales
for radius in 100 300 500 700
do
    for angle in 1 3 5 7 9 12 15 31
    do  python create-circle-stake.py --radius "1/4 1/52 -1/$radius 1/1" --angle "$angle/1 1/20 1/1" --width 10 --view "$VIEW"
done
done
