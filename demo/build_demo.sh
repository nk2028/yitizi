#!/bin/sh
dot -Tpng char.dot -o char.png
dot -Tpng route.dot -o route.png
dot -Kfdp -Tpng example1.dot -o example1.png
dot -Kfdp -Tpng example2.dot -o example2.png
