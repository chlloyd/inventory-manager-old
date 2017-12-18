"""
Authentication Module

Provides Users and manages their permissions for the rest of the modules

GraphQL Queries & Mutations

- Login - Mutation to login a user.
  - Requires a email & password.
  - Return a JWT token
- Register User - Register a user.
  - Requires create user permission
  - Check current JWT token.
  - Requires email, password, name
- Add User to Group
  - Requires a user & a group.
  - Requires create user_group permission.
- Remove User from Group
  - Requires a user & a group.
  - Requires delete user_group permission.
- Add Permission to Group
  - Requires a group & permission
  - Requires create group_permission permission.
- Remove Permission from Group
  - Requires a group & permission
  - Requires delete group_permission permission.
- (Custom Permissions ?)

"""
