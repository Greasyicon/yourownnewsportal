#!/bin/bash

while read p; do
  echo "Installing $p"
  pip install $p --no-cache-dir || true
done <requirements.txt
