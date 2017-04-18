# TODO

###### BUGS
* Don't skip custom validators on empty fields (#334)
* Defer remote validation while request is still pending. (#72)

###### ENHANCEMENTS:
* Refactor validators to optionally return promises. (#131) (#177) (#275)
* use Element.setCustomValidity() for non-native validators (#450)
* DOCS: Give custom validators own example section (#380)
* Improve invalid/valid error events, add post-delay events.
  - include events for whole form validate/validated, change current validate/validated/invalid/valid to fieldvalidate etc.
  - [error/errored] [success/successed] in addition to [valid/invalid], upon displaying or clearing an error
  - add whether or not field is valid in [validated.bs.validator] event.detail
  - add events on `.validator('validate')`, including whole form validity in `event.detail`
  * ^ Add a way to reliably determine if form is valid or invalid upon submit. (#67)
* Add a class to the form to indicate validity state. (#260)


###### BREAKING CHANGES:
* Change remote validator to use response body as error message.


# DONE

