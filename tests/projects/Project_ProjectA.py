from dominion import Project


###############################################################################
class Project_ProjectA(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = "TEST"
        self.desc = "ProjectA"
        self.cost = 3
        self.name = "ProjectA"


# EOF
