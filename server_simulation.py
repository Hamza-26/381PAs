class ServerAgent:
    def __init__(self,small_count=10,medium_count=10,large_count=10):
        self.small_count = small_count
        self.medium_count = medium_count
        self.large_count = large_count
    def select_action(self,percept):
        if (percept >=0 and percept <= 33):
            if(self.large_count != 0):
                self.large_count-=1
                return "large"
        elif(percept >=34 and percept <= 66):
            if(self.medium_count != 0):
                self.medium_count-=1
                return "medium"
        elif(percept >=67 and percept <=99):
            if(self.small_count != 0):
                self.small_count-=1
                return "small"
    def storage_empty(self):
        return (self.small_count ==0 and self.medium_count==0 and self.large_count ==0)


class ServerEnvironment:
    def __init__(self,server_agent):
        self.server_agent = server_agent
        self.num_agent_actions=0
    
    def tick(self):
        import random
        hydration_level = random.randint(0,130)
        self.server_agent.select_action(hydration_level)
        self.num_agent_actions+=1
        
    def simulate(self):
        while(not self.server_agent.storage_empty()):
            self.tick()