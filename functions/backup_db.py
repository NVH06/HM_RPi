import paramiko
from classes.database_info_local import RpiHost, RpiHostTest, SshInfo


def database_backup(output_file):
    print("\n-- DB BACKUP FUNCTION INITIATED --")

    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the SSH server
        print("Initiating SSH connection ...")
        ssh_client.connect(SshInfo.host, username=SshInfo.user, password=SshInfo.pwd)

        # Construct the mysqldump command
        print("Creating backup file ...")
        mysqldump_command = f'mysqldump --host={RpiHostTest.host} --user={RpiHostTest.user} --password={RpiHostTest.pwd} {RpiHostTest.database}'

        # Execute the mysqldump command remotely
        _, stdout, _ = ssh_client.exec_command(mysqldump_command)

        # Save the output to a file locally
        with open(output_file, 'w') as file:
            file.write(stdout.read().decode())

        print("Backup completed.")
    except paramiko.AuthenticationException as e:
        print('Authentication failed. Please check your SSH credentials: ', e)
    except paramiko.SSHException as e:
        print('SSH error:', e)
    except paramiko.ChannelException as e:
        print('Error executing command:', e)
    finally:
        # Close the SSH connection
        ssh_client.close()
