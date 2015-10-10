WEBMIN_FW_TCP_INCOMING = 21 22 80 143 443 587 993 8983 12320 12321 12322

CREDIT_ANCHORTEXT = FormaVid Small Business Appliance

COMMON_OVERLAYS = apache adminer confconsole-lamp
COMMON_CONF = ckeditor apache-credit phpsh apache-vhost adminer-apache adminer-mysql

include $(FAB_PATH)/common/mk/turnkey/php.mk
include $(FAB_PATH)/common/mk/turnkey/mysql.mk
include $(FAB_PATH)/common/mk/turnkey.mk

