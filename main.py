import update, env, lib.requests, lib.logger, lib.requests, lib.timew, time, os, machine
from lib import base64


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


loggerOta = lib.logger.LoggerSimple(time, "OTA")
loggerBoot = lib.logger.LoggerSimple(time, "Boot")

loggerBoot("Booting")

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
    pass
    # updater.update()
except Exception as e:
    log("Failed to OTA update:", e)


import src.Indoor

del loggerBoot
del loggerOta

src.Indoor.start()
