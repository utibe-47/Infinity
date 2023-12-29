import os
from os.path import join
import sys
import socket
from getpass import getuser
from importlib import util


env = os.getenv('SINGULARITY_ENV', 'dev')
override_config_dir = os.getenv('CONFIG_DIR_OVERRIDE', None)
user = 'None' if bool(getuser()) is False else getuser()

if user == "PROD_ARP" or (env == 'prod' and 'U' not in user):
    if override_config_dir is None or not bool(override_config_dir):
        if socket.gethostname() == "AWEBSAPPW03P":
            if env != 'prod':
                config_dir = r'E:\prod_arp\Singularity\Configuration\Test'
            else:
                config_dir = r'E:\prod_arp\Singularity\Configuration\Production'
        else:
            config_dir = r'E:\prod_arp\Singularity\Configuration\Production'
    else:
        config_dir = os.getenv('CONFIG_DIR', None)
else:
    _dir = os.getenv('CONFIG_DIR', None)
    if _dir is None:
        if override_config_dir is None or not bool(override_config_dir):
            config_dir = r'N:\multi_mg\LDN\ARP\execution\configuration\Test'
        else:
            config_dir = r'C:\Dev\ARP\execution_temp\configuration\Test'
    else:
        if override_config_dir is None or not bool(override_config_dir):
            config_dir = _dir
        else:
            config_dir = r'C:\Dev\ARP\execution_temp\configuration\Test'

os.environ["CONFIG_DIR"] = config_dir
sys.path.append(config_dir)

try:
    cantab_execution = __import__('config_cantab_execution')
except ImportError:
    spec = util.spec_from_file_location("module.name", join(config_dir, 'config_cantab_execution.py'))
    cantab_execution = util.module_from_spec(spec)
    spec.loader.exec_module(cantab_execution)

try:
    execution = __import__('config_execution')
except ImportError:
    spec = util.spec_from_file_location("module.name", join(config_dir, 'config_execution.py'))
    execution = util.module_from_spec(spec)
    spec.loader.exec_module(execution)

try:
    thinkfolio_execution = __import__('config_thinkfolio_execution')
except ImportError:
    spec = util.spec_from_file_location("module.name", join(config_dir, 'config_thinkfolio_execution.py'))
    thinkfolio_execution = util.module_from_spec(spec)
    spec.loader.exec_module(thinkfolio_execution)

try:
    config_local = __import__('config_local')
except ImportError:
    spec = util.spec_from_file_location("module.name", join(config_dir, 'config_local.py'))
    config_local = util.module_from_spec(spec)
    spec.loader.exec_module(config_local)


BASEDIR = os.path.dirname(os.path.dirname(__file__))
BASEDIR_RESULTS = join(BASEDIR, 'results')

THINKFOLIO_STRATEGY_RESULTS_PATH = thinkfolio_execution.THINKFOLIO_STRATEGY_RESULTS_PATH
THINKFOLIO_TARGET_POSITIONS_PATH = thinkfolio_execution.THINKFOLIO_TARGET_POSITIONS_PATH
THINKFOLIO_LOGS_PATH = thinkfolio_execution.THINKFOLIO_LOGS_PATH
THINKFOLIO_FEEDBACK_PATH = thinkfolio_execution.THINKFOLIO_FEEDBACK_PATH
THINKFOLIO_CHECKS_PATH = thinkfolio_execution.THINKFOLIO_CHECKS_PATH
BETA_CONSTRAINT_PATH = thinkfolio_execution.BETA_CONSTRAINT_PATH
CORREL_CONSTRAINT_PATH = thinkfolio_execution.CORREL_CONSTRAINT_PATH
EXPOSURE_CONSTRAINT_PATH = thinkfolio_execution.EXPOSURE_CONSTRAINT_PATH
VOL_CONSTRAINT_PATH = thinkfolio_execution.VOL_CONSTRAINT_PATH
VAR_CONSTRAINT_PATH = thinkfolio_execution.VAR_CONSTRAINT_PATH
DRAWDOWN_CONSTRAINT_PATH = thinkfolio_execution.DRAWDOWN_CONSTRAINT_PATH
PORTFOLIO_CONSTRAINT_PATH = thinkfolio_execution.PORTFOLIO_CONSTRAINT_PATH
CHECKS_CONSTRAINT_PATH = thinkfolio_execution.CHECKS_CONSTRAINT_PATH
BACKTEST_CONSTRAINT_PATH = thinkfolio_execution.BACKTEST_CONSTRAINT_PATH
BACKTEST_FREQUENCY = thinkfolio_execution.BACKTEST_FREQUENCY
USE_PROXY_VOL_RATIO = thinkfolio_execution.USE_PROXY_VOL_RATIO
THINKFOLIO_STRATEGY_STORAGE_PATH = thinkfolio_execution.THINKFOLIO_STRATEGY_STORAGE_PATH
THINKFOLIO_ALLOCATION_STORAGE_PATH = thinkfolio_execution.THINKFOLIO_ALLOCATION_STORAGE_PATH


META_STRATEGY_DATA_INPUT_PATH = execution.META_STRATEGY_DATA_INPUT_PATH
STRATEGY_DATA_INPUT_PATH = execution.STRATEGY_DATA_INPUT_PATH
META_STRATEGY_DATA_OUTPUT_PATH = execution.META_STRATEGY_DATA_OUTPUT_PATH
STRATEGY_DATA_OUTPUT_PATH = execution.STRATEGY_DATA_OUTPUT_PATH
MIN_VAR_TICKER_PATH = execution.MIN_VAR_TICKER_PATH


POSITIONS_OUTPUT_PATH = config_local.POSITIONS_OUTPUT_PATH
TEMP_EXECUTION_PATH = config_local.TEMP_EXECUTION_PATH
ABS_PATH_RESULTS = config_local.ABS_PATH_RESULTS
ABS_EXECUTION_PATH_RESULTS = config_local.ABS_EXECUTION_PATH_RESULTS
ABS_ALLOCATION_PATH_RESULTS = config_local.ABS_ALLOCATION_PATH_RESULTS
basedir_singularity = config_local.basedir_singularity


FILE_NAME_DATETIME_OUTPUT_PREFIX = cantab_execution.FILE_NAME_DATETIME_OUTPUT_PREFIX
FILE_NAME_OUTPUT_EXTENSION = cantab_execution.FILE_NAME_OUTPUT_EXTENSION
CANTAB_EXECUTION_INPUT_PATH = cantab_execution.CANTAB_EXECUTION_INPUT_PATH
CANTAB_EXECUTION_OUTPUT_PATH = cantab_execution.CANTAB_EXECUTION_OUTPUT_PATH
ARP_TRADING_OUTPUT_PATH = cantab_execution.ARP_TRADING_OUTPUT_PATH
CANTAB_POLLING_FOLDER = cantab_execution.CANTAB_POLLING_FOLDER
BASEDIR_EXECUTION_COMPARATOR_INPUT = cantab_execution.BASEDIR_EXECUTION_COMPARATOR_INPUT
BASEDIR_EXECUTION_COMPARATOR_EXISTING_INPUT = cantab_execution.BASEDIR_EXECUTION_COMPARATOR_EXISTING_INPUT
BASEDIR_EXECUTION_COMPARATOR_TRADE_INPUT = cantab_execution.BASEDIR_EXECUTION_COMPARATOR_TRADE_INPUT
BASEDIR_EXECUTION_COMPARATOR_OUTPUT = cantab_execution.BASEDIR_EXECUTION_COMPARATOR_OUTPUT
