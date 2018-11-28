set -x

# 安装Docker Engine
yum install wget
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo_bak 
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo 
cat /etc/yum.repos.d/CentOS-Base.repo
yum makecache
yum -y update
uname -r
sudo yum update
sudo yum remove docker  docker-common docker-selinux docker-engine
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum list docker-ce --showduplicates | sort -r
sudo yum install docker-ce-18.06.1.ce
sudo systemctl start docker
sudo systemctl enable docker
docker version

# 开启端口：8080 9090 8069 8072 443 80
firewall-cmd --zone=public --add-port=8080/tcp –permanent
firewall-cmd --zone=public --add-port=9090/tcp –permanent
firewall-cmd --zone=public --add-port=8069/tcp –permanent
firewall-cmd --zone=public --add-port=8070/tcp --permanent
firewall-cmd --zone=public --add-port=8072/tcp –permanent
firewall-cmd --zone=public --add-port=443/tcp –permanent
firewall-cmd --zone=public --add-port=80/tcp –permanent
firewall-cmd --reload
firewall-cmd --zone=public --list-ports

# 创建文件夹
mkdir -p /var/idu/docker

mkdir -p /var/idu/alarm/data 
mkdir -p /var/idu/alarm/certs
mkdir -p /var/idu/alarm/logs
mkdir -p /var/idu/alarm/config
adduser odoo
chown odoo:odoo /var/idu/alarm/data
chown odoo:odoo /var/idu/alarm/certs
chown odoo:odoo /var/idu/alarm/logs
chown odoo:odoo /var/idu/alarm/config

mkdir -p /var/idu/nginx/config
mkdir -p /var/idu/nginx/certs
mkdir -p /var/idu/nginx/logs
adduser nginx
chown nginx:nginx /var/idu/nginx/config
chown nginx:nginx /var/idu/nginx/certs
chown nginx:nginx /var/idu/nginx/logs
sudo chown -R nginx:nginx /var/idu/nginx/logs
sudo chmod -R 755 /var/idu/nginx/logs

mkdir -p /var/idu/chat/logs
mkdir -p /var/idu/chat/certs
mkdir -p /var/idu/chat/config
mkdir -p /var/idu/chat/data


# 下载对应的文件到文件夹（手工操作）
# curl /var/idu/docker
# curl /var/idu/chat/certs
# curl /var/idu/chat/config
# docker save -o docker-idu-alarm.tar idu/alarm:1.0
# docker save -o docker-idu-nginx.tar idu/nginx:1.0
# docker save -o docker-idu-jenkins.tar idu/jenkins
# docker save -o docker-idu-chat.tar idu/chat:1.0
# docker save -o postgres-9.5.tar ipostgres:9.5

# 导入Docker Image
cd /var/idu/docker 
docker load < postgres-9.5.tar
docker load < docker-idu-alarm.tar 
docker load < docker-idu-nginx.tar
docker load < docker-idu-chat.tar
docker load < docker-idu-jenkins.tar

# 以下为开始搭建微信报警演示环境的每日构建步骤
# =============================================================
# 1, 删除已安装的容器
docker container rm -f idu-alarm-db
docker container rm -f idu-alarm
docker container rm -f idu-alarm-a
docker container rm -f idu-alarm-b
docker container rm -f idu-alarm-nginx
docker container rm -f idu-chat
docker network rm idu-alarm-saas-network

# 2, 创建虚拟局域网
docker network create idu-alarm-saas-network

# 3, 创建数据库
docker run \
-d \
--restart=always \
-v /var/idu/alarm/data:/var/lib/postgresql/data \
-p 5432:5432 \
-e POSTGRES_USER=odoo \
-e POSTGRES_PASSWORD=odoo \
--network=idu-alarm-saas-network \
--name idu-alarm-db  \
postgres:9.5

# 4, 创建微信报警后台
: ${ODOO_MASTER_PASS:=`< /dev/urandom tr -dc A-Za-z0-9 | head -c16;echo;`}

