""" 개인 학습용이며 인터넷에 공개할 수 없습니다.
©2022 HongLab, Inc. All Rights Reserved

This is a simple modification of ParlAI interactive script written by Jeong-Mo Hong for educational purposes.
https://github.com/facebookresearch/ParlAI/blob/main/parlai/scripts/interactive.py
"""

from parlai.core.params import ParlaiParser
from parlai.core.agents import create_agent
from parlai.core.worlds import create_task
from parlai.utils.world_logging import WorldLogger
from parlai.agents.local_human.local_human import LocalHumanAgent
import parlai.utils.logging as logging


def setup_args(model_file, parser=None):
    if parser is None:
        parser = ParlaiParser(
            True, True, "Interactive chat with a model on the command line"
        )
    parser.add_argument("-d", "--display-examples", type="bool", default=False)
    parser.add_argument(
        "--display-prettify",
        type="bool",
        default=False,
        help="Set to use a prettytable when displaying "
        "examples with text candidates",
    )
    parser.add_argument(
        "--display-add-fields",
        type=str,
        default="",
        help='Display these fields when verbose is off (e.g., "--display-add-fields label_candidates,beam_texts")',
    )
    parser.add_argument(
        "-it",
        "--interactive-task",
        type="bool",
        default=True,
        help="Create interactive version of task",
    )
    parser.add_argument(
        "--outfile",
        type=str,
        default="",
        help="Saves a jsonl file containing all of the task examples and "
        "model replies. Set to the empty string to not save at all",
    )
    parser.add_argument(
        "--save-format",
        type=str,
        default="conversations",
        choices=["conversations", "parlai"],
        help="Format to save logs in. conversations is a jsonl format, parlai is a text format.",
    )
    parser.set_defaults(model_file=model_file)
    parser.set_defaults(display_prettify=True)

    parser.set_defaults(interactive_mode=True, task="interactive")
    LocalHumanAgent.add_cmdline_args(parser, partial_opt=None)
    WorldLogger.add_cmdline_args(parser, partial_opt=None)
    return parser


class MyChatbot:
    def __init__(self, model_file="zoo:blender/blender_90M/model"):
        self.parser = setup_args(model_file)
        self.opt = self.parser.parse_args(None)

        if isinstance(self.opt, ParlaiParser):
            logging.error("interactive should be passed opt not Parser")
            self.opt = self.opt.parse_args()

        # Create model and assign it to the specified task
        self.agent = create_agent(self.opt, requireModelExists=True)
        self.agent.opt.log()
        self.human_agent = LocalHumanAgent(self.opt)
        # set up world logger
        # world_logger = WorldLogger(self.opt) if self.opt.get("outfile") else None
        self.world = create_task(self.opt, [self.human_agent, self.agent])

    def talk_to_ai(self, user_input):
        reply = {"episode_done": False, "text": user_input}
        self.agent.observe(reply)
        model_res = self.agent.act()
        return model_res["text"]
