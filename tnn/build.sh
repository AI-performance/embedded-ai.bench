#!/bin/bash
set -x

# download code repo from github
function download_repo {
    # download repo
    if [ ! -d "./tnn" ]; then
        git clone https://github.com/tencent/tnn.git tnn
    else
        echo "local tnn repo exited"
    fi
}

function build {
   # prepare build
   cd tnn/scripts/
   ./build_android.sh
}

function main {
    download_repo
    build
}

main ${@}
