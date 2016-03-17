#!/usr/bin/env bash

# Params
IFACE="eth0"
LOCAL=$(ip -4 address show $IFACE | grep 'inet' | sed 's/.*inet \([0-9\.]\+\).*/\1/')
LOCAL_USER=$(whoami)

REMOTE="campus"
REMOTE_USER="gurbain"
REMOTE_HOME="/home/gurbain/private"
REMOTE_BIN_FOLDER="${REMOTE_HOME}/bin"
REMOTE_SRC_FOLDER="${REMOTE_HOME}/src"

RPYC_NAME="rpyc"
PLUMBUM_NAME="plumbum"
BLENDER_NAME="blender"
XVFB_NAME="xvfb_1.11.4-0ubuntu10.17_amd64"
MODEL_NAME="mouse_locomotion"

RPYC_SRC="https://github.com/tomerfiliba/${RPYC_NAME}"
PLUMBUM_SRC="https://github.com/tomerfiliba/${PLUMBUM_NAME}"
MODEL_SRC="https://github.com/Gabs48/${MODEL_NAME}"
BLENDER_BIN="http://download.blender.org/release/Blender2.76/blender-2.76b-linux-glibc211-x86_64.tar.bz2"
XVFB_BIN="${XVFB_NAME}.deb"


# Create a command to execute remotely
echo "[INSTALL PACKAGES] ======== Access Control ======== "
printf "[INSTALL PACKAGES] Enter your password to execute all commands on ${REMOTE}: "
read -s REMOTE_PWD
printf "\n"
REMOTE_CMD="sshpass -p ${REMOTE_PWD} ssh ${REMOTE_USER}@${REMOTE} 'cd ${REMOTE_HOME} && "

# Download package sources
echo "[INSTALL PACKAGES] ======== Downloading source packages ======== "
echo "[INSTALL PACKAGES] Download: ${RPYC_NAME}, ${PLUMBUM_NAME} and ${MODEL_NAME}"
eval "${REMOTE_CMD} mkdir -p ${REMOTE_SRC_FOLDER}'"
eval "${REMOTE_CMD} cd ${REMOTE_SRC_FOLDER} && git clone ${RPYC_SRC}'"
eval "${REMOTE_CMD} cd ${REMOTE_SRC_FOLDER} && git clone ${PLUMBUM_SRC}'"
eval "${REMOTE_CMD} cd ${REMOTE_SRC_FOLDER} && git clone ${MODEL_SRC}'"
eval "${REMOTE_CMD} cp ${REMOTE_SRC_FOLDER}/${RPYC_NAME}/bin/* ${REMOTE_BIN_FOLDER}'"


# Install packages
echo "[INSTALL PACKAGES] ======== Installing source packages ======== "
eval "${REMOTE_CMD} cd ${REMOTE_SRC_FOLDER}/${RPYC_NAME} && python setup.py install --user'"
eval "${REMOTE_CMD} cd ${REMOTE_SRC_FOLDER}/${PLUMBUM_NAME} &&  python setup.py install --user'"


# Download package binaries
echo "[INSTALL PACKAGES] ======== Downloading binary packages ======== "
eval "${REMOTE_CMD} wget ${BLENDER_BIN} -O ${BLENDER_NAME}.tar.bz2 '"
eval "${REMOTE_CMD} apt-get download xvfb'"

echo "[INSTALL PACKAGES] ======== Installing binary packages ======== "
eval "${REMOTE_CMD} mkdir -p ${REMOTE_BIN_FOLDER} && tar -xvf ${BLENDER_NAME}.tar.bz2 -C ${REMOTE_BIN_FOLDER} --strip-components 1'"
eval "${REMOTE_CMD} rm ${BLENDER_NAME}.tar.bz2'"
eval "${REMOTE_CMD} dpkg-deb -x ${XVFB_BIN} ${REMOTE_HOME}'"
eval "${REMOTE_CMD} rm ${XVFB_BIN}'"

#clear $REMOTE_PWD