"""
The main entry point for salt-api
"""

import logging
import signal

import salt.loader
import salt.utils.process

log = logging.getLogger(__name__)


class RunNetapi(salt.utils.process.SignalHandlingProcess):
    """
    Runner class that's pickable for netapi modules
    """

    def __init__(self, opts, fname, **kwargs):
        super().__init__(**kwargs)
        self.opts = opts
        self.fname = fname

    def run(self):
        netapi = salt.loader.netapi(self.opts)
        netapi_func = netapi[self.fname]
        netapi_func()


class NetapiClient:
    """
    Start each netapi module that is configured to run
    """

    def __init__(self, opts):
        self.opts = opts
        self.process_manager = salt.utils.process.ProcessManager(
            name="NetAPIProcessManager"
        )
        self.netapi = salt.loader.netapi(self.opts)

    def run(self):
        """
        Load and start all available api modules
        """
        if not self.netapi:
            log.error("Did not find any netapi configurations, nothing to start")

        for fun in self.netapi:
            if fun.endswith(".start"):
                log.info("Starting %s netapi module", fun)
                self.process_manager.add_process(
                    RunNetapi, args=(self.opts, fun), name="RunNetapi"
                )

        # Install the SIGINT/SIGTERM handlers if not done so far
        if signal.getsignal(signal.SIGINT) is signal.SIG_DFL:
            # No custom signal handling was added, install our own
            signal.signal(signal.SIGINT, self._handle_signals)

        if signal.getsignal(signal.SIGTERM) is signal.SIG_DFL:
            # No custom signal handling was added, install our own
            signal.signal(signal.SIGTERM, self._handle_signals)

        self.process_manager.run()

    def _handle_signals(self, signum, sigframe):  # pylint: disable=unused-argument
        # escalate the signals to the process manager
        self.process_manager.stop_restarting()
        self.process_manager.send_signal_to_processes(signum)
        # kill any remaining processes
        self.process_manager.kill_children()
