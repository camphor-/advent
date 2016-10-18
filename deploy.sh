#!/bin/bash
set -ex

branch=$1
if [ -z "$branch" ]; then
  branch=master
fi

set -u

cd $(dirname $0)

echo "----- start -----"
date

git fetch
git checkout $branch
git reset --hard origin/$branch

/usr/local/bin/docker-compose -f docker-compose.prod.yml build --pull
/usr/local/bin/docker-compose -f docker-compose.prod.yml up -d

echo "----- end -----"
