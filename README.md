# PSPAW: The Python StrawPoll API Wrapper.

PSPAW, an acronym for "Python StrawPoll API Wrapper", is a Python package that allows for simple access to StrawPoll's API. PSPAW aims to be as easy to use as possible and is developed based on official documentation [found here](https://github.com/strawpoll/strawpoll/wiki/API). PSPAW does it's best to deal with deprecation, specifically relating to changes between the earlier polls and the newer ones.

## Documentation

### Importing

PSPAW can be imported in a number of ways due to how the package is structued.

* `import pspaw` will allow PSPAW's main features to be accessed via `pspaw.poll`
* `from pspaw import poll` will allow PSPAW's main features to be accessed via `poll`

For the sake of the usage guide we will be using `import pspaw`.

### User-Agent

In order to change the User-Agent that all requests are performed with, you must set the `pspaw.poll.request.USERAGENT` variable to whatever you wish the User-Agent to be.

```
pspaw.poll.request.USERAGENT = "my app v1.0.0"
```

### Error Handling

PSPAW's `request` module handles all GET and POST requests performed to the API, and more specifically detects when an error is returned by the API. All errors the `request` module detects will be raised as `pspaw.errors.PSPAWBaseException` exceptions. The `pspaw.errors.PSPAWBaseException` exception has two main important properties: `code` and `msg`. `code` is the error-code returned by the API (if there is one), and `msg` is the error string returned by the API.

```
>>> import pspaw
>>> try:
...    p = pspaw.poll.get(-1)
... except pspaw.errors.PSPAWBaseException as e:
...     print("Error #{}: {}".format(e.code, e.msg))
Error #41: Poll not found
```

### Usage

### The `Poll` Object

Both getting and creating a poll will return a `Poll` object. The `Poll` object has the following properties:

* int `id`: ID of the poll.
* str `title`: Title of the poll.
* list `options`: Strings to represent the options for the poll.
* list `votes`: Integers that correspond to the same indexed option which specify the current votes for that option.
* dict `results`: A hashtable where the key is the poll's option and the value is the amount of votes for that option.
* bool `multi`: Can the poll can accept multiple votes from one user?
* bool `permissive`: Attempt to be more lenient in vote duplication checking? (**DEPRECATED**, used for detecting `dupcheck` in earlier polls)
* bool `captcha`: Does the poll require users to pass a CAPTCHA to vote?
* str `dupcheck`: How to handle checking for duplicate votes {"normal", "permissive", "disabled"}

You can get percentage values of each vote using `p.normalise()`, with an optional `rounding` paramater which defaults to 2 decimal places.

You can fetch fresh voting values for the poll by using `p.refresh()`.

#### Getting a Poll

```
>>> import pspaw
>>> p = pspaw.poll.get(1)
>>> p.id
1
>>> p.title
u'What movie should we watch'
>>> p.total_votes
64644
>>> p.results
{u'Witchhunter': 7928, u'Prison logic': 7008, u'Sucker punch ': 16425, u'Pirates of carribian ': 33283}
>>> p.normalise()
{u'Witchhunter': 12.26, u'Prison logic': 10.84, u'Sucker punch ': 25.41, u'Pirates of carribian ': 51.49}
```

#### Creating a Poll

```
>>> import pspaw
>>> p = pspaw.poll.create(title="Is PSPAW a cool project?", options=["Yes", "No"], multi=False, dupcheck="permissive", captcha=True)
>>> p.id
5941011
```
