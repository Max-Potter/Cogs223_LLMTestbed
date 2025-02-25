import os
import re
import pandas as pd
import datetime
import json

from HelperFuncs.regexExtractions import get_integer_ratings, get_date_now, get_average_vote
import Instructions.instructions as instructionDoc
import Instructions.statements as statementDoc
import Instructions.observations as observationDoc
from Agents.Gemini_Agent import gem_Agent
import Agents.agentGeneration as agentGen

class trialExecution():
    #agents -- list [] of all agents
    #condition -- condition
    def __init__(self, condition, agentType, numAgents = 6):
        #self.agents = agents
        self.agentType = agentType
        self.numAgents = numAgents
        self.statements = statementDoc.statements
        self.instructions = instructionDoc.conditionDictionary
        self.observations = observationDoc.observationList

        self.condition = condition
        self.agents = agentGen.generate_n_agents(self.numAgents, self.agentType, self.observations, self.condition)
        self.finalVote = []
        

    def reinit(self, condition = None, agentType = None, numAgents = None):
        if condition != None:
            self.condition = condition
        if agentType != None:
            self.agentType = agentType
        if numAgents != None:
            self.numAgents = numAgents
        self.agents = agentGen.generate_n_agents(self.numAgents, self.agentType, self.observations, self.condition)
        self.finalVote = {}

    def format_Data_for_Export(self):
        
       
        #dataDictionary = {
        #condition = pd.Series([self.condition], name = 'condition'),
        #agentType = pd.Series([self.agentType], name = 'agentType'),
        #initEvals = pd.Series([[list(agent.context["Initial Evaluations"].values()) for agent in self.agents]], name = 'initialEvals'),
        #finalEvals = pd.Series([[list(agent.context["Final Evaluations"].values()) for agent in self.agents]], name = 'finalEvals'),
        #groupDecision = pd.Series([self.finalVote], name='groupDecision'),
        #agentContext = pd.Series([[agent.context for agent in self.agents]], name = 'agentContext'),
        #}
        dataDictionary = {
            'condition': self.condition,
            'agentType': self.agentType,
            'initEvals': [list(agent.context["Initial Evaluations"].values()) for agent in self.agents],
            'finalEvals': [list(agent.context["Final Evaluations"].values()) for agent in self.agents],
            'groupDecision': self.finalVote,
            'agentContext': [agent.context for agent in self.agents],
        }
        #record = [
        #          [self.condition], 
        #          [self.agentType], 
        #          [agent.context["Observations"] for agent in self.agents],
        #          [list(agent.context["Initial Evaluations"].values()) for agent in self.agents], 
        #          [list(agent.context["Final Evaluations"].values()) for agent in self.agents],
        #          [self.finalVote],
                  #[agent.context for agent in self.agents],
        #          ]
        #i = 1
        #for entry in record:
        #    print(i)
        #    print(entry)
        #    i += 1
            
        #print(record[6], len(record))
        #columnNames = [
        #    'condition',
        #    'agentType',
        #    'agentObservations',
        #    'initEvals',
        #    'finalEvals',
        #    'finalVote',
        #    'catch',
            #'context',
        #]

        #supplementaryData = {"Agent " + str(i): self.agents[i].context for i in range(len(self.agents))}
        #supplementaryData = pd.DataFrame([agent.context for agent in self.agents])
        #dataDictionary = pd.json_normalize(dataDictionary)
        #dataDF = pd.concat([condition, agentType, initEvals, finalEvals, groupDecision, agentContext], axis=1)
        #dataDF = pd.DataFrame.from_dict(dataDictionary)
        #dataDF = pd.DataFrame.from_records(record, columns = columnNames)
        #dataDF = dataDF.transpose
        #suppDataDF = pd.DataFrame(supplementaryData)
        
        return dataDictionary #suppDataDF


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
            prompt = """You will now all collectively vote for the final ratings of each statement. The decision will be the average of all your votes. Please vote for the likelihood of each statement now."""
            for agent in self.agents:
                agent.update_Context(prompt)
            i = 0
            allVotes = []
            for agent in self.agents:
                votingAgent = self.agents[i]
                other_agents = self.agents[:i]+self.agents[i+1:]
                prompt = "\n It is now your turn to vote. Respond ONLY with integers between 0 and 10 to rate the likelihood of each statement, and separate each integer with a space.\n"
                response = votingAgent.get_response(prompt + " You are Person " + str(i))
                formattedResponse = "Person " + str(i) + "'s response: " + response
                statementRatings = get_integer_ratings(self.statements, response)
                vote = list(statementRatings.values())
                allVotes.append(vote)
                #self.finalVote["Person " + str(i)] = statementRatings

                for agent in other_agents:
                    agent.update_Context(formattedResponse)
                i += 1
            averageVotes = get_average_vote(allVotes)
            self.finalVote = averageVotes









    def run_1_trial(self):
         ###Flow: Init instruction + observations --> statement instruction + statements --> init rating
    ###  --> discuss instruction --> final rating --> vote
        for agent in self.agents:
            self.generate_Instruction_Prompt(agent)

        self.discussion()
        self.get_final_ratings()
        self.get_final_vote_by_condition()
        #print(self.finalVote)
        data = self.format_Data_for_Export()
        return data
    
    def run_n_trials(self, n, testTrial = False):
        fileName = ""
        if testTrial:
            fileName += "TESTRUN_"
        now = get_date_now()
        fileName += now + "_" + str(self.condition) + ".csv"
        
        records = []
        for i in range(n):
            newData = self.run_1_trial()
            records.append(newData)
            self.reinit()

           
        columnNames = [
            'condition',
            'agentType',
            'initEvals',
            'finalEvals',
            'groupDecision',
            'agentContext',
        ]
        df = pd.DataFrame.from_records(records, columns = columnNames)
        df.to_csv(fileName, encoding='utf-8', index=False)
        #suppDf.to_csv("Supplementary_" + fileName, encoding='utf-8', index=False)
        return
        



condition = "Council"


trial = trialExecution(condition, "GEMINI", numAgents=2)
trial.run_n_trials(2, testTrial = True)
