let s:darwin = has('mac')

set nocompatible

call plug#begin()

  Plug 'ConradIrwin/vim-bracketed-paste'
  Plug 'Glench/Vim-Jinja2-Syntax'
  Plug 'airblade/vim-gitgutter'
  Plug 'bling/vim-airline'
  Plug 'fholgado/minibufexpl.vim'
  Plug 'junegunn/fzf',           {'do': 'yes \| ./install'}
  Plug 'junegunn/goyo.vim',      {'on': 'Goyo'}
  Plug 'junegunn/limelight.vim', {'on':  'Limelight'}
  Plug 'junegunn/rainbow_parentheses.vim'
  Plug 'junegunn/seoul256.vim'
  Plug 'navicore/vissort.vim'
  Plug 'schlueter/zsh-ft.vim'
  Plug 'tpope/vim-commentary', {'on': '<Plug>Commentary'}
  Plug 'tpope/vim-endwise'
  Plug 'tpope/vim-fugitive'
  Plug 'tpope/vim-git'
  Plug 'tpope/vim-repeat'
  Plug 'tpope/vim-surround'
  Plug 'tpope/vim-tbone'
  Plug 'vim-scripts/ReplaceWithRegister'

  if s:darwin
    Plug 'zerowidth/vim-copy-as-rtf', {'on': 'CopyRTF'}
    Plug 'junegunn/vim-xmark'
  endif

  if v:version >= 703
    Plug 'junegunn/vim-after-object'
  endif

call plug#end()

filetype plugin on
filetype plugin indent on

set laststatus=2
set wrap
set visualbell noerrorbells
set history=1000 undolevels=1000
set hidden
set hlsearch incsearch showmatch
set backupdir=~/.vim/tmp,. noswapfile
set pastetoggle=<F3>
set clipboard=unnamed

"Set command and input cursors
let &t_SI = "\<Esc>Ptmux;\<Esc>\<Esc>]50;CursorShape=1\x7\<Esc>\\"
let &t_EI = "\<Esc>Ptmux;\<Esc>\<Esc>]50;CursorShape=0\x7\<Esc>\\"

" Easy window handling
map <C-h> <C-w>h
map <C-j> <C-w>j
map <C-k> <C-w>k
map <C-l> <C-w>l
map <C-s> <C-w>s

" Diff of current state and current saved state
map <F2> :w !diff '%' -<CR>

" Sudo save
cmap w!! w !sudo tee % >/dev/null

",/ turns off search highlighting
nmap <silent> ,/ :nohlsearch<CR>

" Search for word under cursor
vnoremap // y/<C-R>"<CR>

" Remove trailing whitespace
autocmd BufWritePre * :%s/\s\+$//e

" Html linting
vmap ,x :%!tidy -q -i --show-errors 0<CR>

" Always change working dir to current file dir
autocmd BufEnter * silent! lcd %:p:h

" mouse
silent! set ttymouse=xterm2
set mouse=a

" 80 chars/line
set textwidth=0
if exists('&colorcolumn')
  set colorcolumn=80
endif

" Line number management
au FocusLost * :set number
autocmd InsertEnter * :set number
if exists('&relativenumber')
  au FocusGained * :set relativenumber
  autocmd InsertLeave * :set relativenumber
endif

" Spaces, not tabs
set expandtab tabstop=4 shiftwidth=4

" Make modelines work
set modelines=10

" Display Whitespace
set listchars=eol:$,tab:>-,trail:~,extends:>,precedes:<,nbsp:%

" Because typos
cmap W :w

" Let's not
cmap bd :q

" MiniBufExplorer shortcuts
nnoremap <Leader>q :MBEToggle<CR>

" Shortcut buffer switching to # \ where # in 1..99
let c = 1
while c <= 99
  execute "nnoremap " . c . "<Leader> :" . c . "b\<CR>"
  let c += 1
endwhile

" Some buffer switching shortcuts
nnoremap <Leader>p :bp<CR>
nnoremap <Leader>n :bn<CR>

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Theme
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
syntax enable
set background=dark
let g:seoul256_background = 236
colo seoul256


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" Airline Theme
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

" let g:airline_left_sep='>'
" let g:airline_right_sep='<'
let g:airline_inactive_collapse=1
let g:airline_powerline_fonts=1
let g:airline_exclude_filenames = ['MiniBufExplorer']


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Limelight
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
let g:limelight_conceal_ctermfg = 'gray'
let g:limelight_conceal_ctermfg = 240
