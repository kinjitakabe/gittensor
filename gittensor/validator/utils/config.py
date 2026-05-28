import os

import bittensor as bt

VALIDATOR_WAIT = 60  # 60 seconds
VALIDATOR_STEPS_INTERVAL = 120  # 2 hours, every time a scoring round happens

# required env vars
GITTENSOR_VALIDATOR_PAT = os.getenv('GITTENSOR_VALIDATOR_PAT')
WANDB_API_KEY = os.getenv('WANDB_API_KEY')
WANDB_PROJECT = os.getenv('WANDB_PROJECT', 'gittensor-validators')
WANDB_VALIDATOR_NAME = os.getenv('WANDB_VALIDATOR_NAME', 'vali')

# optional env vars
STORE_DB_RESULTS = os.getenv('STORE_DB_RESULTS', 'false').lower() == 'true'

# log values
bt.logging.info(f'VALIDATOR_WAIT: {VALIDATOR_WAIT}')
bt.logging.info(f'VALIDATOR_STEPS_INTERVAL: {VALIDATOR_STEPS_INTERVAL}')
bt.logging.info(f'WANDB_PROJECT: {WANDB_PROJECT}')


# DEV_MODE disables the maintainer anti-gaming gates, so honor it only on dev networks.
DEV_MODE_NETWORKS = frozenset({'local', 'test'})


def resolve_dev_mode(network: str) -> bool:
    """Whether DEV_MODE bypasses apply, forcing them off outside dev networks.

    The maintainer gates read DEV_MODE from the environment directly, so on a non-dev
    network we clear the stray variable to keep those gates enabled even if an operator
    left DEV_MODE set.
    """
    if not os.environ.get('DEV_MODE'):
        return False
    if network in DEV_MODE_NETWORKS:
        return True
    bt.logging.error(
        f'DEV_MODE is set on network={network!r}; ignoring it so maintainer anti-gaming gates stay active '
        '(DEV_MODE is only honored on local/test).'
    )
    os.environ.pop('DEV_MODE', None)
    return False
