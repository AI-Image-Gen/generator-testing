rm -rf ../img/old
mkdir -p ../img/old
mv ../img/* ../img/old/

git config --global user.name cleanup
git config --global user.email github-actions@github.com
git add .
git commit -m "Daily cleanup"