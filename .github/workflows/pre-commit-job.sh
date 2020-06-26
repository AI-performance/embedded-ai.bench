#!/usr/bin/env bash
set -x

readonly PREFIX="$(pwd)/miniconda3"
function is_cmd_existed() {
  cmd=$1
  exec_res=$(command -v ${cmd})
  if [[ ${#exec_res} > 0 ]]; then
      echo "command ${cmd} existed"
      echo 1
  else
      echo "command ${cmd} not existed"
      echo 0
  fi
}

function get_platform() {
    uname_a_str=`uname -a`
    if [[ $uname_a_str =~ "Linux" ]]; then
        echo "Linux"
    elif [[ $uname_a_str =~ "Darwin" ]]; then
        echo "Darwin"
    else
        echo "Unsupported for platform ${uname_a_str}"
        exit 1
    fi
}

function abort() {
    echo "Your change doesn't follow embedded-ai.bench's code style" 1>&2
    echo "Please use pre-commit to auto-format your code." 1>&2
    exit 1
}

function install_miniconda() {
    #apt update
    apt install -y wget git
    #cmd="conda"
    #is_conda_existed=`is_cmd_existed ${cmd}`
    #echo $is_conda_existed
    #if [[ $is_conda_existed =~ "1" ]]; then
    #    return
    #fi

    miniconda_pkg_name=""
    platform=$(get_platform)
    if [[ $platform =~ "Linux" ]]; then
        miniconda_pkg_name="Miniconda3-latest-Linux-x86_64.sh"
    elif [[ $platform =~ "Darwin" ]]; then
        miniconda_pkg_name="Miniconda3-latest-MacOSX-x86_64.sh"
    else
        echo "Unsupported for platform ${platform}"
        exit 1
    fi

    wget -c "https://repo.anaconda.com/miniconda/${miniconda_pkg_name}"
    chmod +x ${miniconda_pkg_name}
    ./${miniconda_pkg_name} -b -p $PREFIX

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
    conda create --yes --quiet --name dev-env-py python=3.8
    conda activate dev-env-py

    python3 -m pip install pre-commit
    conda activate
    conda init bash

    pre-commit uninstall
    pre-commit install

    if ! pre-commit run -a ; then
        ls -lh
        git diff --exit-code
        exit 1
    fi

    trap : 0
}

set e
trap 'abort' 0
cd `dirname $0`
cd ..
export PATH=/usr/bin:$PATH

install_miniconda
