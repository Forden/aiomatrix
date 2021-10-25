import logging

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

dispatcher = logging.getLogger('aiomatrix.dispatcher')
client = logging.getLogger('aiomatrix.client')
