#!/bin/bash

${MINIO_BIN} server --console-address ":9001" --config-dir=${MINIO_CONFIG_DIR} $@ ${MINIO_DATA_DIR}
