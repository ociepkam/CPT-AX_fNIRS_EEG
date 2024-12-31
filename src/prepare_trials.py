import random
from psychopy import visual


def prepare_trials(trials_dict, win, config):
    trials = [{"first":  visual.TextStim(win, color=config["stimulus_color"], text=k.split("-")[0], height=config["stimulus_size"]),
               "second": visual.TextStim(win, color=config["stimulus_color"], text=k.split("-")[1], height=config["stimulus_size"]),
               "stimulus": k}
              for k, v in trials_dict.items() for _ in range(v)]
    random.shuffle(trials)
    return trials
