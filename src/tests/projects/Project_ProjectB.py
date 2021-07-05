from Project import Project


###############################################################################
class Project_ProjectB(Project):
    def __init__(self):
        Project.__init__(self)
        self.base = "TEST"
        self.desc = "ProjectB"
        self.name = "ProjectB"


# EOF
