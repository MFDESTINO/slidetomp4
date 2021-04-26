mkdir tmp
unzip $1 -d tmp
unoconv -f pdf $1
cp -R tmp/ppt/media media
cp -R tmp/ppt/slides/_rels xmlfiles
rm -rf tmp
python main.py $1
rm -rf media
rm -rf xmlfiles

