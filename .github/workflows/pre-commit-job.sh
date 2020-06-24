#!/usr/bin/env bash
set -ex

function abort() {
    echo "Your change doesn't follow embedded-ai.bench's code style" 1>&2
    echo "Please use pre-commit to auto-format your code." 1>&2
    exit 1
}

function install_miniconda() {
    #hash conda 2>/dev/null || { echo >&2 "I require foo but it's not installed.  Aborting."; return; }

    #apt update
    #apt install -y wget git
    wget -c https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    chmod +x Miniconda3-latest-Linux-x86_64.sh
    PREFIX="$(pwd)/miniconda3"
    ./Miniconda3-latest-Linux-x86_64.sh -b -p $PREFIX


    echo """
# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('${PREFIX}/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "${PREFIX}/etc/profile.d/conda.sh" ]; then
        . "${PREFIX}/etc/profile.d/conda.sh"
    else
        export PATH="${PREFIX}/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<
""" >> ~/.bashrc
    source ~/.bashrc

    source ${PREFIX}/bin/activate
    conda create --yes --quiet --name dev-env-py python
    conda activate dev-env-py

    python3 -m pip install pre-commit
    #alias pre-commit=/root/miniconda3/envs/dev-env-py/bin/pre-commit
    pre-commit install
    conda init bash

# note(ysh329): enable below for C/C++
# which clang-format
# clang-format --version

    if ! pre-commit run -a ; then
        ls -lh
        git diff --exit-code
        exit 1
    fi

    trap : 0
}

trap 'abort' 0
cd `dirname $0`
cd ..
export PATH=/usr/bin:$PATH

install_miniconda
