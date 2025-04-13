'''
1. Must follow the naming rule. <rule_#>
2. Update rule rang in ../normalize.py
'''

def rule_1(message):
    # Define the logic for rule_1
    #print(f"Debug: Checking rule_1 for message: {message}")
    if message == 'The illegal process="/etc/ips/rate_based.pyc"(/compress/usr/bin/python3.8), has been triggered, cmdline="/usr/bin/python /etc/ips/rate_based.pyc"':
        return 1
    else:
        return 0

def rule_2(message):
    # Define the logic for rule_2
    #print(f"Debug: Checking rule_2 for message: {message}")
    if message == 'The illegal process="/etc/ips/system_protection_port_check.pyc"(/compress/usr/bin/python3.8), has been triggered, cmdline="python /etc/ips/system_protection_port_check.pyc"':
        return 1
    else:
        return 0

def rule_3(message):
    # Define the logic for rule_3
    #print(f"Debug: Checking rule_3 for message: {message}")
    if message == 'The unsafe file=/db/etc/ip-reputation/zirsig(CREATE), has been added, pid=(mv), ppid=(irsig_zsdn_upda), cmdline="mv /tmp/ir-signature /db/etc/ip-reputation/zirsig"':
        return 1
    else:
        return 0

def rule_4(message):
    # Define the logic for rule_3
    #print(f"Debug: Checking rule_4 for message: {message}")
    if message == 'The illegal process="/etc/external-block-list/external_block_list_download.pyc"(/compress/usr/bin/python3.8), has been triggered, cmdline="/bin/python3 /etc/external-block-list/external_block_list_download.pyc dns-url"':
        return 1
    else:
        return 0

def rule_5(message):
    # Define the logic for rule_3
    #print(f"Debug: Checking rule_5 for message: {message}")
    if message == 'The illegal process="/etc/ip-reputation/parse_ip_sig_version.pyc"(/compress/usr/bin/python3.8), has been triggered, cmdline="/bin/python /etc/ip-reputation/parse_ip_sig_version.pyc /db/etc/app_patrol/sig-version.txt"':
        return 1
    else:
        return 0

def rule_6(message):
    # Define the logic for rule_3
    #print(f"Debug: Checking rule_6 for message: {message}")
    if message == 'The illegal process="/etc/backup_mail/backup_and_send.sh"(/compress/usr/bin/bash), has been triggered, cmdline="/bin/bash /etc/backup_mail/backup_and_send.sh"':
        return 1
    else:
        return 0

def rule_7(message):
    # Define the logic for rule_7
    #print(f"Debug: Checking rule_7 for message: {message}")
    if message == 'The illegal process="/etc/backup_mail/send_backup_mail.sh"(/compress/usr/bin/bash), has been triggered, cmdline="/bin/bash /etc/backup_mail/send_backup_mail.sh"':
        return 1
    else:
        return 0

def rule_8(message):
    # Define the logic for rule_8
    #print(f"Debug: Checking rule_8 for message: {message}")
    if message == 'The illegal process="/etc/backup_mail/send_mail_now.sh"(/compress/usr/bin/bash), has been triggered, cmdline="/bin/bash /etc/backup_mail/send_mail_now.sh"':
        return 1
    else:
        return 0

def rule_9(message):
    # Define the logic for rule_9
    #print(f"Debug: Checking rule_9 for message: {message}")
    if message == 'The illegal process="/etc/sslvpn/start-up.sh"(/compress/usr/bin/bash), has been triggered, cmdline="/bin/bash /etc/sslvpn/start-up.sh tun0    init"':
        return 1
    else:
        return 0


def rule_10(message):
    # Define the logic for rule_10
    #print(f"Debug: Checking rule_10 for message: {message}")
    if message == 'The illegal process="/etc/sslvpn/sslvpn_disconnect.sh"(/compress/usr/bin/bash), has been triggered, cmdline="/bin/bash /etc/sslvpn/sslvpn_disconnect.sh "':
        return 1
    else:
        return 0

def rule_11(message):
    # Define the logic for rule_11
    #print(f"Debug: Checking rule_11 for message: {message}")
    if message == 'The unsafe file=/db/etc/security_signature_auto_update/ips(CREATE), has been added, pid=(/bin/touch), ppid=(python3), cmdline="/bin/touch /db/etc/security_signature_auto_update/ips"':
        return 1
    else:
        return 0

