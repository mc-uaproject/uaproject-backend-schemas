#!/usr/bin/env python3
"""
Debug script to understand ResponseSelf schema behavior with is_superuser field
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'uaproject_backend_schemas'))

from uaproject_backend_schemas.models.user import User

def debug_response_self_schema():
    print("=== User Model Field Analysis ===")
    
    # Check the User model's is_superuser field definition
    is_superuser_field = User.model_fields.get('is_superuser')
    print(f"is_superuser field info: {is_superuser_field}")
    print(f"is_superuser required_permissions: {getattr(is_superuser_field, 'required_permissions', 'None')}")
    
    print("\n=== ResponseSelf Schema Analysis ===")
    
    # Get the ResponseSelf schema definition
    response_self_def = getattr(User.Schemas, 'ResponseSelf', None)
    print(f"ResponseSelf definition: {response_self_def}")
    print(f"ResponseSelf permissions: {getattr(response_self_def, 'permissions', 'None')}")
    
    # Create the ResponseSelf schema without permissions
    response_self_schema = User.schemas.response_self
    print(f"ResponseSelf schema fields: {list(response_self_schema.model_fields.keys())}")
    
    # Check if is_superuser is in the schema
    has_is_superuser = 'is_superuser' in response_self_schema.model_fields
    print(f"is_superuser in ResponseSelf schema: {has_is_superuser}")
    
    print("\n=== Testing with_permissions method ===")
    
    # Test with no permissions (should exclude is_superuser)
    schema_no_perms = response_self_schema.with_permissions([])
    print(f"Schema with no permissions - fields: {list(schema_no_perms.model_fields.keys())}")
    has_is_superuser_no_perms = 'is_superuser' in schema_no_perms.model_fields
    print(f"is_superuser with no permissions: {has_is_superuser_no_perms}")
    
    # Test with user.read.self permission (should exclude is_superuser)
    schema_self_perms = response_self_schema.with_permissions(['user.read.self'])
    print(f"Schema with user.read.self - fields: {list(schema_self_perms.model_fields.keys())}")
    has_is_superuser_self_perms = 'is_superuser' in schema_self_perms.model_fields
    print(f"is_superuser with user.read.self: {has_is_superuser_self_perms}")
    
    # Test with admin permission (should include is_superuser)
    schema_admin_perms = response_self_schema.with_permissions(['user.admin'])
    print(f"Schema with user.admin - fields: {list(schema_admin_perms.model_fields.keys())}")
    has_is_superuser_admin_perms = 'is_superuser' in schema_admin_perms.model_fields
    print(f"is_superuser with user.admin: {has_is_superuser_admin_perms}")
    
    print("\n=== Field Permission Analysis ===")
    
    # Check what permissions are required for is_superuser
    if is_superuser_field and hasattr(is_superuser_field, 'format_permissions'):
        formatted_perms = is_superuser_field.format_permissions(User)
        print(f"is_superuser formatted permissions: {formatted_perms}")
    
    # Check access field as well
    access_field = User.model_fields.get('access')
    print(f"access field info: {access_field}")
    if access_field and hasattr(access_field, 'format_permissions'):
        access_formatted_perms = access_field.format_permissions(User)
        print(f"access formatted permissions: {access_formatted_perms}")
    
    print("\n=== Schema Field Filtering Analysis ===")
    
    # Let's trace through the field filtering logic
    schemas_instance = User.schemas
    
    print(f"User.__scope_prefix__: {getattr(User, '__scope_prefix__', 'None')}")
    
    # Test _should_include_field method
    should_include_no_perms = schemas_instance._should_include_field(is_superuser_field, [])
    should_include_self_perms = schemas_instance._should_include_field(is_superuser_field, ['user.read.self'])
    should_include_admin_perms = schemas_instance._should_include_field(is_superuser_field, ['user.admin'])
    
    print(f"Should include is_superuser with no permissions: {should_include_no_perms}")
    print(f"Should include is_superuser with user.read.self: {should_include_self_perms}")
    print(f"Should include is_superuser with user.admin: {should_include_admin_perms}")

if __name__ == "__main__":
    debug_response_self_schema()