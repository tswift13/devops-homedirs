if [[ -s "${ZDOTDIR:-$HOME}/.zprezto/init.zsh" ]]
then
    source "${ZDOTDIR:-$HOME}/.zprezto/init.zsh"
fi

[[ "$OSTYPE" == darwin* ]] && export BROWSER='open'

export EDITOR='vim'
export VISUAL='vim'
export PAGER='less'

[[ -z "$LANG" ]] && export LANG='en_US.UTF-8'

# Ensure path arrays do not contain duplicates.
typeset -gU cdpath fpath mailpath path

# Set the the list of directories that cd searches.
# cdpath=(
#   $cdpath
# )

# Set the list of directories that Zsh searches for programs.
path=(
  $HOME/bin
  /opt/chefdk/bin
  /Applications/Postgres.app/Contents/Versions/9.4/bin
  $(brew --prefix coreutils)/libexec/gnubin
  /usr/local/{bin,sbin}
  $path
)

export CLASSPATH=$HOME/workspace/libs

# Set the default Less options.
# Mouse-wheel scrolling has been disabled by -X (disable screen clearing).
# Remove -X and -F (exit if the content fits on one screen) to enable it.
export LESS='-F -g -i -M -R -S -w -X -z-4'

# Set the Less input preprocessor.
# Try both `lesspipe` and `lesspipe.sh` as either might exist on a system.
if (( $#commands[(i)lesspipe(|.sh)] ))
then
  export LESSOPEN="| /usr/bin/env $commands[(i)lesspipe(|.sh)] %s 2>&-"
fi

#
# Temporary Files
#

if [[ ! -d "$TMPDIR" ]]
then
  export TMPDIR="/tmp/$LOGNAME"
  mkdir -p -m 700 "$TMPDIR"
fi

TMPPREFIX="${TMPDIR%/}/zsh"

touch ~/.todo && cat ~/.todo

unsetopt CORRECT

############################################################
# Custom stuff
############################################################
touch ~/.aliases && source ~/.aliases
touch  ~/.secrets && source ~/.secrets

export R29=~/workspace/r29

############################################################
# Third party stuff
############################################################
[[ -d /usr/local/opt/autoenv ]] && source /usr/local/opt/autoenv/activate.sh

touch ~/.git-completion && source ~/.git-completion

[ -f /Users/blue/.travis/travis.sh ] && source /Users/blue/.travis/travis.sh

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

which pyenv > /dev/null && eval "$(pyenv init -)"

export PYTHONSTARTUP=~/.pythonrc

fpath=(/usr/local/share/zsh-completions $fpath)
