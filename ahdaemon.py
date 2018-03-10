import daemon
import pwd
import schedule
import time
import lockfile
import sys
from gw2ahmonitor.helpers.logging import LoggingHelper
from gw2ahmonitor.helpers.exception import format_exception
from gw2ahmonitor.monitor.datarefresh import PriceMonitor, ItemListMaintainer

user_name = "gw2-ah-monitor"
user_group = "gw2-ah-monitor"
root_dir = "/var/lib/gw2-ah-monitor"
pidlock_file = "/var/lib/gw2-ah-monitor/pidlock"

def get_prices():
    monitor = PriceMonitor()
    monitor.refresh_and_store()

def maintain_items_data_cache():
    monitor = ItemListMaintainer()
    monitor.refresh_and_store()

def run_main_loop():
    LoggingHelper.init_logging()
    LoggingHelper.info("Daemon started...")

    schedule.every().minute.do(get_prices)
    schedule.every().day.do(maintain_items_data_cache)
    # schedule.every().hour.do(aggregate_minute_prices())
    # schedule.every().week.do(release_old_minute_data())


    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            # LoggingHelper.error(format_exception(e))
            raise

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
        raise

if __name__ == "__main__":
    run_daemon()
