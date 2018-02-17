import daemon
import pwd
import time
import lockfile
from gw2ahmonitor.monitor.monitor import Monitor

user_name = "gw2-ah-monitor"
user_group = "gw2-ah-monitor"
root_dir = "/var/lib/gw2-ah-monitor"
pidlock_file = "/var/lib/gw2-ah-monitor/pidlock"

def get_prices():
    monitor = Monitor()
    monitor.refresh_and_store()

def run_main_loop():
    while True:
        time.sleep(60)
        get_prices()

def run_daemon():
    userinfo = pwd.getpwnam(user_name)
    uid = userinfo.pw_uid
    gid = userinfo.pw_gid

    try:
        with daemon.DaemonContext(
                working_directory=root_dir,
                uid=uid,
                gid=gid,
                umask=0o002,
                pidfile=lockfile.FileLock(pidlock_file)
                ):
            run_main_loop()
    except BaseException as e:
        print(e)

if __name__ == "__main__":
    run_daemon()
