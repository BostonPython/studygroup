
class ModelNotFoundException(Exception):
    pass

class FormValidationException(Exception):
    pass

class UnAuthorizedException(FormValidationException):
    def __init__(self, member_id):
        message = "UnAuthorized action for member with Id: %s " % (member_id)
        super(UnAuthorizedException, self).__init__(message)

class MembershipException(FormValidationException):
    def __init__(self, member_id, group_id):
        message = "Member {%s} is already part of group: {%s} " % (member_id, group_id)
        super(MembershipException, self).__init__(message)

class GroupFullException(FormValidationException):
    def __init__(self, group):
        message = "Group: %s Id: %s" % (group.name, group.id)
        super(GroupFullException, self).__init__(message)
