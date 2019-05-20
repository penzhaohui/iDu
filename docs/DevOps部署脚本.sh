1. 创建虚拟局域网
docker network create \
-d bridge \
--subnet 192.168.100.0/24 \
--gateway 192.168.100.1 \
-o parent=eth0 idu-devops-network

2. 创建Jenkins
docker run -d \
--restart=always \
--net=idu-devops-network \
--ip=192.168.100.101 \
--hostname=jenkins  \
--name jenkins \
-p 5050:8080 \
-p 50000:50000 \
-v /data/jenkins_home:/var/jenkins_home \
-v /var/run/docker.sock:/var/run/docker.sock \
-v $(which docker):/usr/bin/docker \
idu/jenkins

3. 创建Portainer
docker run -d \
--restart=always \
--net=idu-devops-network \
--ip=192.168.100.102 \
--hostname=portainer  \
--name portainer \
-p 9000:9000  \
-v /var/run/docker.sock:/var/run/docker.sock \
portainer/portainer

4. 创建测试环境
docker volume create --name mariadb_data

docker run -d \
--restart=always \
--net=idu-devops-network \
--ip=192.168.100.201 \
--hostname=mariadb  \
--name mariadb \
-e ALLOW_EMPTY_PASSWORD=yes \
-e MARIADB_USER=bn_testlink \
-e MARIADB_DATABASE=bitnami_testlink \
--volume mariadb_data:/bitnami \
bitnami/mariadb:latest

docker volume create --name testlink_data

docker run -d \
--restart=always \
--net=idu-devops-network \
--ip=192.168.100.202 \
--hostname=testlink \
--name testlink \
-p 8000:80 \
-p 8443:443 \
-e ALLOW_EMPTY_PASSWORD=yes \
-e TESTLINK_DATABASE_USER=bn_testlink \
-e TESTLINK_DATABASE_NAME=bitnami_testlink \
-e TESTLINK_USERNAME=user \
-e TESTLINK_PASSWORD=bitnami \
-e TESTLINK_EMAIL=peter.peng@opengov.top \
-e TESTLINK_LANGUAGE=zh_CN \
-e SMTP_ENABLE=true \
-e SMTP_HOST=smtp.opengov.top \
-e SMTP_PORT=25 \
-e SMTP_USER=peter.peng@opengov.top \
-e SMTP_PASSWORD=Change@2020 \
--volume testlink_data:/bitnami \
bitnami/testlink:latest

U/P: user/bitnami

docker logs testlink

docker run -d \
--restart=always \
--net=idu-devops-network \
--ip=192.168.100.203 \
--hostname=mantisbtdb \
--name mantisbtdb \
-e MYSQL_ROOT_PASSWORD=root \
-e MYSQL_DATABASE=bugtracker \
-e MYSQL_USER=mantisbt \
-e MYSQL_PASSWORD=mantisbt \
mysql:5.7.20

docker exec -ti mantisbtdb /bin/bash
mysql -uroot -proot
show databases;
select host,user from mysql.user;
show grants for mantisbt;

docker run -d \
--restart=always \
--net=idu-devops-network \
--ip=192.168.100.204 \
--hostname=mantisbt \
--name mantisbt \
-p 8001:80 \
vimagick/mantisbt:latest