import os

import Instructions.instructions
from Agents.Gemini_Agent import gem_Agent

class trialExecution():
    #agents -- list [] of all agents
    #condition -- condition
    def __init__(self, agents, condition):
        self.agents = agents
        self.condition = condition

    def run_1_trial(self):
        for agent in self.agents:
            pass




