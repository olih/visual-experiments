#!/bin/zsh
VIEW="stake"

# Linear spirales
for ellipse in 1 2 3 4
do
for radius in 100 300 500 700
do
    for angle in 7 9 12 15 31
    do  python create-circle-stake.py --radius "1/4 1/52 -1/$radius 1/1" --angle "$angle/1 1/30 1/1" --width 10 --ellipse "1/$ellipse" --view "$VIEW"
done
done
done

#Circles
for ellipse in 1 2 3 5 7 9
do
for angle in 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 27 33 36
    do python create-circle-stake.py --radius "1/4 1/4 0/1 1/1" --angle "1/1 1/$angle 1/1" --width 10 --ellipse "1/$ellipse" --view "$VIEW"
done
done

#sine decrease amplitude
python create-sine-wave-stake.py --amplitude "1/4 1/16 -1/1400 1/1" --period "7/1 1/30 1/1" --view "$VIEW"
python create-sine-wave-stake.py --amplitude "1/4 1/16 -1/1400 1/1" --period "11/1 1/30 1/1" --view "$VIEW"

#sine wave
for period in 3 5 7 11
do
    python create-sine-wave-stake.py --amplitude "1/4 1/4 0/1 1/1" --period "$period/1 1/30 1/1" --view "$VIEW"
done

# With golden ratio
python create-circle-stake.py --radius "1/4 1/4 0/1 1/1" --angle "1/1 1/360 1597/987" --view "$VIEW"
python create-circle-stake.py --radius "1/4 1/4 0/1 1/1" --angle "99/100 1/1 987/1597" --view "$VIEW"

