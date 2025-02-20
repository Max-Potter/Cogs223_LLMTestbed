import os

import Instructions.instructions as instructions
from Agents.Gemini_Agent import gem_Agent

class trialExecution():
    #agents -- list [] of all agents
    #condition -- condition
    def __init__(self, agents, condition, statements):
        self.agents = agents
        self.condition = condition
        self.instructions = (instructions.conditionInstructions()).conditionDictionary
        self.statements = statements

    def generate_Instruction_Prompt(self, agent):
        instruction_Prompt = self.instructions["InitInstruction"][self.condition] + "\n"
        count = 1
        for observation in agent.context["Observations"]:
            instruction_Prompt += str(count) + ".) " + observation + "\n"
            count += 1
        instruction_Prompt += "\n"
        instruction_Prompt += self.instructions["EvalStatement_Priv"] + "\n"
        count = 1
        for statement in self.statements:
            instruction_Prompt += str(count) + ".) " + statement + "\n"
            count += 1

        response = agent.get_response(instruction_Prompt)
        print("Response:", response)
        ##STORE THESE INTEGER RESPONSES IN PRIVATE EVALUATION --> need to do some regex probably?

    def discussion_1_round1(self, eligible_Agents):
        pass




    def run_1_trial(self):
         ###Flow: Init instruction + observations --> statement instruction + statements --> init rating
    ###  --> discuss instruction --> final rating --> vote
        for agent in self.agents:
            self.generate_Instruction_Prompt(agent)

            





agent1 = gem_Agent(["John went to the beach"])
agent2 = gem_Agent(["John bought 17 watermelons from Albertsons with his Capital One credit card"])
trial = trialExecution([agent1, agent2], "Council", ["John is a cool guy", "John likes to swim in the ocean"])
trial.run_1_trial()