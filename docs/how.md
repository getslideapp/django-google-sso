# How Django Google SSO works?

## Current Flow

1. First, the user is redirected to the Django login page. If settings `GOOGLE_SSO_ENABLED` is True, the
"Login with Google" button will be added to default form.

2. On click, **Django-Google-SSO** will add, in a anonymous request session, the `next_path` and Google Flow `state`.
This data will expire in 10 minutes. Then user will be redirected to Google login page.

    !!! info "Using Request Anonymous session"
        If you make any actions which changes or destroy this session, like restart django, clear cookies or change
        browsers, the login will fail and you can see the message "State Mismatched. Time expired?" in the next time
        you log in again.

3. On callback, **Django-Google-SSO** will check `code` and `state` received. If they are valid,
Google's UserInfo will be retrieved. If the user is already registered in Django, the user
will be logged in.

4. Otherwise, the user will be created and logged in, if his email domain,
matches one of the `GOOGLE_SSO_ALLOWABLE_DOMAINS`. You can disable the auto-creation setting `GOOGLE_SSO_AUTO_CREATE_USER`
to False.

5. On creation only, this user can be set to the`staff` or `superuser` status, if his email are in `GOGGLE_SSO_STAFF_LIST` or
`GOGGLE_SSO_SUPERUSER_LIST` respectively. Please note if you add an email to one of these lists, the email domain
must be added to `GOOGLE_SSO_ALLOWABLE_DOMAINS`too.

6. This authenticated session will expire in 1 hour, or the time defined, in seconds, in `GOOGLE_SSO_SESSION_COOKIE_AGE`.

7. Browser will be redirected to `next_path` if operation succeeds, or the `login` page, if operation fails.


## Using Custom Authentication Backend

If the users need to log in using a custom authentication backend, you can use the `GOOGLE_SSO_AUTHENTICATION_BACKEND`
setting:

```python
# settings.py

GOOGLE_SSO_AUTHENTICATION_BACKEND = "myapp.authentication.MyCustomAuthenticationBackend"
```
