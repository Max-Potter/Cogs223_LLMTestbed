import os
import re

import Instructions.instructions as instructionDoc
import Instructions.statements as statementDoc
import Instructions.observations as observationDoc
from Agents.Gemini_Agent import gem_Agent
import Agents.agentGeneration as agentGen

class trialExecution():
    #agents -- list [] of all agents
    #condition -- condition
    def __init__(self, agents, condition, statements, instructions):
        self.agents = agents
        self.condition = condition
        self.instructions = instructions
        self.statements = statements

    def generate_Instruction_Prompt(self, agent):
        instruction_Prompt = self.instructions["InitInstruction"][agent.condition] + "\n"
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
        #DISCUSSION -- PROMPT IF LLM HAS ANYTHING TO SAY, THEN LET IT RESPOND OR NOT?
        pass




    def run_1_trial(self):
         ###Flow: Init instruction + observations --> statement instruction + statements --> init rating
    ###  --> discuss instruction --> final rating --> vote
        for agent in self.agents:
            self.generate_Instruction_Prompt(agent)


statements = statementDoc.statements
condition = "Hierarchy"
instructions = instructionDoc.conditionDictionary
observations = observationDoc.observationList
agents = agentGen.generate_n_agents(2, "GEMINI", observations, condition)

trial = trialExecution(agents, condition, statements, instructions)
trial.run_1_trial()