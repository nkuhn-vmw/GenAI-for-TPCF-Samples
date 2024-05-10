# UAA audit requirements
This topic describes audit requirements for the User Account and Authentication Service (UAA).
UAA does the following:

* Handles authentication for users and client apps

* Manages user accounts

* Manages client app registrations
Each audit event contains the following:

* Client Address - the client IP or if not attainable, the IP of the last proxy

* Date/Time of the event

* Principal - if authenticated

* Client ID - if available

* Data identifying the event

## Authentication and password events
UAA includes the following authentication and password events:

* `UserAuthenticationSuccess`

+ **Trigger:** When a user is successfully authenticated

+ **Data Recorded:** User ID and Username

* `UserAuthenticationFailure`

+ **Trigger:** When a user authentication fails, user exists

+ **Data Recorded:** Username

+ **Notes:** Followed by a `PrincipalAuthenticationFailure`

* `UserNotFound`

+ **Trigger:** When a user authentication fails, user does not exists

+ **Data Recorded:** Username

+ **Notes:** Followed by a `PrincipalAuthenticationFailure`

* `UnverifiedUserAuthentication`

+ **Trigger:** When a user that is not yet verified authenticates

+ **Data Recorded:** User ID, Username

* `PasswordChangeSuccess`

+ **Trigger:** When a user password is changed through `/Users/{user_id}/password`

+ **Data Recorded:** User ID

* `PasswordChangeFailure`

+ **Trigger:** When a user password change is attempted through `/Users/{user_id}/password`

+ **Data Recorded:** User ID

* `ClientAuthenticationSuccess`

+ **Trigger:** When a client is successfully authenticated

+ **Data Recorded:** Client ID

* `ClientAuthenticationFailure`

+ **Trigger:** When a client authentication fails (client may or may not exist)

+ **Data Recorded:** Client ID

* `PrincipalAuthenticationFailure`

+ **Trigger:** When a client or user authentication fails

+ **Data Recorded:** Client ID or Username

* `PrincipalNotFound`

+ **Trigger:** currently not used

+ **Data Recorded:**

* `PasswordResetRequest`

+ **Trigger:** When a user requests to reset their password

+ **Data Recorded:** Email used

* `IdentityProviderAuthenticationSuccess`

+ **Trigger:** When a user successfully authenticates

+ **Data Recorded:** User ID and Username

* `IdentityProviderAuthenticationFailure`

+ **Trigger:** When a user authentication fails, and user exists

+ **Data Recorded:** User ID

+ **Notes:** Followed by a `UserAuthenticationFailureEvent` and `PrincipalAuthenticationFailure`

## Scim administration events
UAA includes the following Scim administration events:

* `UserCreatedEvent`

+ **Trigger:** When a user is created

+ **Data Recorded:** User ID (user\_id), Username (username), User Origin (user\_origin)

+ **Notes:** When the user is created by a client, also records the client ID (created\_by\_client\_id).
When the user is created by another user, also records the User ID (created\_by\_user\_id) and Username (created\_by\_username) of the user who performed the creation.

* `UserModifiedEvent`

+ **Trigger:** When a user is modified

+ **Data Recorded:** User ID, Username

* `UserDeletedEvent`

+ **Trigger:** When a user is deleted

+ **Data Recorded:** User ID (user\_id), Username (username), User Origin (`user_origin`)

+ **Notes:** When the user is deleted by a client, also records the client ID (`deleted_by_client_id`).
When the user is deleted by another user, also records the User ID (`deleted_by_user_id`) and Username (deleted\_by\_username) of the user who performed the deletion.

* `UserVerifiedEvent`

+ **Trigger:** When a user is verified

+ **Data Recorded:** User ID, Username

* `EmailChangedEvent`

+ **Trigger:** When a user email is changed

+ **Data Recorded:** User ID, Username, updated Email

* `ApprovalModifiedEvent`

+ **Trigger:** When approvals are added, modified or deleted for a user

+ **Data Recorded:** Username, Scope and Approval Status

* `GroupCreatedEvent`

+ **Trigger:** When a group is created

