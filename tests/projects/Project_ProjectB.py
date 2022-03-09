from dominion import Project


###############################################################################
class Project_ProjectB(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = "TEST"
        self.desc = "ProjectB"
        self.name = "ProjectB"


# EOF
