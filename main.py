import update, env, lib.requests, lib.logger, lib.requests, lib.timew, time, os, machine
from lib import base64

t = lib.timew.Time(time=time)

# Configure Logger
# logger = lib.logger.config(
#     enabled=env.settings["debug"],
#     include=env.settings["logInclude"],
#     exclude=env.settings["logExclude"],
#     time=t,
# )
# log = logger(append="boot")
# log("The current time is %s" % t.human())

# loggerOta = logger(append="OTAUpdater")


loggerBoot = lib.logger.LoggerSimple(time, "Boot")

loggerBoot("Booting", 4)


logger = lib.logger.config(
    enabled=env.settings["debug"],
    include=env.settings["logInclude"],
    exclude=env.settings["logExclude"],
    time=t,
)
log = logger(append="boot")
log("The current time is %s" % t.human())

loggerOta = logger(append="OTAUpdater")


io = update.IO(os=os, logger=loggerOta)
github = update.GitHub(
    io=io,
    remote=env.settings["githubRemote"],
    branch=env.settings["githubRemoteBranch"],
    logger=loggerOta,
    requests=lib.requests,
    username=env.settings["githubUsername"],
    token=env.settings["githubToken"],
    base64=base64,
)
updater = update.OTAUpdater(io=io, github=github, logger=loggerOta, machine=machine)

try:
    updater.update()
except Exception as e:
    loggerBoot("Failed to OTA update:", e)

del loggerBoot
del loggerOta
del io
del github
del updater

import src.Indoor


src.Indoor.start()
