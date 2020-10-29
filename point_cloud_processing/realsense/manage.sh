#!/bin/bash
LOG_OUT="manage.sh.log"

function log() {
  echo -e "$(date '+%Y-%m-%dT%H:%M:%S') $@" | tee -a ${LOG_OUT}
}

log "start"
python3 measure_point_cloud.py
log "measure point cloud"
python3 scp_client.py
log "file to server"
log "end"
