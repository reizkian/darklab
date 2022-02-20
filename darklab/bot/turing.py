from darklab.bot.george import botGeorge

class botTuring:
    def __init__(self, inp):
        self.george = botGeorge(inp)
    
    def pinp(self):
        self.george.print_input()
