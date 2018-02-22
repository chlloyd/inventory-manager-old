# Git Cheat Sheet

### Create


- `git clone <url>` - Clone a remote git repository
- `git init` - Create a new local git repository


### Local Changes 


- `git status` - See changed files as well as untracked files
- `git diff` - See the difference between previous commit and current directory
- `git add <file>` - Add a file to staging area (be tracked by git) or add changes to a file to staging area
- `git commit -m "{message}"` - Create a snapshot of the current directory to be stored into git
- `git rm <file>` - Tell git to delete a file in the repository. Wont delete the file but git will stop tracking the file`

### Commit History


- `git log --graph` - View a graph of the previous commits and branches`


### Branches


- `git branch` - Lists all the branches
- `git branch -av` - Lists all branches including remote branches
- `git checkout <branch>` - Change to a different branch
- `git branch -d <branch>` - Delete a local branch
- `git branch -dr <remote/branch>` - Delete a remote branch

### Remote Repository

- `git pull <remote> <branch>` - Download changes (and move HEAD pointer). Specifying remote and brancha are optional but recommended
- `git push <remote> <branch>` - Push local changes. Specifying remote and brancha are optional but recommended.

### Undo

- `git reset --hard HEAD` - Discard all local changes in the working directory
- `git checkout HEAD <file>` - Discard changes in a specific file.



Conventions

- Commit regularly




### Installation

- Make sure python is installed and in PATH. You'll also need yarn

    $ pip install virtualenv
    $ git clone https://github.com/terimater2/Inventory-Manager.git
    $ cd Inventory-Manager
    $ virtualenv venv

- On linux

    $ source venv/bin/activate

- On Windows

    $ venv/Scripts/activate.bat

    (venv) $ pip install -r requirements.txt

    yarn install --modules-folder=./inventorymanager/static/
