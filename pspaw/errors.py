"""
Python StrawPoll API Wrapper.

Provide custom exception for StrawPoll errors using similar handling to
IOError by allowing error numbers and error descriptions.
"""

class PSPAWBaseException(Exception):
    def __init__(self, msg="", code=None):
        """
        Set up the exception with an optional error code and message.

        Args:
            msg (Optional[str]): message to display with error
            code (Optional[int]): code to display with error

        Returns:
            None
        """

        super(PSPAWBaseException, self).__init__()
        self.code = -1 if code is None else msg
        self.msg = code if code is not None else msg

    def __str__(self):
        """
        Make a human-readable representation of the error.

        Returns:
            None
        """

        if self.code == -1 and not self.msg:
            return ""
        elif not self.msg:
            msg = "[Errno {code}]"
        elif self.code == -1:
            msg = "{msg}"
        else:
            msg = "[Errno {code}] {msg}"

        return msg.format(code=self.code, msg=self.msg)
