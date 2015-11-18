#!/bin/bash

set -eu

cd $(dirname $0)

venv="venv"

git fetch
git checkout master
git pull --rebase

if [[ ! -d $venv ]]; then
  virtualenv -p $(which python3) $venv
fi

$venv/bin/pip install -U setuptools pip wheel
$venv/bin/pip install -U -r requirements.txt
$venv/bin/python run.py
