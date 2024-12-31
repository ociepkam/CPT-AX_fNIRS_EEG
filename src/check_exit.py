from psychopy import event, logging


def check_exit(key='f7'):
    stop = event.getKeys(keyList=[key])
    if len(stop) > 0:
        logging.critical('Experiment finished by user! {} pressed.'.format(key))
        exit(1)