docker run \
-d \
--name idu-alarm \
--restart=always \
--network=idu-alarm-saas-network \
-v /var/idu/alarm/certs:/mnt/certs \
-v /var/idu/alarm/logs:/mnt/logs  \
-e ODOO_MASTER_PASS=${ODOO_MASTER_PASS} \
-e DB_PORT_5432_TCP_ADDR=idu-alarm-db \
-t idu/alarm:1.0


docker run \
-d \
--name idu-alarm-a \
--restart=always \
--network=idu-alarm-saas-network \
-v /var/idu/alarm/certs:/mnt/certs \
-v /var/idu/alarm/logs:/mnt/logs  \
-e ODOO_MASTER_PASS=${ODOO_MASTER_PASS} \
-e DB_PORT_5432_TCP_ADDR=idu-alarm-db \
-t idu/alarm:1.0

docker run \
-d \
--name idu-alarm-b \
--restart=always \
--network=idu-alarm-saas-network \
-v /var/idu/alarm/certs:/mnt/certs \
-v /var/idu/alarm/logs:/mnt/logs  \
-e ODOO_MASTER_PASS=${ODOO_MASTER_PASS} \
-e DB_PORT_5432_TCP_ADDR=idu-alarm-db \
-t idu/alarm:1.0

docker run \
-d \
--name idu-alarm-app \
--restart=always \
-p 8069:8069 \
-p 8072:8072 \
--network=idu-alarm-saas-network \
-v /var/idu/alarm/logs:/mnt/logs  \
-e ODOO_MASTER_PASS=admin \
-e DB_PORT_5432_TCP_ADDR=idu-alarm-db \
-t idu/alarm:1.0

docker exec \
 -u root \
 -t idu-alarm \
sed -i 's/dbfilter.*/dbfilter = ^%d$/' /mnt/config/odoo-server.conf

docker exec \
 -u root \
 -t idu-alarm-a \
sed -i 's/dbfilter.*/dbfilter = ^%d$/' /mnt/config/odoo-server.conf

docker exec \
 -u root \
 -t idu-alarm-b \
sed -i 's/dbfilter.*/dbfilter = ^%d$/' /mnt/config/odoo-server.conf

# 5, 创建Nginx反向代理服务器

docker run  \
-d \
-p 80:80 \
-p 443:443 \
--name idu-alarm-nginx \
--network=idu-alarm-saas-network \
-v /var/idu/nginx/nginx.conf:/etc/nginx/nginx.conf  \
-v /var/idu/nginx/certs:/etc/nginx/certs  \
-v /var/idu/nginx/logs:/etc/nginx/logs  \
-t idu/nginx:1.0

# 6, 创建微信报警实时聊天服务器
docker run -d  \
--name idu-chat  \
--network=idu-alarm-saas-network \
--restart=always -p 8080:8080  \
-p 9090:9090  \
-v /var/idu/chat/logs:/etc/idu-chat/logs  \
-v /var/idu/chat/certs:/etc/idu-chat/certs  \
-v /var/idu/chat/config:/etc/idu-chat/config  \
-v /var/idu/chat/data:/etc/idu-chat/data  \
-t idu/chat:1.0

# 以下是开发环境
# 安装Docker 容器的可视化管理工具(U/P: admin/admin@2018)
# =============================================================
docker run -d \
-p 9000:9000  \
--restart=always \
-v /var/run/docker.sock:/var/run/docker.sock \
--name portainer \
portainer/portainer

# 安装Jenkins 容器的可视化管理工具
# =============================================================
# mv /var/jenkins_home /data
docker run -d \
--name jenkins \
--restart=always \
-p 5050:8080 \
-p 50000:50000 \
-v /data/jenkins_home:/var/jenkins_home \
-v /var/run/docker.sock:/var/run/docker.sock \
-v $(which docker):/usr/bin/docker \
idu/jenkins

