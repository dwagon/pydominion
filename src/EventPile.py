import imp


###############################################################################
class EventPile(object):
    def __init__(self, eventname, eventpath='events'):
        self.eventname = eventname
        self.eventpath = eventpath
        self.event = self.loadClass(eventname)()

    ###########################################################################
    def loadClass(self, eventname, eventfile=None):
        eventmodule = self.importEvent(eventname=eventname, eventfile=eventfile)
        self.eventclass = getattr(eventmodule, "Event_%s" % eventname)
        return self.eventclass

    ###########################################################################
    def importEvent(self, eventname=None, eventfile=None):
        if eventfile:
            fp, pathname, desc = imp.find_module(eventfile, [self.eventpath, 'events'])
        else:
            fp, pathname, desc = imp.find_module("Event_%s" % eventname, [self.eventpath, 'events'])
        eventmodule = imp.load_module(eventname, fp, pathname, desc)
        return eventmodule

    ###########################################################################
    def __getattr__(self, name):
        return getattr(self.event, name)

    ###########################################################################
    def __repr__(self):
        return "Event %s" % self.name

# EOF
