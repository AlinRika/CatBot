import logging

logging.basicConfig(
    level=logging.INFO,
    filename='bot_log.log',
    format='%(levelname)s => %(message)s => %(asctime)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

main_formatter = logging.Formatter(
    '%(levelname)s => %(message)s'
)


class ProgressFileHandler(logging.FileHandler):
    """
    A handler class which allows the cursor to stay on
    one line for selected messages
    """
    on_same_line = False

    def __init__(self):
        super().__init__(filename='bot_log.log', mode='w')

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            same_line = hasattr(record, 'same_line')
            if self.on_same_line and not same_line:
                stream.write(self.terminator)
            stream.write(msg)
            if same_line:
                stream.write('... ')
                self.on_same_line = True
            else:
                stream.write(self.terminator)
                self.on_same_line = False
            self.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


class TestFilter(logging.Filter):
    def filter(self, record):
        return record.msg.lower().find('cat') == -1


logger = logging.getLogger()

progress = ProgressFileHandler()
progress.setLevel(logging.DEBUG)
progress.setFormatter(main_formatter)

logger.addHandler(progress)
logger.addFilter(TestFilter())
