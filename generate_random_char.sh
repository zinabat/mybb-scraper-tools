#!/bin/sh

RESET_CACHE=0
# Loop through arguments and process them
for arg in "$@"
do
  case $arg in
    -c|--reset-cache)
    RESET_CACHE=1
    shift
    ;;
  esac
done
if [[ RESET_CACHE -eq 1 || ! -f activeUsers.json ]]; then
  URL="https://wolf-rpg.com/" WAIT_TIME=2 python3 scripts/getActiveUsers.py
  if [ $? -eq 0 ]; then
      echo OK
  else
      echo FAIL
      exit 1
  fi
fi
POST_MIN=50 python3 scripts/randChar.py