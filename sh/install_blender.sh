#!/usr/bin/env bash


BIN_DIR="bin"
BLENDER_REMOTE_REP="http://download.blender.org/release/"
BLENDER_VERS="Blender2.77"
BLENDER_FILE="blender-2.77-rc2-linux-glibc211-x86_64"

# Check
echo "[INSTALL BLENDER] Check directory"
CURRENT_DIR=${PWD##*/}
if [ "$CURRENT_DIR" != "mouse_locomotion" ]; then
	echo "[INSTALL BLENDER] Please cd to mouse_locomotion directory to install blender"
	exit
fi

# Download
cd ${BIN_DIR}
echo "[INSTALL BLENDER] Download Blender"
wget "${BLENDER_REMOTE_REP}${BLENDER_VERS}/${BLENDER_FILE}.tar.bz2"

# Install
echo "[INSTALL BLENDER] Extract and install Blender"
tar -xvf "${BLENDER_FILE}.tar.bz2"
mv ${BLENDER_FILE} ${BLENDER_VERS}
rm "${BLENDER_FILE}.tar.bz2"
