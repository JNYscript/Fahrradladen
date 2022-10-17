import logging
from sty import fg, bg, ef, rs, Style
import colorama
from os.path import exists
import os

colorama.init()


"""
Uses pytohns "logging" and builds ontop to print colorful messages inside the debugger & there destination.
HOW TO USE:
- import: from log import Logger
- init: log = Logger("logfilename","current-moduleName")
- use: log.info("starting module") / log.error("failed to start module")
>> choose from [debug, info, smallwarn, warn, error, critical]
"""


class Logger:
    def __init__(self, logfilename="syslog", log_sendername="no-sender", user="anonym"):
        self.logfilename = str(logfilename)
        self.user = user
        self.log_sendername = str(
            log_sendername
        )  # lib or module the logger is called from

        if not os.path.isdir("./logs/"):
            os.mkdir("./logs/")

        if not exists("./logs/" + self.logfilename + ".log"):
            f = open(self.logfilename + ".log", "w+")
            f.close()

        logging.basicConfig(
            filename="./logs/" + self.logfilename + ".log",
            level=logging.INFO,
            format="%(asctime)s:%(levelname)s:%(message)s",
        )

    def message_formatter(self, message):
        return self.user + " >> [" + self.log_sendername + "] " + str(message)

    def debug(self, message):

        print(
            fg.da_blue + bg.blue + " debug| " + self.message_formatter(message) + rs.all
        )

    def info(self, message):

        logging.info(self.message_formatter(message))
        print(
            fg.da_green
            + bg.li_green
            + " info| "
            + self.message_formatter(message)
            + rs.all
        )

    def smallwarn(self, message):

        logging.warning(self.message_formatter(message))
        print(
            fg.da_grey
            + bg.grey
            + " smallwarn| "
            + self.message_formatter(message)
            + rs.all
        )

    def warn(self, message):

        logging.warning(self.message_formatter(message))
        print(
            fg.da_yellow
            + bg.li_yellow
            + " warn| "
            + self.message_formatter(message)
            + rs.all
        )

    def error(self, message):

        logging.error(self.message_formatter(message))
        print(
            fg.da_red + bg.red + " error| " + self.message_formatter(message) + rs.all
        )

    def critical(self, message, exit_code=True):

        logging.critical(self.message_formatter(message))
        print(
            ef.bold
            + fg.da_red
            + bg.li_red
            + "!critical| "
            + self.message_formatter(message)
            + rs.all
        )

        # Ends Program. @crit no further actions should be allowed without log documentation
        if exit_code:
            exit()


if __name__ == "__main__":

    log = Logger("syslog", "testlib")

    log.debug("This is a Debug-Log Test")
    log.info("This is a Info-Log Test")
    log.smallwarn("This is a Smallwarn-Log Test")
    log.warn("This is a Warn-Log Test")
    log.error("This is a Error-Log Test")
    log.critical("This is a Crit-Log Test")
