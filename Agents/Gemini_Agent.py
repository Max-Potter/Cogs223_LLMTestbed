import os
from dotenv import load_dotenv, dotenv_values
from google import genai



load_dotenv()



class gem_Agent():
    #basicInstruction = """You are an agent working with 5 other agents. You have each spent some time observing the behavior of John, 
    #a person of interest. You will be given multiple statements about John, and you must evaluate their likelihood based on 
    #your observations and your discussions with other agents in the group. Each agent has made distinct observations.
    #Your observations are listed below: """

    ###Flow: Init instruction --> observations --> statement instruction --> statements --> init rating
    ###  --> discuss instruction --> final rating --> vote
    def __init__(self, observations):
        self.key = os.getenv("GEMINI_KEY")
        self.client = genai.Client(api_key = self.key)
        self.model = "gemini-2.0-flash"
        self.context = {
                        "Observations": observations,
                        #"Statements": self.statements,
                        "Initial Evaluations": {},
                        "Context": "",
                        "Final Evaluations": {},
                        }
        
    def get_response(self, text):
        response = self.client.models.generate_content(
            model = self.model,
            contents = text
        )
        return response

    #def store_context(self):

#agent1 = Gemini_Agent("Hierarchy","abcdefg", "aaa")
#rep = agent1.get_response("Which animal is the best in terms of visual appeal? Be brief. The last word of your response MUST be your animal choice in all capitals.")
#print(rep.text)