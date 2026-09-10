#!/usr/bin/env bash
# UserPromptSubmit hook: inject the checklist for the active output style.
#
# Hooks do not receive the active output style, so read it from the settings
# files in Claude Code's precedence order (the first file that sets it wins).
# /config saves a style change to the project's settings.local.json, so a
# switch mid-session is seen on the next prompt. A style passed with
# `claude --settings` is not visible here.
#
# Style "<Name>" maps to <name>-reminder.txt next to this script. A style
# with no reminder file injects nothing.

input=$(cat)
project_dir=${CLAUDE_PROJECT_DIR:-$(jq -r '.cwd // empty' <<<"$input" 2>/dev/null)}
project_dir=${project_dir:-$PWD}
config_dir=${CLAUDE_CONFIG_DIR:-$HOME/.claude}

style=""
for f in /etc/claude-code/managed-settings.json \
         "$project_dir/.claude/settings.local.json" \
         "$project_dir/.claude/settings.json" \
         "$config_dir/settings.json"; do
  [ -r "$f" ] || continue
  style=$(jq -r '.outputStyle // empty' "$f" 2>/dev/null)
  [ -n "$style" ] && break
done

[[ $style =~ ^[A-Za-z0-9_-]+$ ]] || exit 0
reminder="$(dirname "$0")/${style,,}-reminder.txt"
[ -r "$reminder" ] || exit 0

jq -Rs '{hookSpecificOutput:{hookEventName:"UserPromptSubmit",additionalContext:.},suppressOutput:true}' < "$reminder"
