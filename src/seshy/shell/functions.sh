#!/usr/bin/env bash
# seshy tmux window functions
# Source: extracted from ~/.config/tmux/functions.sh

# ============================================
# tmux state retrieval
# ============================================

get_tmux_session() {
    tmux display-message -p '#S' 2>/dev/null
}

get_tmux_window() {
    tmux display-message -p '#W' 2>/dev/null
}

get_tmux_pane() {
    tmux display-message -p '#P' 2>/dev/null
}

get_tmux_panes() {
    local session="${1:-$(get_tmux_session)}"
    local window="${2:-$(get_tmux_window)}"
    [[ -n "$session" && -n "$window" ]] && \
        tmux list-panes -t "${session}:${window}" -F "#{pane_index}" 2>/dev/null
}

# ============================================
# command execution
# ============================================

# win-exec: Execute command in specified tmux pane
#
# Args:
#   $1: command (required)
#   $2: window (optional, defaults to current window)
#   $3: pane (optional, defaults to current pane)
#   $4: session (optional, defaults to current session)
win-exec() {
    local command="${1}"
    local window="${2:-$(get_tmux_window)}"
    local pane="${3:-$(get_tmux_pane)}"
    local session="${4:-$(get_tmux_session)}"

    tmux send-keys -t "${session}:${window}.${pane}" "$command" C-m
}

# ============================================
# base pane commands
# ============================================

pane-nvim() {
    clear && nvim "${1:-.}"
}

pane-git-status() {
    clear && git status
}

pane-lazygit() {
    clear && lazygit
}

pane-lazydocker() {
    clear && lazydocker
}

# ============================================
# window split functions
# ============================================

win-split() {
    local window="${1:-$(get_tmux_window)}"
    local ratio="${2:-50}"
    local orientation="${3:-h}"
    local session="${4:-$(get_tmux_session)}"

    if [[ -n "$session" ]]; then
        tmux select-window -t "$session:$window"
    fi
    tmux split-window -t "$window" -"$orientation" -p "$ratio"
}

win-split-70-30() {
    local window="${1:-$(get_tmux_window)}"
    local session="${2:-$(get_tmux_session)}"

    win-split "$window" 30 h "$window" "$session"
}

# ============================================
# clearing
# ============================================

win-clear() {
    local window="${1:-$(get_tmux_window)}"
    local session="${2:-$(get_tmux_session)}"
    local -a panes
    panes=($(get_tmux_panes "$session" "$window"))

    for pane in "${panes[@]}"; do
        tmux send-keys -t "${session}:${window}.${pane}" 'clear' C-m
    done
}

pane-clear() {
    local window="${1:-}"
    local pane="${2:-}"
    local session="${3:-$(get_tmux_session)}"

    win-exec "clear" "$window" "$pane" "$session"
}

# ============================================
# composite window patterns (used by sesh startup_script)
# ============================================

win-editor-git() {
    local window="${1:-editor}"
    local session="${2:-$(get_tmux_session)}"

    tmux select-window -t "$session":"$window"
    win-split-70-30 "$window" "$session"
    win-exec "pane-nvim" "$window" 1 "$session"
    win-exec "pane-git-status" "$window" 2 "$session"
    tmux select-pane -t "${window}.2"
    pane-clear "$window" 2 "$session"
}

win-split-dual() {
    local window="${1:-dual}"
    local session="${2:-$(get_tmux_session)}"

    win-split "$window" 50 h "$session"
    win-clear "$window" "$session"
}

win-lazygit() {
    local window="${1:-lazygit}"
    local session="${2:-$(get_tmux_session)}"

    tmux select-window -t "$session":"$window"
    win-exec pane-lazygit "$window" "" "$session"
}

win-lazydocker() {
    local window="${1:-lazydocker}"
    local session="${2:-$(get_tmux_session)}"

    tmux select-window -t "$session":"$window"
    win-exec pane-lazydocker "$window" "" "$session"
}
