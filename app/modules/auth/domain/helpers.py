def normalize_roles(roles):
    if isinstance(roles, list):
        return [role["role"]["role_name"] if isinstance(role, dict) and "role" in role and "role_name" in role["role"] else role for role in roles]
    return roles