'''
1. Must follow the naming rule. <rule_#>
2. Update rule rang in ../normalize.py
'''

def rule_1(message):
    # Define the logic for rule_1
    print(f"Debug: Checking rule_1 for message: {message}")
    if message == 'The illegal process="/etc/ips/rate_based.pyc"(/compress/usr/bin/python3.8), has been triggered, cmdline="/usr/bin/python /etc/ips/rate_based.pyc"':
        return 1

def rule_2(message):
    # Define the logic for rule_2
    print(f"Debug: Checking rule_2 for message: {message}")
    if message == 'The illegal process="/etc/ips/system_protection_port_check.pyc"(/compress/usr/bin/python3.8), has been triggered, cmdline="python /etc/ips/system_protection_port_check.pyc"':
        return 1

def rule_3(message):
    # Define the logic for rule_3
    print(f"Debug: Checking rule_3 for message: {message}")
    if message == 'The unsafe file=/db/etc/ip-reputation/zirsig(CREATE), has been added, pid=(mv), ppid=(irsig_zsdn_upda), cmdline="mv /tmp/ir-signature /db/etc/ip-reputation/zirsig"':
        return 1

def rule_4(message):
    # Define the logic for rule_3
    print(f"Debug: Checking rule_4 for message: {message}")
    if message == 'The illegal process="/etc/external-block-list/external_block_list_download.pyc"(/compress/usr/bin/python3.8), has been triggered, cmdline="/bin/python3 /etc/external-block-list/external_block_list_download.pyc dns-url"':
        return 1

def rule_5(message):
    # Define the logic for rule_3
    print(f"Debug: Checking rule_5 for message: {message}")
    if message == 'The illegal process="/etc/ip-reputation/parse_ip_sig_version.pyc"(/compress/usr/bin/python3.8), has been triggered, cmdline="/bin/python /etc/ip-reputation/parse_ip_sig_version.pyc /db/etc/app_patrol/sig-version.txt"':
        return 1

def rule_6(message):
    # Define the logic for rule_3
    print(f"Debug: Checking rule_6 for message: {message}")
    if message == 'The illegal process="/etc/backup_mail/backup_and_send.sh"(/compress/usr/bin/bash), has been triggered, cmdline="/bin/bash /etc/backup_mail/backup_and_send.sh"':
        return 1

def rule_7(message):
    # Define the logic for rule_7
    print(f"Debug: Checking rule_7 for message: {message}")
    if message == 'The illegal process="/etc/backup_mail/send_backup_mail.sh"(/compress/usr/bin/bash), has been triggered, cmdline="/bin/bash /etc/backup_mail/send_backup_mail.sh"':
        return 1

def rule_8(message):
    # Define the logic for rule_3
    print(f"Debug: Checking rule_8 for message: {message}")
    if message == 'The illegal process="/etc/backup_mail/send_mail_now.sh"(/compress/usr/bin/bash), has been triggered, cmdline="/bin/bash /etc/backup_mail/send_mail_now.sh"':
        return 1

def rule_9(message):
    # Define the logic for rule_3
    print(f"Debug: Checking rule_9 for message: {message}")
    if message == 'The unsafe file=/db/etc/zyxel/ftp/.myzyxel/fetchurl/app_zyxel_incr(CREATE), has been added, pid=(python), ppid=(sh), cmdline="python /usr/sbin/fetchurl_agent.pyc all 1.30(ABXE.1) USG FLEX 200HP 1.30(ABXE.0) USG FLEX 200HP"':
        return 1



