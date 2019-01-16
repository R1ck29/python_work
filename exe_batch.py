#! python3
# coding: UTF-8

import paramiko

k = paramiko.RSAKey.from_private_key_file("key_name.key")
c = paramiko.SSHClient()
c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("connecting")
c.connect(hostname="", username="", pkey=k)
print("connected")

ssh_command = 'ssh -t -t admin@192.168.2.65'

"""
#method 1
ini = c.invoke_shell()
print(ini.send('ls'))
print(ini.recv(1024))



ssh_command = 'ssh -t -t admin@192.168.2.65'

print("connecting")
c.exec_command(ssh_command)
print("connected")

test_command = 'ls'
print(c.exec_command(test_command))
"""
c = paramiko.SSHClient()
c.load_system_host_keys()
try:
    c.connect(hostname="192.168.2.65", username="", password="")

    command = 'ls'
    print("Executing {}".format(command))
    stdin, stdout, stderr = c.exec_command(command)
    print(stdout.readlines())
    print("Errors")
    print(stderr.readlines())

finally:
    c.close()

