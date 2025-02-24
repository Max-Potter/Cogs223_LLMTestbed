import os
import re

from HelperFuncs.regexExtractions import get_integer_ratings
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
        self.finalVote = {}

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
        
        statementRatings = get_integer_ratings(self.statements, response)
        agent.set_InitialEvaluations(statementRatings)
        

    def discussion(self, rounds = 2):
        if self.condition == "Council":
            eligible_agents = self.agents
            discussion_Prompt = "\n" + self.instructions["DiscussInstruction"]["Council"] +"\n"
            for agent in eligible_agents:
                agent.update_Context(discussion_Prompt)
            for round in range(rounds):
                print("Round " + str(round+1))
                prompt = "It is your turn to speak"
                for i in range(len(eligible_agents)):
                    turn_at_talk_agent = eligible_agents[i]
                    other_agents = eligible_agents[:i]+eligible_agents[i+1:]

                    response = turn_at_talk_agent.get_response(prompt + ". You are Person " + str(i))
                    formattedResponse = "\n" + "Person " + str(i) + "'s response: " + response
                    for agent in other_agents:
                        agent.update_Context(formattedResponse)


    def get_final_ratings(self):
        instruction_Prompt = self.instructions["EvalStatement_Priv"] + "\n"
        count = 1
        for statement in self.statements:
            instruction_Prompt += str(count) + ".) " + statement + "\n"
            count += 1
        for agent in self.agents:
            response = agent.get_response(instruction_Prompt)
        
            statementRatings = get_integer_ratings(self.statements, response)
            agent.set_FinalEvaluations(statementRatings)

    def get_final_vote_by_condition(self):
        if self.condition == "Council":
            prompt = """You will now all collectively vote for the final ratings of each statement. The decision will be by majority vote. Please vote for the likelihood of each statement now."""
            for agent in self.agents:
                agent.update_Context(prompt)
            i = 0
            for agent in self.agents:
                votingAgent = self.agents[i]
                other_agents = self.agents[:i]+self.agents[i+1:]
                prompt = "\n It is now your turn to vote. Respond ONLY with integers between 0 and 10 to rate the likelihood of each statement, and separate each integer with a space.\n"
                response = votingAgent.get_response(prompt + " You are Person " + str(i))
                formattedResponse = "Person " + str(i) + "'s response: " + response
                statementRatings = get_integer_ratings(self.statements, response)
                self.finalVote["Person " + str(i)] = statementRatings

                for agent in other_agents:
                    agent.update_Context(formattedResponse)
                i += 1





    def run_1_trial(self):
         ###Flow: Init instruction + observations --> statement instruction + statements --> init rating
    ###  --> discuss instruction --> final rating --> vote
        for agent in self.agents:
            self.generate_Instruction_Prompt(agent)

        self.discussion()
        self.get_final_ratings()
        self.get_final_vote_by_condition()
        print(self.finalVote)


statements = statementDoc.statements
condition = "Council"
instructions = instructionDoc.conditionDictionary
observations = observationDoc.observationList
agents = agentGen.generate_n_agents(2, "GEMINI", observations, condition)

trial = trialExecution(agents, condition, statements, instructions)
trial.run_1_trial()
print(agents[0].context["Context"])