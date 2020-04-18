from notify_run import Notify

notify = Notify()
notify.register()
notify.send("Hi there!")
notify.send('Click to open noitfy.run!', 'https://notify.run')
