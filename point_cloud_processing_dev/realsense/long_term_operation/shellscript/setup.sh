#!/bin/bash

sudo chmod 700 *.sh

# 作業用ディレクトリ
cd /home/pi/workspace/akiyama_measure_pcd/long_term_operation/service

sudo chmod 700 *.service

sudo cp measure_pcd.service /etc/systemd/system/measure_pcd.service

cd /etc/systemd/system
sudo chmod 700 measure_pcd.service

# サービスの無効化
sudo systemctl disable measure_pcd

# サービスの有効化
sudo systemctl enable measure_pcd

# サービスの開始
sudo systemctl start measure_pcd