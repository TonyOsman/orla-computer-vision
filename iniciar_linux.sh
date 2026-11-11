#!/usr/bin/env bash
set -e
cd -- "$(dirname -- "$0")"
if [ -x .venv/bin/python ]; then
    exec .venv/bin/python codigo/orla_interacao.py --camera "${1:-0}"
fi
printf '%s\n' 'Ambiente .venv ausente. Siga a instalação no README.md.'
exit 1
