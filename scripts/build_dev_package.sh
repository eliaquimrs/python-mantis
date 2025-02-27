#!/bin/bash

SCRIPT=$(realpath "$0")
PROJECT_PATH=$(dirname $(dirname "$SCRIPT"))

PARTIAL_VERSION=$1
if [ -z "$PARTIAL_VERSION" ]; then
    echo "Emtpy target version."
    echo "Use: build_dev_package.sh <target-version>"
    exit 0;
fi

VERSION_NUMBER_FILE="${PROJECT_PATH}/scripts/.version_ctrl-${PARTIAL_VERSION}"

if [ -f ${VERSION_NUMBER_FILE} ]; then
    echo "Version file exists"
    VERSION=$(cat ${VERSION_NUMBER_FILE})
else
    echo "Version file don't exists"
    VERSION=0
fi
 
VERSION_COUNT=$(expr ${VERSION} + 1)
echo "${VERSION_COUNT}" > ${VERSION_NUMBER_FILE}

FULL_VERSION="${PARTIAL_VERSION}-dev${VERSION_COUNT}"

echo ${FULL_VERSION}

sed -i "s/{{VERSION_PLACEHOLDER}}/${FULL_VERSION}/g" ${PROJECT_PATH}/pyproject.toml
sed -i "s/{{VERSION_PLACEHOLDER}}/${FULL_VERSION}/g" ${PROJECT_PATH}/mantis/__version.py

python3 -m pip install --upgrade build && python3 -m build ${PROJECT_PATH}

sed -i "s/${FULL_VERSION}/{{VERSION_PLACEHOLDER}}/g" ${PROJECT_PATH}/pyproject.toml
sed -i "s/${FULL_VERSION}/{{VERSION_PLACEHOLDER}}/g" ${PROJECT_PATH}/mantis/__version.py