def rule_12(message):
    # Define the logic for rule_11
    #print(f"Debug: Checking rule_11 for message: {message}")
    if message == 'The unsafe file=/db/etc/security_signature_auto_update/app-patrol(CREATE), has been added, pid=(/bin/touch), ppid=(python3), cmdline="/bin/touch /db/etc/security_signature_auto_update/app-patrol"':
        return 1
    else:
        return 0

def rule_13(message):
    # Define the logic for rule_12
    #print(f"Debug: Checking rule_12 for message: {message}")
    if message == 'The unsafe file=/share/sys_mgnt.log(CREATE), has been added, pid=(bootup_progress), ppid=(rsyslogd), cmdline="/bin/sh /usr/sbin/bootup_progress   systemd[1]: Started Serial Getty on ttyS1."':
        return 1
    else:
        return 0
    
def rule_14(message):
    # Define the logic for rule_14
    rule_string = 'The unsafe file=/db/etc/modsecurity/sigversion.txt(CREATE), has been added, pid=(null), ppid=(modsecurity_upd), cmdline="/bin/mv /tmp/sigversion.txt /db/etc/modsecurity/sigversion.txt"'
    if message == rule_string:
        return 1
    else:
        #print(f"Debug: Checking rule_14 for message: {message}")
        print(f"Debug: Comparing rule_14 with string: {rule_string}")
        return 0

def rule_15(message):
    # Define the logic for rule_15
    rule_string = 'The unsafe file=/db/etc/zyxel/ftp/.myzyxel/fetchurl/fw_zyxel_1(CREATE), has been added, pid=(python), ppid=(myzyxel_fetchur), cmdline="python /usr/sbin/fetchurl_agent.pyc sps    "'
    if message == rule_string:
        return 1
    else:
        #print(f"Debug: Checking rule_15 for message: {message}")
        print(f"Debug: Comparing rule_15 with string: {rule_string}")
        return 0

def rule_16(message):
    # Define the logic for rule_16
    rule_string = 'The unsafe file=/db/etc/zyxel/ftp/.myzyxel/fetchurl/modsecurity_zyxel(CREATE), has been added, pid=(python), ppid=(myzyxel_fetchur), cmdline="python /usr/sbin/fetchurl_agent.pyc sps    "'
    if message == rule_string:
        return 1
    else:
        #print(f"Debug: Checking rule_16 for message: {message}")
        print(f"Debug: Comparing rule_16 with string: {rule_string}")
        return 0

def rule_17(message):
    # Define the logic for rule_17
    rule_string = 'The unsafe file=/db/etc/zyxel/ftp/.myzyxel/fetchurl/fetchurl_ret(CREATE), has been added, pid=(python), ppid=(myzyxel_fetchur), cmdline="python /usr/sbin/fetchurl_agent.pyc sps    "'
    if message == rule_string:
        return 1
    else:
        #print(f"Debug: Checking rule_17 for message: {message}")
        print(f"Debug: Comparing rule_17 with string: {rule_string}")
        return 0

def rule_18(message):
    # Define the logic for rule_17
    rule_string = 'ABC'
    if message == rule_string:
        return 1
    else:
        #print(f"Debug: Checking rule_17 for message: {message}")
        print(f"Debug: Comparing rule_17 with string: {rule_string}")
        return 0

def rule_19(message):
    # Define the logic for rule_17
    rule_string = 'ABC'
    if message == rule_string:
        return 1
    else:
        #print(f"Debug: Checking rule_17 for message: {message}")
        print(f"Debug: Comparing rule_17 with string: {rule_string}")
        return 0

def rule_20(message):
    # Define the logic for rule_17
    rule_string = 'ABC'
    if message == rule_string:
        return 1
    else:
        #print(f"Debug: Checking rule_17 for message: {message}")
        print(f"Debug: Comparing rule_17 with string: {rule_string}")
        return 0
def rule_(message):
    # Define the logic for rule_17
    rule_string = 'ABC'
    if message == rule_string:
        return 1
    else:
        #print(f"Debug: Checking rule_17 for message: {message}")
        print(f"Debug: Comparing rule_17 with string: {rule_string}")
        return 0
