"""
Python StrawPoll API Wrapper.

Provide an object for easily accessible polls and functions to
fetch existing polls or create new ones.
"""

from __future__ import division

from pspaw import request

class Poll(object):
    def __init__(self, id=-1, title="", options=None, votes=None, multi=False, dupcheck=None, permissive=False, captcha=False, **kwargs):
        """
        Set up a new poll's instance variables and handle
        deprecation/new features (permissive vs dupcheck).

        Args:
            id (Optional[int]): ID of the poll. Defaults to -1.
            title (Optional[str]): Title of the poll. Defaults to "".
            options (Optional[list]): Strings to represent the options for the poll. Defaults to None.
            votes (Optional[list]): Integers that correspond to the same indexed option which specify the current votes for that option. Defaults to None.
            multi (Optional[bool]): Can the poll can accept multiple votes from one user? Defaults to False.
            dupcheck (Optional[str]): How to handle checking for duplicate votes {"normal", "permissive", "disabled"}. Defaults to None.
            permissive (Optional[bool]): DEPRECATED! use "dupcheck" instead | Attempt to be more lenient in vote duplication checking? Defaults to False.
            captcha (Optional[bool]): Does the poll require users to pass a captcha to vote? Defaults to False.

        Returns:
            None.
        """

        self.id = id
        self.title = title
        self.multi = multi
        self.permissive = permissive
        self.captcha = captcha

        if dupcheck is None:
            dupcheck = "permissive" if self.permissive else "disabled"
        self.dupcheck = dupcheck

        self._update_results(options, votes)

    def _update_results(self, options=None, votes=None):
        """
        Set the poll's results and total votes based on input.

        Args:
            options (Optional[list]): strings to represent the options for the poll
            votes (Optional[list]): integers that correspond to the same indexed option which specify the current votes for that option

        Returns:
            None.
        """

        self.results = {}
        self.total_votes = 0

        self.options = options if options is not None else []
        self.votes = votes if votes is not None else []

        if self.options and not self.votes:
            self.votes = [0] * len(self.options)

        for idx, option in enumerate(self.options):
            self.results[option] = self.results.get(option, 0) + self.votes[idx]
            self.total_votes += self.votes[idx]

    def normalise(self, rounding=2):
        """
        Get percentage values of the poll's results.

        Args:
            rounding (Optional[int]): Precision of percentage values. Defaults to 2.

        Returns:
            dict: A dictionary where keys are the poll's options and values are the percentage of people that voted for them.
                  When nobody has voted, each value will be 0.
        """

        results = {}
        for option, votes in self.results.items():
            if self.total_votes == 0:
                results[option] = 0
            else:
                results[option] = round((votes / self.total_votes) * 100, rounding)
        return results

    def refresh(self):
        """
        Fetch new data from the API and update the poll's results and total votes.

        Returns:
            None.
        """

        req = request.get("http://strawpoll.me/api/v2/polls/{}".format(self.id))
        options = req["options"] if "options" in req else []
        votes = req["votes"] if "votes" in req else []
        self._update_results(options, votes)


def create(title, options, multi=False, dupcheck="normal", captcha=False):
    """
    Create a new poll by querying the API with specified values.

    Args:
        title (str): Title of the poll.
        options (list): Strings to represent the options for the poll.
        multi (Optional[bool]): Can the poll can accept multiple votes from one user? Defaults to False.
        dupcheck (Optional[str]): How to handle checking for duplicate votes {"normal", "permissive", "disabled"}. Defaults to "normal".
        captcha (Optional[bool]): Does the poll require users to pass a captcha to vote? Defaults to False.

    Returns:
        Poll: A new Poll instance with the ID of the poll included.
    """

    return Poll(**request.post(
        "http://strawpoll.me/api/v2/polls",
        {
            "title": title,
            "options": options,
            "multi": multi,
            "dupcheck": dupcheck,
            "captcha": captcha
        }
    ))

def get(id):
    """
    Fetch an existing poll by querying the API with its ID.

    Args:
        id (int): ID of the poll.

    Returns:
        Poll: A new Poll instance with the poll's information.
    """

    return Poll(**request.get(
        "http://strawpoll.me/api/v2/polls/{}".format(id)
    ))
