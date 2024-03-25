import os


class RpiHost:
    host = os.environ["HOST"]
    database = "hm"
    user = "root"
    pwd = os.environ["MYSQL_PWD"]
    tables = ["financial", "location", "property"]


class RpiHostTest:
    host = os.environ["HOST"]
    database = "hm_test"
    user = "root"
    pwd = os.environ["MYSQL_PWD"]
    tables = ["financial", "location", "property"]


class SshInfo:
    host = os.environ["HOST"]
    user = 'admin'
    pwd = os.environ["SSH_PWD"]
