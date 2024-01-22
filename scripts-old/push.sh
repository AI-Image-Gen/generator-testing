mkdir -p ../img/prompts
cp ./tmp/*.jpg ../img
cp ./tmp/prompt.txt ./prompt.txt
cp ./prompt.txt ../img/prompts/$RUNNUM-$RUNID.txt

python push.py $CONFIGPATH

rm -rf ./tmp
rm -rf ./prompt.txt

cd ..
git config --global user.name ai
git config --global user.email github-actions@github.com
git add .
git commit -m "Next photos"