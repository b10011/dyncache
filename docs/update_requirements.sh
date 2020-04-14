#!/bin/bash

SCRIPTDIR="$(dirname $(readlink -f ${BASH_SOURCE[0]}))"

poetry export -f requirements.txt --dev > ${SCRIPTDIR}/requirements.txt
