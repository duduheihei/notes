1. create a new repository on the command line
   ```shell
    echo "# notes" >> README.md
    git init
    git add README.md
    git commit -m "first commit"
    git branch -M master
    git remote add origin git@github.com:duduheihei/notes.git
    git push -u origin master
   ```
2. push an existing repository from the command line
   ```shell
    git remote add origin git@github.com:duduheihei/notes.git
    git branch -M master
    git push -u origin master
   ```