+ **Data Recorded:** Group ID, Group Name, Members

* `GroupModifiedEvent`

+ **Trigger:** When a group is updated (members added/removed)

+ **Data Recorded:** Group ID, Group Name, Members

* `GroupDeletedEvent`

+ **Trigger:** When a group is deleted

+ **Data Recorded:** Group ID, Group Name, Members

## Token events
UAA includes the following token event:

* `TokenIssuedEvent`

+ **Trigger:** When a token is created

+ **Data Recorded:** Principal ID (client or user ID), scopes

## Client administration events
UAA includes the following client administration events:

* `ClientCreateSuccess`

+ **Trigger:** When a client is created

+ **Data Recorded:** Client ID, Scopes, Authorities

* `ClientUpdateSuccess`

+ **Trigger:** When a client is updated

+ **Data Recorded:** Client ID, Scopes, Authorities

* `SecretChangeFailure`

+ **Trigger:** When a client secret fails to change

+ **Data Recorded:** Client ID

* `SecretChangeSuccess`

+ **Trigger:** When a client secret is changed

+ **Data Recorded:** Client ID

* `ClientApprovalsDeleted`

+ **Trigger:** When all approvals for a client are deleted

+ **Data Recorded:** Client ID

* `ClientDeleteSuccess`

+ **Trigger:** When a client is deleted

+ **Data Recorded:** Client ID

## UAA administration events
UAA includes the following UAA administration events:

* `ServiceProviderCreatedEvent`

+ **Trigger:** When managing the details of an external service provider which uses the UAA as a SAML IDP

+ **Data Recorded:** Principal ID (client or user ID), Service Provider

* `ServiceProviderModifiedEvent`

+ **Trigger:** When managing the details of an external service provider which uses the UAA as a SAML IDP

+ **Data Recorded:** Principal ID (client or user ID), Service Provider

* `IdentityZoneCreatedEvent`

+ **Trigger:** When identity zone is created in the UAA

+ **Data Recorded:** Principal ID (client or user ID), Identity Zone

* `IdentityZoneModifiedEvent`

+ **Trigger:** When managing the configuration of identity zones in the UAA

+ **Data Recorded:** Principal ID (client or user ID), Identity Zone

* `IdentityProviderCreatedEvent`

+ **Trigger:** When configuring the UAA to authenticate with an external IDP such as SAML or LDAP

+ **Data Recorded:** Principal ID (client or user ID), Identity Provider

* `IdentityProviderModifiedEvent`

+ **Trigger:** When configuring the UAA to authenticate with an external IDP such as SAML or LDAP

+ **Data Recorded:** Principal ID (client or user ID), Identity Provider

* `EntityDeletedEvent`

+ **Trigger:** When an identity provider or identity zone is deleted

+ **Data Recorded:** Principal ID (client or user ID), Deleted entity

## Flows
Below are some example flows for a UAA configured with LDAP as an IDP:

* Browser flows

+ **Successful login:** UserNotFound -> `PrincipalAuthenticationFailure` -> `UserCreatedEvent` -> `IdentityProviderAuthenticationSuccess` -> `UserAuthenticationSuccess`

+ **Invalid password:** `UserNotFound` -> `PrincipalAuthenticationFailure` -> `IdentityProviderAuthenticationFailure`

+ **Unknown user:** `UserNotFound` -> `PrincipalAuthenticationFailure` -> `IdentityProviderAuthenticationFailure`

* Password grant

+ **Successful login:** `ClientAuthenticationSuccess` -> `UserNotFound` -> `PrincipalAuthenticationFailure` -> `IdentityProviderAuthenticationSuccess` -> `UserAuthenticationSuccess` -> `TokenIssuedEvent`

+ **Invalid password:** `ClientAuthenticationSuccess` -> `UserNotFound` -> `PrincipalAuthenticationFailure` -> `IdentityProviderAuthenticationFailure`

+ **Unknown user:** `ClientAuthenticationSuccess` -> `UserNotFound` -> `PrincipalAuthenticationFailure` -> `IdentityProviderAuthenticationFailure`