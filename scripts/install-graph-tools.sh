#!/usr/bin/env bash
# Check and install the graph tools for dev-kit (rule G1).
#   --check    (default) print status; exit 0 if both are present, 1 if any is missing
#   --install  install the missing tools at pinned versions; a tool that is already present is left alone
# dk:init asks the user first, then calls --install. It never runs
# `codegraph install` / `code-review-graph install` (they register MCP, hooks, instruction files).
set -euo pipefail

CODEGRAPH_PIN="v1.5.0"
CRG_PIN="2.3.9"
CODEGRAPH_INSTALLER="https://raw.githubusercontent.com/colbymchenry/codegraph/${CODEGRAPH_PIN}/install.sh"

mode="${1:---check}"

version_of() { "$1" --version 2>/dev/null | head -1 || true; }

# Locate a tool: on PATH first, then the default install dirs (a fresh machine may not have ~/.local/bin on PATH)
locate() {
  local name=$1 dir
  if command -v "$name" >/dev/null 2>&1; then command -v "$name"; return 0; fi
  for dir in "${CODEGRAPH_BIN_DIR:-}" "${PIPX_BIN_DIR:-}" "$HOME/.local/bin"; do
    [ -n "$dir" ] && [ -x "$dir/$name" ] && { echo "$dir/$name"; return 0; }
  done
  return 1
}

status() {
  local missing=0 name path
  for name in codegraph code-review-graph; do
    if path=$(locate "$name"); then
      if command -v "$name" >/dev/null 2>&1; then
        echo "$name: $(version_of "$path") ($path)"
      else
        echo "$name: $(version_of "$path") ($path) NOT on PATH — call it by this absolute path, or add: export PATH=\"$(dirname "$path"):\$PATH\""
      fi
    else
      echo "$name: missing"; missing=1
    fi
  done
  return $missing
}

install_codegraph() {
  command -v curl >/dev/null 2>&1 || { echo "need curl to install codegraph" >&2; return 1; }
  echo "Installing codegraph ${CODEGRAPH_PIN} via ${CODEGRAPH_INSTALLER}"
  # install.sh honors CODEGRAPH_INSTALL_DIR / CODEGRAPH_BIN_DIR when set
  curl -fsSL "$CODEGRAPH_INSTALLER" | CODEGRAPH_VERSION="$CODEGRAPH_PIN" sh
}

install_crg() {
  if command -v pipx >/dev/null 2>&1; then
    echo "Installing code-review-graph ${CRG_PIN} via pipx"
    pipx install "code-review-graph==${CRG_PIN}"
  elif command -v uv >/dev/null 2>&1; then
    echo "Installing code-review-graph ${CRG_PIN} via uv tool"
    uv tool install "code-review-graph==${CRG_PIN}"
  else
    echo "need pipx or uv to install code-review-graph (e.g. 'brew install pipx')" >&2
    return 1
  fi
}

case "$mode" in
  --check)
    status
    ;;
  --install)
    locate codegraph >/dev/null || install_codegraph
    locate code-review-graph >/dev/null || install_crg
    hash -r
    status
    ;;
  *)
    echo "usage: $0 [--check|--install]" >&2
    exit 2
    ;;
esac
