#!/usr/bin/env bash

PROJECT_DIR=`dirname $0`/..

PROJECT_ENV=${PROJECT_DIR}/virtualenv

if [ -d "/vagrant/" ]; then
  PROJECT_ENV=~/virtualenv
fi

# Confirm we're definitely running inside the VM or on a server, otherwise we'll bail.
HOSTNAME=`hostname`
grep 'CentOS' /etc/redhat-release 2>&1 >/dev/null
ON_CENTOS=$?
if [ "x${HOSTNAME}" != "xbear.virt.local" ] && [ "x${ON_CENTOS}" != "x0" ]; then
    echo "ERROR: attempting to run ${0} outside of VM."
    exit 1
fi

${PROJECT_DIR}/bin/update-virtualenv.sh ${PROJECT_DIR} ${PROJECT_ENV}

# Update the database schema.
MANAGE=${PROJECT_DIR}/src/manage.py

$MANAGE migrate

echo "Done."
