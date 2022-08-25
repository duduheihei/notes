## Git global setup
```
git config --global user.name "name"
git config --global user.email "xxxx@xxx.com.cn"
```

## Create a new repository
```
git clone git@devgit.xxx.com.cn:xxxx/3d-resnets.git
cd 3d-resnets
touch README.md
git add README.md
git commit -m "add README"
git push -u origin master
```

## Push an existing folder
```
cd existing_folder
git init
git remote add origin git@devgit.xxx.com.cn:xxx/3d-resnets.git
git add .
git commit -m "Initial commit"
git push -u origin master
```

## Push an existing Git repository
```
cd existing_repo
git remote rename origin old-origin
git remote add origin git@devgit.xxx.com.cn:xxx/3d-resnets.git
git push -u origin --all
git push -u origin --tags
```