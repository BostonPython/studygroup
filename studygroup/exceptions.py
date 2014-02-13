

class ModelNotFoundException(Exception):
    pass

class GroupFullException(Exception):

    def __init__(self, group):
        message = "Group: %s Id: %s" % (group.name, group.id)
        super(GroupFullException, self).__init__(message)