# Schlueter's dotfiles

The dotfiles I use to make my life easier.

## Installation

#### tl;dr: 

    cd /path/that/isnt/~
    git clone git@github.com:schlueter/dotfiles
    cd dotfiles
    echo '*' >> .git/info/exclude
    git config core.worktree ~

#### Some explanation

Because of how config files do (and should) work, neither symlinks nor hardlinks can be used to install all of these files. The lazy, bad way to do it would be to just copy the files into place, but then they aren't in version control. The solution is to clone this repo to a subdirectory of ~ and then set the git worktree to the home directory with `git config core.worktree ~`. This may seem like voodoo black magic at first, and it leaves behind a directory for the repo containing only a *.git* dir, but it works like a charm. Once that's done, everything in ~ will need to be ignored, but that's easy with a `echo '*' >> .git/info/exclude` in the cloned directory. 

## Files

### .zshrc

My [zsh](http://www.zsh.org/) config file, which has a number of dependencies to be used as is.
