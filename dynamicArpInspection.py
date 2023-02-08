#netmiko is a library used to establish SSH connections to network devices, getpass is a library that prevents passwords from echoing to screen
import netmiko
import getpass

#takes the file name and the credentials for the engineer running the script 
user = input("Enter your username: ")
secret = getpass.getpass("Enter you password: ")
targets_file = input("Enter the name of the file containing the targets: ")
commands_file = input("Enter the name of the file containing the commands: ")

#opens the file containing the target ip addresses / hostnames and stores the contents in a variable
with open(targets_file) as filename:
    targets = filename.readlines()

#takes the contents in target, removes the whitespace at the end, and adds them to a list
target_list = []
for line in targets:
    target_list.append(line.strip())

#Tries to establish SSH connection to devices in target_list then runs the commands_file
for target in target_list:
    try:
        net_connect = netmiko.ConnectHandler(
            device_type = "cisco_ios",
            host = target,
            username = user,
            password = secret,
            conn_timeout = 30
        )

        config_changes = net_connect.send_config_from_file("dynamicArp.txt")
        verified_changes = net_connect.send_command("show ip arp inspection interfaces")

        #Creates a file with a unique name and adds the output of verified_changes to the file.
        new_file = target + "_show_ip_arp_inspection.txt"
        with open(new_file, 'a') as new:
            for line in verified_changes:
                new.write(line)
    #IF unable to establish a connection for any reason it will the save the ip address and the error code for further investigation
    except Exception as e:
        error_file = "error_file.txt"
        with open(error_file, 'a') as err:
            err.write(f"{target} {e}\n")

        



