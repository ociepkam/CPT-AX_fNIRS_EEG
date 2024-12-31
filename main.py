import atexit
from psychopy import visual, event, core
from os.path import join
import random
import datetime

from src.screen_misc import get_screen_res
from src.check_exit import check_exit
from src.load_data import load_config
from src.show_info import show_info, part_info
from src.prepare_trials import prepare_trials

PART_ID = ""
TRAINING_ANSWER = ""
TRAINING_CORRECT = ""
EXPERIMENT_ANSWER = ""
EXPERIMENT_CORRECT = ""


@atexit.register
def save_results():
    current_datetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'{PART_ID}_{current_datetime}.txt'
    with open(join('results', file_name), 'w', newline='') as file:
        file.write(f"training answer: {TRAINING_ANSWER}")
        file.write(f"training correct: {TRAINING_CORRECT}\n")
        file.write(f"experiment answer: {EXPERIMENT_ANSWER}")
        file.write(f"experiment correct: {EXPERIMENT_CORRECT}\n")


def draw_stimulus(stimulus, clock, win, stimulus_time):
    stimulus.setAutoDraw(True)
    win.callOnFlip(clock.reset)
    win.flip()
    while clock.getTime() < stimulus_time:
        check_exit()
    stimulus.setAutoDraw(False)


def experiment_loop(win, config, block_type, screen_res, clock, fixation, textbox, textbox_info):
    global TRAINING_ANSWER, TRAINING_CORRECT, EXPERIMENT_ANSWER, EXPERIMENT_CORRECT
    trials = prepare_trials(trials_dict=config[f"{block_type}_trials"], win=win, config=config)
    show_info(win=win, file_name=join("messages", f"{block_type}.txt"), text_size=config["text_size"],
              text_color=config["text_color"], screen_res=screen_res)

    for idx, trial in enumerate(trials):
        if config["first_fixation"] and idx == 0 and block_type == "experiment":
            fixation_time = config["first_fixation_time"]
        else:
            fixation_time = random.uniform(config[f"{block_type}_fixation_time"][0], config[f"{block_type}_fixation_time"][1])
        draw_stimulus(stimulus=fixation, clock=clock, win=win, stimulus_time=fixation_time)
        draw_stimulus(stimulus=trial["first"], clock=clock, win=win, stimulus_time=config[f"{block_type}_first_time"])
        draw_stimulus(stimulus=trial["second"], clock=clock, win=win, stimulus_time=config[f"{block_type}_second_time"])

    textbox.setText("")
    win.callOnFlip(event.clearEvents)
    while True:
        textbox_info.draw()
        textbox.draw()
        win.flip()
        keys = event.getKeys()
        if config["textbox_key"] in keys:
            if block_type == "training":
                TRAINING_ANSWER = textbox.text
                TRAINING_CORRECT = config["training_trials"][config["target"]]
            else:
                EXPERIMENT_ANSWER = textbox.text
                EXPERIMENT_CORRECT = config["experiment_trials"][config["target"]]
            break
        if len(textbox.text) > config["textbox_max_size"]:
            textbox.text = textbox.text[:config["textbox_max_size"]]


def main():
    global PART_ID
    config = load_config()
    info, PART_ID = part_info()

    screen_res = dict(get_screen_res())
    win = visual.Window(list(screen_res.values()), fullscr=True, monitor='testMonitor', units='pix', screen=0,
                        color=config["screen_color"])
    event.Mouse(visible=False)
    clock = core.Clock()
    fixation = visual.TextStim(win, color=config["fixation_color"], text=config["fixation_text"], height=config["fixation_size"])
    textbox = visual.TextBox2(win, text="", editable=True, borderWidth=config["textbox_border_width"], color=config["text_color"],
                              letterHeight=config["text_size"], pos=config["textbox_pos"], borderColor=config["text_color"],
                              size=config["textbox_size"], alignment='center')
    textbox_info = visual.TextStim(win, color=config["text_color"], text=config["textbox_info_text"],
                                   height=config["text_size"], pos=config["textbox_info_pos"])

    # --------------------------------------- procedure ---------------------------------------
    # training
    if config["training"]:
        experiment_loop(win=win, config=config, block_type="training", screen_res=screen_res, clock=clock, fixation=fixation, textbox=textbox,
                        textbox_info=textbox_info)

    # experiment
    experiment_loop(win=win, config=config, block_type="experiment", screen_res=screen_res, clock=clock, fixation=fixation, textbox=textbox,
                    textbox_info=textbox_info)

    # end screen
    show_info(win=win, file_name=join("messages", "end.txt"), text_size=config["text_size"], text_color=config["text_color"], screen_res=screen_res)


if __name__ == "__main__":
    main()
