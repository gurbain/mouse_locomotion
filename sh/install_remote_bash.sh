#!/usr/bin/env bash

# Params
IFACE="eth0"
LOCAL=$(ip -4 address show $IFACE | grep 'inet' | sed 's/.*inet \([0-9\.]\+\).*/\1/')
LOCAL_USER=$(whoami)
LOCAL_BASH_FILE="${HOME}/mouse_locomotion/sh/.bashrc"

REMOTE="campus"
REMOTE_USER="gurbain"
REMOTE_HOME="/home/gurbain/private"
REMOTE_BASH_FILE="${REMOTE_HOME}/.bashrc"
REMOTE_PROFILE_FILE="${REMOTE_HOME}/.bash_profile"

# If .bashrc does not existn add .bashrc from this repository and add .bash_profile entry
if ssh ${REMOTE_USER}@${REMOTE} stat ${REMOTE_BASH_FILE} \> /dev/null 2\>\&1
	then
		echo "[INSTALL REMOTE BASH] .bashrc already exists! Nothing to do..."
	else
		echo "[INSTALL REMOTE BASH] .bashrc does not exist! Copying from source $LOCAL_BASH_FILE"
		scp ${LOCAL_BASH_FILE} ${REMOTE_USER}@${REMOTE}:${REMOTE_BASH_FILE}
		ssh ${REMOTE_USER}@${REMOTE} "echo 'source .bashrc' >> ${REMOTE_PROFILE_FILE}"
fi