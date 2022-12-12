# All Django Settings options

| Setting                                  | Description                                                                                                                                              |
|------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `GOOGLE_SSO_ALLOWABLE_DOMAINS`           | List of domains that will be allowed to create users. Default: `[]`                                                                                      |
| `GOOGLE_SSO_AUTHENTICATION_BACKEND`      | The authentication backend to use.  Default: `None`                                                                                                      |
| `GOOGLE_SSO_AUTO_CREATE_FIRST_SUPERUSER` | If True, the first user that logs in will be created as superuser if no superuser exists in the database at all. Default: `False`                        |
| `GOOGLE_SSO_AUTO_CREATE_USERS`           | Enable or disable the auto-create users feature. Default: `True`                                                                                         |
| `GOOGLE_SSO_CALLBACK_DOMAIN`             | The netloc to be used on Callback URI. Default: `None`                                                                                                   |
| `GOOGLE_SSO_CLIENT_ID`                   | The Google OAuth 2.0 Web Application Client ID. Default: `None`                                                                                          |
| `GOOGLE_SSO_CLIENT_SECRET`               | The Google OAuth 2.0 Web Application Client Secret. Default: `None`                                                                                      |
| `GOOGLE_SSO_ENABLED`                     | Enable or disable the plugin. Default: `True`                                                                                                            |
| `GOOGLE_SSO_PROJECT_ID`                  | The Google OAuth 2.0 Project ID. Default: `None`                                                                                                         |
| `GOOGLE_SSO_SCOPES`                      | The Google OAuth 2.0 Scopes. Default: `["openid", "https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]` |
| `GOOGLE_SSO_SESSION_COOKIE_AGE`          | The age of the session cookie in seconds. Default: `3600`                                                                                                |
| `GOOGLE_SSO_STAFF_LIST`                  | List of emails that will be created as staff. Default: `[]`                                                                                              |
| `GOOGLE_SSO_SUPERUSER_LIST`              | List of emails that will be created as superuser. Default: `[]`                                                                                          |
| `GOOGLE_SSO_TIMEOUT`                     | The timeout in seconds for the Google SSO authentication returns info, in minutes. Default: `10`                                                         |
