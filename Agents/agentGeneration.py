import os
import random
import numpy as np

from Agents.Gemini_Agent import gem_Agent
#from Deepseek_Agent import deep_Agent

def generate_n_agents(n, model_type, observations, condition, observationsPerAgent = 2, possible_names = ["Gary", "Steven", "Anne", "Jenny", "Charles", "Lucille"]):
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
    
    namesList = np.random.choice(n, n, replace=False)
    i=0
    for agent in agents:
        sampledObservations = random.sample(observations, observationsPerAgent)
        agent.set_Observations(sampledObservations)
        agent.set_Condition(condition)
        agent.set_Name(possible_names[namesList[i]])
        i+=1
        

    if condition == "Hierarchy":
        leader = np.random.randint(0, len(agents))
        for x in range(len(agents)):
            if x == leader:
                agents[x].set_Condition("Hierarchy_L")
            else:
                agents[x].set_Condition("Hierarchy_P")
    return agents




            
