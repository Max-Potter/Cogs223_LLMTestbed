import os

conditionDictionary = {
        "InitInstruction": {
            "Baseline":"",
            "Council": """You are a councilmember working with 5 other people in a council. You have each spent some time observing the
            behavior of John, a person of interest. You will be given multiple statements about John, and you must evaluate their
            likelihood based on your observations and your discussions with other people in the council. Each person has made
            distinct observations. Your observations are listed below: """,
            "Community": """You are a community-member working with 2 other people in a small community. You have each spent some time
            observing the behavior of John, a person of interest. You will be given multiple statements about John,
            and you must evaluate their likelihood based on your observations and your discussions with other people in the
            community. Each person has made distinct observations. There is a neighboring community also made up of 3 people working 
            on the same task. Your observations are listed below: """,
            "Hierarchy_P": """You are an employee working alongside 4 other employees and your boss. You have each spent some time
            observing the behavior of John, a person of interest. You will be given multiple statements about John, and you must evaluate
            their likelihood based on your observations and your discussions with your boss. Each person has made distinct observations.
            Your observations are listed below: """,
            "Hierarchy_L": """You are a boss working alongside 5 other employees that report to you. You have each spent some time
            observing the behavior of John, a person of interest. You will be given multiple statements about John, and you must evaluate
            their likelihood based on your observations and your discussions with each employee individually. Each person has made distinct observations.
            Your observations are listed below: """,
        },
        "DiscussInstruction":{
            "Baseline": "",
            "Council": """You will now have time to discuss your opinions on the statements as a group of 6. At the end of discussion,
            all 6 councilmembers will vote to decide the likelihood of each statement.""",
            "Community": """You will now have time to discuss your opinions on the statements with 2 of the other agents. At the end of discussion,
            all 6 community members will vote to decide the likelihood of each statement.""",
            "Hierarchy_P": """You will now have time to discuss your opinions with the leader. The leader will get to talk with each other agent.
            At the end of discussion, the leader will decide the likelihood of each statement""",
            "Hierarchy_L":"""You will now have time to discuss your opinions with each employee individually. At the end of discussion,
            you alone will decide the likelihood of each statement""",
        },
    }