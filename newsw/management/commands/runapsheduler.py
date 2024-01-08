import logging


from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger(__name__)


def my_mails():
    appointments_schedulers = BackgroundScheduler()
    appointments_schedulers.add_job(
    id='send_main',
    func=lambda: print("----", 'hello skillfactory'),
    trigger='interval',
    seconds=5,


)
