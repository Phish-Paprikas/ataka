import enum


class FlagStatus(str, enum.Enum):
    UNKNOWN = 'unknown'

    # Flag yielded points
    OK = 'ok'

    # Flag is in queue for submission
    QUEUED = 'queued'

    # Flag is currently being submitted
    PENDING = 'pending'

    # We already submitted this flag and the submission system tells us that
    DUPLICATE = 'duplicate'

    # We didn't submit this flag because it was a duplicate
    DUPLICATE_NOT_SUBMITTED = "duplicate_not_submitted"

    # something is wrong with our submitter or the flag service
    ERROR = 'error'

    # the flag belongs to the NOP team
    NOP = 'NOP'

    # we tried to submit our own flag and the submission system lets us know
    OWNFLAG = 'ownflag'

    # the flag is not longer active. This is used if a flags expire
    INACTIVE = 'inactive'

    # flag fits the format and could be sent to the submission system, but the
    # submission system told us it is invalid
    INVALID = 'invalid'

    CONTEST_OVER = 'Game is not running / Contest is over'
    SUBMISSION_NOT_APPROVED = 'Submission not approved'
    MEMBERSHIP_NOT_APPROVED = 'Membership not approved'
    BREAK_TIME = 'Break time'
    INVALID_FORMAT = 'Invalid flag format'
    FLAG_NOT_FOUND = 'Flag not found for this contest.'
    OWN_FLAG = 'You cannot submit your own flag.'
    FLAG_FROM_FUTURE = 'Flag is from the future.'
    FLAG_TOO_OLD = 'Flag is too old'
    FLAG_ALREADY_SUBMITTED = 'Flag already submitted.'
    NOP_TEAM = 'You are not allowed to submit flags from NOP teams'
    GENERIC_ERROR = 'Generic error'

DuplicatesDontResubmitFlagStatus = {
    FlagStatus.OK,
    FlagStatus.QUEUED,
    FlagStatus.PENDING,
    FlagStatus.DUPLICATE,
    FlagStatus.NOP, 
    FlagStatus.OWNFLAG,
    FlagStatus.INACTIVE,
    FlagStatus.INVALID,
    
    FlagStatus.INVALID_FORMAT,
    FlagStatus.FLAG_NOT_FOUND,
    FlagStatus.OWN_FLAG,
    FlagStatus.FLAG_TOO_OLD,
    FlagStatus.FLAG_ALREADY_SUBMITTED,
    FlagStatus.NOP_TEAM,
}