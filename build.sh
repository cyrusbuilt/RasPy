#!/usr/bin/env bash

# Get script dir.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"
DOCS_DIR=${SCRIPT_DIR}/docs

echo
echo "Installing documentation helpers..."
echo
unamestr=`uname`
if [[ "${unamestr}" == "Darwin" ]]; then
    sudo tlmgr install ucs dvipng
else
    sudo apt-get install -qq texlive txlive-latex-extra dvipng
fi

echo
echo "Cleaning compiled scripts ..."
echo
find "${SCRIPT_DIR}" -name \*.pyc -type f -delete -print

echo
echo "Installing required packages ..."
echo
if [ -f requirements.txt ]; then
    sudo -H pip install --ignore-installed -r requirements.txt
else
    echo "ERROR: Missing package manifest. Cannot install dependencies."
    exit 1
fi

# Check if running on a Raspberry Pi (Linux). If so, install spidev.
if [[ "${unamestr}"=="Linux" ]]; then
    arch=`uname -m`
    if [[ ${arch} = *"arm"* ]]; then
        sudo -H pip install --ignore-installed spidev
    fi
fi

echo
echo "Checking documentation source ..."
if [ -d "${DOCS_DIR}" ]; then
    echo "Checking for makefile ..."
    if [ ! -f "${DOCS_DIR}/Makefile" ]; then
        echo "ERROR: Makefile missing. Cannot build."
        exit 1
    fi

    echo "Checking Sphinx configuration ..."
    if [ ! -f "${DOCS_DIR}/conf.py" ]; then
        echo "ERROR: Configuration file missing: ${DOCS_DIR}/conf.py. Cannot build."
        exit 1
    fi

    echo
    echo "Cleaning API documentation ..."
    echo
    cd "${DOCS_DIR}"
    make clean
    echo
    echo "Building API documentation ..."
    sphinx-apidoc -fo . ../raspy
    make html
else
    echo "WARN: Documentation source path not found: ${DOCS_DIR}"
fi

cd "${SCRIPT_DIR}"
echo
echo "Compiling source ..."
echo
python -m compileall -f ./raspy

echo
echo "Linting source ..."
echo
pylint --rcfile pylintrc ./raspy/*.py
flake8 ./raspy

echo
echo "Running unit tests ..."
echo
nose2 -v