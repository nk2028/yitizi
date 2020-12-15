#! /usr/bin/env bash

for i in *.gv; do
    dot -Tpng "$i" -o "${i%.gv}.png"
done
