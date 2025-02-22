import os
from dotenv import load_dotenv, dotenv_values
from google import genai



load_dotenv()



class gem_Agent():
    #basicInstruction = """You are an agent working with 5 other agents. You have each spent some time observing the behavior of John, 
    #a person of interest. You will be given multiple statements about John, and you must evaluate their likelihood based on 
    #your observations and your discussions with other agents in the group. Each agent has made distinct observations.
    #Your observations are listed below: """

   
    def __init__(self):
        self.key = os.getenv("GEMINI_KEY")
        self.client = genai.Client(api_key = self.key)
        self.model = "gemini-2.0-flash"
        self.condition = None
        self.context = {
                        "Observations": [],
                        #"Statements": self.statements,
                        "Initial Evaluations": {},
                        "Context": "",
                        "Final Evaluations": {},
                        }
        
    def set_Condition(self, condition):
        self.condition = condition

    def set_Observations(self, observations):
        self.context["Observations"] = observations

    def set_InitialEvaluations(self, statements, evaluations):
        self.context["Initial Evaluations"] = {statements[x]:evaluations[x] for x in range(len(statements))}

    def set_FinalEvaluations(self, statements, evaluations):
        self.context["Final Evaluations"] = {statements[x]:evaluations[x] for x in range(len(statements))}

    def update_Context(self, newContext):
        self.context["Context"] = self.context["Context"] + "\n" + newContext
        
    def get_response(self, intText):
        self.update_Context(intText)
        #self.context["Context"] = self.context["Context"] + "\n" + intText
        response = self.client.models.generate_content(
            model = self.model,
            contents = self.context["Context"]
        )
        formatted_For_Context = "\n" + "Your Response: " + response.text + "\n"
        self.update_Context(formatted_For_Context)
        print("Context: ", self.context["Context"])
        return response.text

    #def store_context(self):

#agent1 = Gemini_Agent("Hierarchy","abcdefg", "aaa")
#rep = agent1.get_response("Which animal is the best in terms of visual appeal? Be brief. The last word of your response MUST be your animal choice in all capitals.")
#print(rep.text)