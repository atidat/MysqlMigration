#!/bin/sh

prj=$1
ts=`date "+%s"`
mapping_dir=/data/var/${prj}${ts}
mapping_port=$2

if [[ -z ${mapping_port} ]]; then
    echo "warn: You didn't input port info and PlEaSe EnSuRe YoUr PoRt NuMbEr Is NoT OcCuPiEd"
    echo "usage: bash dmBasextrabackupContainer.sh 7274"
	echo "exit"
	exit 0
fi


function prepare()
{
    echo "[0] create mysql container ..."
    rm -rf ${mapping_dir}/run ${mapping_dir}/lib
    mkdir -p ${mapping_dir}/run ${mapping_dir}/lib

    container_name=${prj}${ts}
    docker stop ${container_name} >/dev/null 2>&1
    docker rm ${container_name} >/dev/null 2>&1
}

function create_container()
{
    echo "[1] create mysql container ..."
    docker run -itd --name ${container_name} -p ${mapping_port}:3306 -v ${mapping_dir}/run/mysqld:/data/var/run/mysqld -v ${mapping_dir}/lib/mysql:/data/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 mysql:8.0.20
}

function backup_data()
{
    echo "[2] configure mysql data ..."
    docker exec -it ${container_name} /bin/bash -c "ln -s /etc/mysql/my.cnf /etc/my.cnf && cd /data/var && chown -R mysql:mysql run lib"
    docker cp /home/mysql-docker/my.cnf ${container_name}:/etc/mysql/my.cnf
    # docker cp /home/fulu/dba/meisuo0414/slave_cfg/my.cnf ${container_name}:/etc/mysql/my.cnf 
    docker restart ${container_name}
    docker exec -it ${container_name} /bin/bash -c "ln -s /data/var/run/mysqld/mysqld.sock /var/run/mysqld/mysqld.sock && chown -R mysql:mysql /var/run/mysqld && mysql -uroot -p123456 << EOF 2>/dev/null
    ALTER USER 'root'@'%' IDENTIFIED BY 'Root123...';flush privileges;
    EOF"
}

function restore_data()
{
    echo "[3] restore data"
    rm -rf /home/mysql-docker/mysql/* && mkdir -p /home/mysql-docker/mysql && cp -rf ${mapping_dir}/lib/mysql /home/mysql-docker/mysql
    cd ${mapping_dir}/lib/mysql && rm -rf *
    xtrabackup --apply-log --target-dir=/tmp/meishuo0415 --host=193.169.200.132 --port=${mapping_port} --user=root --password="Root123..." --socket=${mapping_dir}/run/mysqld/mysqld.sock --datadir=${mapping_dir}/lib/mysql >/dev/null 2>&1

    xtrabackup --copy-back --target-dir=/tmp/meishuo0415 --host=193.169.200.132 --port=${mapping_port} --user=root --password="Root123..." --socket=${mapping_dir}/run/mysqld/mysqld.sock --datadir=${mapping_dir}/lib/mysql >/dev/null 2>&1
    cd ${mapping_dir} && chown -R polkitd:input *
}

function post_prepare()
{
    echo "[4] mysql server is ready ..."
    docker exec -it ${container_name} /bin/bash -c "cd /data/var/lib/mysql && chown -R mysql:mysql *"
    docker restart ${container_name}
}


prepare
create_container
backup_data
restore_data
post_prepare

end_ts=`date "+%s"`

echo "*************** NOTICE ***************"
echo "mysql server listening" $mapping_port
echo "mysql server password is the same as source mysql server"
echo "cost time:" `expr ${end_ts} - ${ts}` "s"
echo "Restore data Successful"

