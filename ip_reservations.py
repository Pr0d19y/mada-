__author__ = 'nfreiman'
import re

#DHCP_FILE_NAME = r'/etc/dhcpcd.conf'
DHCP_FILE_NAME = r'dhcpcd_test.conf'
NEW_IP_LINE = 'static ip_address={}\n'

IPS = {
    'pollination_tomato': '192.168.10.12',
    'pollination_zuc_male': '192.168.10.13',
    'pollination_zuc_female': '192.168.10.14',
    'pollination_zuc_fruit': '192.168.10.15',
    'cracker_maker': '192.168.10.16'
}


def set_static_ip(ip):
    static_ip_regex = re.compile('static ip_address=([\d\.]+)')
    initial_file_lines = []

    write_new_file = False
    block_exists = False
    with open(DHCP_FILE_NAME, 'r') as f:
        for line in f:
            a = static_ip_regex.match(line)
            if a:
                block_exists = True
                current_ip = a.groups()[0]
                if current_ip == ip:
                    return
                else:
                    initial_file_lines.append(NEW_IP_LINE.format(ip))
            else:
                initial_file_lines.append(line)

    if not block_exists:
        initial_file_lines.extend([
            '# configure raspberry pi as static IP\n',
            'interface wlan0\n',
            NEW_IP_LINE.format(ip),
            'static routers=192.168.10.1'
        ])

    with open(DHCP_FILE_NAME, 'w') as f:
        for line in initial_file_lines:
            f.write(line)

if __name__ == '__main__':
    set_static_ip(IPS['pollination_zuc_male'])