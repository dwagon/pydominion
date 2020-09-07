from Project import Project


###############################################################################
class Project_ProjectA(Project):
    def __init__(self):
        Project.__init__(self)
        self.base = "TEST"
        self.desc = "ProjectA"
        self.cost = 3
        self.name = "ProjectA"

# EOF
