#!/bin/sh

cd ~/Documents/energyDashboard_Bresso/
scp -P 37729 pi@proxy51.yoics.net:~/Documents/energyBuffer.log .
python parser.py
cp *.html ../Bresso_scuola_grafici/
cd ~/Documents/Bresso_scuola_grafici/
git add --all
git commit -m "html daily update"
git push -u origin gh-pages


