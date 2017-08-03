#!/bin/bash -xe

unzip -o ../LoanStats3d_securev1.csv.zip -d .
python ../lending_club_clean.py `pwd`/lc-2015-loans.csv
rm LoanStats3d_securev1.csv