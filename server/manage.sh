#!/bin/bash

# アフィン変換計算パラメーター保存ファイル
FILE="./affine_parameter.json"

pipenv shell
if [ -e $FILE ]; then
  python affine.py
else
  python ransac_affine_cal.py
fi

