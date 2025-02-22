import os
import random
import numpy as np

from Agents.Gemini_Agent import gem_Agent
#from Deepseek_Agent import deep_Agent

def generate_n_agents(n, model_type, observations, condition, observationsPerAgent = 2):
    agents = []
    if model_type == "GEMINI":
        for i in range(n):
            agents.append(gem_Agent())
    elif model_type == "DEEPSEEK":
        for i in range(n):
            print("NYI -- not yet implemented")
            return
    else:
        print("Invalid")
        return
    
    for agent in agents:
        sampledObservations = random.sample(observations, observationsPerAgent)
        agent.set_Observations(sampledObservations)
        agent.set_Condition(condition)

    if condition == "Hierarchy":
        leader = np.random.randint(0, len(agents))
        for x in range(len(agents)):
            if x == leader:
                agents[x].set_Condition("Hierarchy_L")
            else:
                agents[x].set_Condition("Hierarchy_P")
    return agents




            
