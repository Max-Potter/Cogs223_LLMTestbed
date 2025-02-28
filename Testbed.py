import os
import re
import pandas as pd
import datetime
import json
import numpy as np
import math
import operator

from HelperFuncs.regexExtractions import get_integer_ratings, get_date_now, get_average_vote, get_Voted_Person
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
        self.additionalInfo = None
        self.agents = agentGen.generate_n_agents(self.numAgents, self.agentType, self.observations, self.condition)
        self.finalVote = []
        

    def reinit(self, condition = None, agentType = None, numAgents = None):
        if condition != None:
            self.condition = condition
        if agentType != None:
            self.agentType = agentType
        if numAgents != None:
            self.numAgents = numAgents

        self.additionalInfo = None
        self.agents = agentGen.generate_n_agents(self.numAgents, self.agentType, self.observations, self.condition)
        self.finalVote = {}



    def format_Data_for_Export(self):
    
        dataDictionary = {
            'condition': self.condition,
            'agentType': self.agentType,
            'observations': [agent.context['Observations'] for agent in self.agents],
            'initEvals': [list(agent.context["Initial Evaluations"].values()) for agent in self.agents],
            'finalEvals': [list(agent.context["Final Evaluations"].values()) for agent in self.agents],
            'groupDecision': self.finalVote,
            'additionalInfo': self.additionalInfo,
            #'agentContext': [agent.context['Context'] for agent in self.agents],
        }
        
        
        
        return dataDictionary 


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
            discussion_Prompt = "\n" + self.instructions["DiscussInstruction"][self.condition] +"\n"
            for agent in eligible_agents:
                agent.update_Context(discussion_Prompt)
            for round in range(rounds):
                print("Round " + str(round+1))
                prompt = "It is your turn to speak"
                for i in range(len(eligible_agents)):
                    turn_at_talk_agent = eligible_agents[i]
                    other_agents = eligible_agents[:i]+eligible_agents[i+1:]

                    response = turn_at_talk_agent.get_response(prompt + ". You are " + turn_at_talk_agent.name)
                    formattedResponse = "\n" + turn_at_talk_agent.name + "'s response: " + response
                    for agent in other_agents:
                        agent.update_Context(formattedResponse)

        elif self.condition == "Community":
            agents_per_community = math.floor(self.numAgents/2)
            indicesSelected = np.random.choice(self.numAgents,agents_per_community, replace=False)
            indicesSelected = [int(index) for index in indicesSelected]
            otherIndices = [index for index in range(self.numAgents) if index not in indicesSelected]
            self.additionalInfo = (indicesSelected, otherIndices)
            
            ##Community 1 Discussion
            eligible_agents = [self.agents[i] for i in indicesSelected]
            discussion_Prompt = "\n" + self.instructions["DiscussInstruction"][self.condition] +"\n"
            for agent in eligible_agents:
                agent.update_Context(discussion_Prompt)
            for round in range(rounds):
                print("Round " + str(round+1))
                prompt = "It is your turn to speak"
                for i in range(len(eligible_agents)):
                    turn_at_talk_agent = eligible_agents[i]
                    other_agents = eligible_agents[:i]+eligible_agents[i+1:]

                    response = turn_at_talk_agent.get_response(prompt + ". You are " + turn_at_talk_agent.name)
                    formattedResponse = "\n" + turn_at_talk_agent.name + "'s response: " + response
                    for agent in other_agents:
                        agent.update_Context(formattedResponse)

            #Community 2 Discussion
            eligible_agents = [self.agents[i] for i in otherIndices]
            discussion_Prompt = "\n" + self.instructions["DiscussInstruction"][self.condition] +"\n"
        
            for agent in eligible_agents:
                agent.update_Context(discussion_Prompt)
            for round in range(rounds):
                print("Round " + str(round+1))
                prompt = "It is your turn to speak"
                for i in range(len(eligible_agents)):
                    turn_at_talk_agent = eligible_agents[i]
                    other_agents = eligible_agents[:i]+eligible_agents[i+1:]

                    response = turn_at_talk_agent.get_response(prompt + ". You are " + turn_at_talk_agent.name)
                    formattedResponse = "\n" + turn_at_talk_agent.name + "'s response: " + response
                    for agent in other_agents:
                        agent.update_Context(formattedResponse)

        elif self.condition == "Hierarchy":
            leader = None
            others = []
            self.additionalInfo = [[],[]]
            for i in range(len(self.agents)):
                currAgent = self.agents[i]
                if currAgent.condition == "Hierarchy_L":
                    leader = currAgent
                    self.additionalInfo[0].append(i)
                else:
                    others.append(currAgent)
                    self.additionalInfo[1].append(i)
                currAgent.update_Context("\n" + self.instructions["DiscussInstruction"][currAgent.condition] + "\n")
            for agent in others:
                for round in range(rounds):
                    print("Round " + str(round+1))
                    prompt = "It is your turn to speak"
                    response = agent.get_response(prompt + ". You are employee " + agent.name)
                    formattedResponse = "\n employee " + agent.name + "'s response: " + response
                    leader.update_Context(formattedResponse)

                    response = leader.get_response(prompt + ". You are boss " + leader.name)
                    formattedResponse = "\n boss " + leader.name + "'s response: " + response
                    agent.update_Context(formattedResponse)

        elif self.condition == "Baseline":
            return


            

            

                

            
            





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
                response = votingAgent.get_response(prompt + " You are " + votingAgent.name)
                formattedResponse = votingAgent.name + "'s response: " + response
                statementRatings = get_integer_ratings(self.statements, response)
                vote = list(statementRatings.values())
                allVotes.append(vote)
                #self.finalVote["Person " + str(i)] = statementRatings

                for agent in other_agents:
                    agent.update_Context(formattedResponse)
                i += 1
            averageVotes = get_average_vote(allVotes)
            self.finalVote = averageVotes
        elif self.condition == "Community":
            prompt = """You will now privately vote for a representative for your community. This representative will vote with the representative from the other community to decide the ratings for each statement. You can not vote for yourself. Type ONLY the name of the person you want to vote for, and include nothing else in your response."""
            representatives = []
            for indexList in self.additionalInfo:
                i = 0
                eligible_agents = [self.agents[j] for j in indexList]
                votes = {agent.name: 0 for agent in eligible_agents}
                for agent in eligible_agents:
                    successfulVote = False
                    vote = agent.get_response(prompt + " You are " + agent.name + "\n")
                    votedName = get_Voted_Person(vote)[0]
                    while successfulVote == False:
                        if votedName in votes:
                            votes[votedName] = votes[votedName] + 1
                            successfulVote = True
                            print(agent.name + " voted for: " + votedName)
                        else:
                            vote = agent.get_response("\n You have not voted for an eligible person. Please vote again, responding with ONLY the name of the person you are voting for.")
                            votedName = get_Voted_Person(vote)[0]
                            print("invalid vote")
                VotedAgent = max(votes.items(), key=operator.itemgetter(1))[0]
                print("Final Vote: " + VotedAgent)
                representatives.append(VotedAgent)
            allVotes = []
            for representative in representatives:
                selectedAgent = [agent for agent in self.agents if agent.name == representative][0]
                print(selectedAgent.name)
                prompt = "\n You have been selected as the representative for your community. It is now your turn to vote for the likelihood of each of the 4 statements discussed. Respond ONLY with integers between 0 and 10 to rate the likelihood of each statement, and separate each integer with a space."
                response = selectedAgent.get_response(prompt + " You are " + selectedAgent.name)
                #formattedResponse = selectedAgent.name + "'s response: " + response
                statementRatings = get_integer_ratings(self.statements, response)
                vote = list(statementRatings.values())
                allVotes.append(vote)
            averageVotes = get_average_vote(allVotes)
            self.finalVote = averageVotes
        elif self.condition == "Hierarchy":
            index = self.additionalInfo[0][0]
            leader = self.agents[index]
            prompt = "As the boss, you will now decide the final ratings for each statement for your team. Respond ONLY with integers between 0 and 10 to rate the likelihood of each statement, and separate each integer with a space.\n"
            response = leader.get_response(prompt)
            statementRatings = get_integer_ratings(self.statements, response)
            vote = list(statementRatings.values())
            self.finalVote = vote
        elif self.condition == "Baseline":
            prompt = "You will now officially lock in your ratings for each statement. Response ONLY with integers between 0 and 10 to rate the likelihood of each statement, and separate each integer with a space. \n"
            allVotes = []
            for agent in self.agents:
                response = agent.get_response(prompt)
                statementRatings = get_integer_ratings(self.statements, response)
                vote = list(statementRatings.values())
                allVotes.append(vote)
            averageVotes = get_average_vote(allVotes)
            self.finalVote = averageVotes
                    #for agenta in eligible_agents:
                    #    print(agenta.name)
                    #print(votedName, agent.name)
                    

            #prompt = """You will now vote for the final ratings of each statement within your community. The decision will be the average of all your votes. Please vote for the likelihood of each statement now."""
            #for agent in self.agents:
            #    agent.update_Context(prompt)
            #allVotes = [[],[]]
            #z = 0
            #for indexList in self.additionalInfo:
            #    i = 0
            #    eligible_agents = [self.agents[j] for j in indexList]
            #    for agent in eligible_agents:
            #        votingAgent = eligible_agents[i]
            #        other_agents = eligible_agents[:i]+eligible_agents[i+1:]
            #        prompt = "\n It is now your turn to vote. Respond ONLY with integers between 0 and 10 to rate the likelihood of each statement, and separate each integer with a space.\n"
            #        response = votingAgent.get_response(prompt + " You are Person " + str(i))
            #        formattedResponse = "Person " + str(i) + "'s response: " + response
            #        statementRatings = get_integer_ratings(self.statements, response)
            #        vote = list(statementRatings.values())
            #        allVotes[z].append(vote)
                    #self.finalVote["Person " + str(i)] = statementRatings

            #        for agent in other_agents:
            #            agent.update_Context(formattedResponse)
            #        i += 1
            #    z += 1

            #averageVote_community1, averageVote_community2 = get_average_vote(allVotes[0]), get_average_vote(allVotes[1])
            #self.finalVote = [averageVote_community1, averageVote_community2]
            
    









    def run_1_trial(self, verbose = False, run = 0):
         ###Flow: Init instruction + observations --> statement instruction + statements --> init rating
    ###  --> discuss instruction --> final rating --> vote
        for agent in self.agents:
            self.generate_Instruction_Prompt(agent)

        self.discussion()
        self.get_final_ratings()
        self.get_final_vote_by_condition()
        #print(self.finalVote)
        data = self.format_Data_for_Export()
        if verbose == True:
            now = get_date_now()
            fileName = now + "_run=" + str(run) + "_" + str(self.condition) + ".txt"
            with open(fileName, 'w') as text_file:
                text_file.write(str([agent.context['Context'] for agent in self.agents]))
        return data
    
    def run_n_trials(self, n, testTrial = False, verbose = False):
        fileName = ""
        if testTrial:
            fileName += "TESTRUN_"
        now = get_date_now()
        fileName += now + "_" + str(self.condition) + ".csv"
        
        records = []
        for i in range(n):
            newData = self.run_1_trial(verbose = verbose, run = i)
            records.append(newData)
            self.reinit()

           
        columnNames = [
            'condition',
            'agentType',
            'observations',
            'initEvals',
            'finalEvals',
            'groupDecision',
            'additionalInfo',
            #'agentContext',
        ]
        df = pd.DataFrame.from_records(records, columns = columnNames)
        df.to_csv(fileName, encoding='utf-8', index=False)
        #suppDf.to_csv("Supplementary_" + fileName, encoding='utf-8', index=False)
        return
        



condition = "Baseline"


trial = trialExecution(condition, "GEMINI", numAgents=3)
trial.run_n_trials(2, testTrial = True, verbose=True)
##May update community to be voting for a representative, then those two vote and are averaged?

##Settle on observations and statements

##Update: Replace Person 'i' with explicit names for community voting

#Verbose tag for outputting agent.context data