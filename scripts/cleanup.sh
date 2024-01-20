rm -rf ../img/old
mkdir -p ../img/old/prompts
mv ../img/*.img ../img/old/
mv ../img/prompts/* ../img/old/prompts/

cd ..
git config --global user.name cleanup
git config --global user.email github-actions@github.com
git add .
git commit -m "Daily cleanup"