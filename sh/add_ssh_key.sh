#!/usr/bin/env bash

## READ this explanation for UGent ELIS computers !! ##

# --> When logging with ssh, /home/gurbain/.bash_profile is read
# This change HOME to /home/gurbain/private and read new .bash_profile
# in /home/gurbain/private/.bash_profile, reading /home/gurbain/private/.bashrc

# --> When adding ssh key to /home/gurbain/.ssh/authorized_keys, a different
# config is read from /etc/ssh/ssh_config, using PAM and SELinux.
# In this configuration, there seem to be no more RW rights for the user, neither is
# /home/gurbain/.bash_profile executed. Thus, HOME is still /home/gurbain
# but nothing can be written anymore...
# Therefore, ssh_keys are not used..

# Params
LOCAL="157.193.206.245"
LOCAL_USER="gabs48"
LOCAL_SSH_FILE="${HOME}/.ssh/id_rsa.pub"

REMOTE="campus"
REMOTE_USER="gurbain"
REMOTE_HOME="/home/gurbain"
REMOTE_SSH_FOLDER="${REMOTE_HOME}/.ssh"

# Add keys
echo "[ADD SSH KEY] ======== Adding key to server ======== "
ssh-copy-id ${REMOTE_USER}@${REMOTE}