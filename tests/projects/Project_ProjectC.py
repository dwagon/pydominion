from dominion import Project


###############################################################################
class Project_ProjectC(Project.Project):
    def __init__(self):
        Project.Project.__init__(self)
        self.base = "TEST"
        self.desc = "ProjectC"
        self.name = "ProjectC"


# EOF
