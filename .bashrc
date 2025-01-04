# awesome fuzzy finding
# completions
eval "$(fzf --bash)"

# initialize zoxide (cd alternative)
eval "$(zoxide init bash)"

# eza setup
alias l='eza --color=always -1 -l -a --git --git-repos --group-directories-first --icons'
alias l.="eza -a | grep -E '^\.'"

export FZF_DEFAULT_OPTS="--preview='bat --style=numbers --line-range :500 --color=always {}' --bind=down:preview-down --bind=up:preview-up"
