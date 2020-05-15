import subprocess
import optparse
import re

def get_argu():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="provide the interface")
    parser.add_option("-m", "--mac", dest="mac", help="provide mac address")
    (option, argu) = parser.parse_args()
    if not option.interface:
        parser.error("[-] interface not found.")
    elif not option.mac:
        parser.error("[-] mac address not in proper format.")
    return option


def mac_changer(interface, mac):
    subprocess.call(["interface", interface, "down"])
    subprocess.call(["interface", interface, "hw", "ether", mac])
    subprocess.call(["interface", interface, "up"])
    print("[+] mac address successful change")


def get_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # print(ifconfig_result)
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_result:
        return mac_result.group(0)
    else:
        print("could not find mac address")

option = get_argu()

current_mac = get_mac(option.interface)
print("CURRENT_MAC = " + str(current_mac))

mac_changer(option.interface, option.mac)

current_mac = get_mac(option.interface)
if current_mac == option.mac:
    print("[+] MAC Address Successfully changed " + current_mac)
else:
    print("[-] MAC Address did not get changed.")


