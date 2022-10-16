#!/bin/bash

# please assure master has zip, slave has unzip and master could ssh slave without password
# master: yum install zip && ssh-keygen && ssh-copy-id ~/.ssh/id_rsa.pub root@${slave_ip}
# slave: yum install unzip

tar_dir=$1
master_ip=$2
user=$3
mysql_password=$4
slave_ip=$5
data_dir=$6

function backup()
{
    xtrabackup --backup --target-dir=${tar_dir} --no-timestamp --password=${mysql_password} --user=${user} 
    cd ${tar_dir} && zip -r master.zip *
    scp master.zip ${master_ip}:${tar_dir}
}

function restore()
{
    ssh ${slave_ip}
    cd ${tar_dir} && unzip ${master}.zip
    xtrabackup --apply-log --target-dir=${tar_dir}
    rm -rf ${data_dir} # should backup
    xtrabackup --copy-back --target-dir=${tar_dir}
    chown -R mysql:mysql ${data_dir}
    systemctl restart mysqld.service
}

backup
restore