uCloud: 106.75.171.47
U/P: root/peter.peng

Daily Update
===================================
cd iDu
git pull
git log

docker cp /root/iDu/extra-addons/idu_wechat_alarm idu:/mnt/addons/idu
docker restart idu

===================================
docker cp /root/iDu/extra-addons/idu_wechat_alarm idu:/mnt/addons/idu
docker cp /root/iDu/3rd-addons/auth_oauth_check_client_id idu:/mnt/addons/idu
docker cp /root/iDu/3rd-addons/auth_oauth_ip idu:/mnt/addons/idu
docker cp /root/iDu/3rd-addons/backend_theme_v10 idu:/mnt/addons/idu
docker cp /root/iDu/3rd-addons/base_user_role idu:/mnt/addons/idu
docker cp /root/iDu/3rd-addons/oauth_provider idu:/mnt/addons/idu
docker cp /root/iDu/3rd-addons/web_mobile idu:/mnt/addons/idu
docker cp /root/iDu/3rd-addons/web_notify idu:/mnt/addons/idu
docker cp /root/iDu/3rd-addons/web_responsive idu:/mnt/addons/idu

docker restart idu
docker exec -i -u root -t idu /bin/bash
cd /mnt/addons
ls
chmod -R 777 *

docker cp /root/iDu/odoo-10.0/ idu:/mnt/backups
docker exec -i -u root -t idu /bin/bash
cd /mnt/backups
cd /mnt/odoo-source
ls

chown -R root /mnt/odoo-source/
rm -rf /mnt/odoo-source
cp -r /mnt/backups/odoo-10.0/ /mnt/odoo-source
chown -R odoo:odoo /mnt/odoo-source

