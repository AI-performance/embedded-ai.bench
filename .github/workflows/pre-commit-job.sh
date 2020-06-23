#!/bin/bash
function abort() {
    echo "Your change doesn't follow embedded-ai.bench's code style" 1>&2
    echo "Please use pre-commit to auto-format your code." 1>&2
    exit 1
}

trap 'abort' 0
set -e
cd `dirname $0`
cd ..
export PATH=/usr/bin:$PATH
pip install pre-commit
pre-commit install

# note(ysh329): enable below for C/C++
# which clang-format
# clang-format --version

if ! pre-commit run -a ; then
  ls -lh
  git diff  --exit-code
  exit 1
fi

trap : 0
