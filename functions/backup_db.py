import paramiko
import subprocess
from classes.database_info_rpi import RpiHost, RpiHostTest, SshInfo
# from classes.database_info_local import RpiHost, RpiHostTest, SshInfo


def database_backup_rpi(output_file):
    print("Creating backup of database...")

    # Identify the Docker container running MySQL
    container_cmd = subprocess.run(['docker', 'ps', '--filter', 'ancestor=mysql/mysql-server:5.7', '--format', '{{.ID}}'],
                                   capture_output=True, text=True, check=True)
    container_id = container_cmd.stdout.strip()

    if not container_id:
        print("MySQL Docker container not found.")
        print("DB backup aborted.")
        return

    # Construct the mysqldump command to run inside the Docker container
    print("Creating backup file ...")
    mysqldump_cmd = [
        'docker', 'exec', container_id,
        'mysqldump', f'--user={RpiHostTest.user}', f'--password={RpiHostTest.pwd}', RpiHostTest.database
    ]

    # Save the output to a file locally
    with open(output_file, 'w') as file:
        sql_file = subprocess.run(mysqldump_cmd, stdout=file, text=True, check=True)

    print("Backup completed.")

    return


def database_backup_local(output_file):
    print("\n-- DB BACKUP FUNCTION INITIATED --")

    # Create an SSH client
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the SSH server
        print("Initiating SSH connection ...")
        ssh_client.connect(SshInfo.host, username=SshInfo.user, password=SshInfo.pwd)

        # Identify the Docker container running MySQL
        print("Identifying Docker container running MySQL ...")
        stdin, stdout, stderr = ssh_client.exec_command('docker ps --filter "ancestor=mysql" --format "{{.ID}}"')
        container_id = stdout.read().decode().strip()

        if not container_id:
            print("MySQL Docker container not found.")
            print("DB backup aborted.")
            return

        # Construct the mysqldump command to run inside the Docker container
        print("Creating backup file ...")
        mysqldump_command = (
            f'docker exec {container_id} '
            f'mysqldump --user={RpiHost.user} --password={RpiHost.pwd} {RpiHost.database}'
        )

        # Execute the mysqldump command remotely
        _, stdout, _ = ssh_client.exec_command(mysqldump_command)

        # Save the output to a file locally
        with open(output_file, 'w') as file:
            backup_data = stdout.read().decode()
            file.write(backup_data)

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

    return