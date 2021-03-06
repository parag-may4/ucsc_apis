# Copyright 2017 Cisco Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
This module performs the operation related to ldap.
"""
from ucscsdk.ucscexception import UcscOperationError
from ..admin.locale import locale_exists
from ..common.utils import get_device_profile_dn
ucsc_base_dn = get_device_profile_dn(name="default")


def ldap_provider_create(handle, name, order="lowest-available", rootdn=None,
                         basedn="", port="389", enable_ssl="no", filter=None,
                         attribute=None, key=None, timeout="30",
                         vendor="OpenLdap", retries="1",
                         descr=None, **kwargs):
    """
    creates a ldap provider

    Args:
        handle (UcscHandle)
        name (string): name of ldap provider
        order (string): "lowest-available" or 0-16
        rootdn (string): rootdn
        basedn (string): basedn
        port (string): port
        enable_ssl (string): enable_ssl
        filter (string): filter
        attribute (string): attribute
        key (string): key
        timeout (string): timeout
        vendor (string): vendor
        retries (string): retries
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaLdapProvider : Managed Object

    Example:
        ldap_provider_create(handle, name="test_ldap_prov", port="320",
                             order="3")
    """

    from ucscsdk.mometa.aaa.AaaLdapProvider import AaaLdapProvider

    dn = ucsc_base_dn + "/ldap-ext"
    ldap_mo = handle.query_dn(dn)
    if not ldap_mo:
        raise UcscOperationError("ldap_provider_create",
                                 "LDAP MO doesn't exist")

    mo = AaaLdapProvider(parent_mo_or_dn=dn,
                         name=name,
                         order=order,
                         rootdn=rootdn,
                         basedn=basedn,
                         port=port,
                         enable_ssl=enable_ssl,
                         filter=filter,
                         attribute=attribute,
                         key=key,
                         timeout=timeout,
                         vendor=vendor,
                         retries=retries,
                         descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_provider_get(handle, name):
    """
    Gets the ldap provider

    Args:
        handle (UcscHandle)
        name (string): name of ldap provider

    Returns:
        AaaLdapProvider : Managed Object OR None

    Example:
        ldap_provider_get(handle, name="test_ldap_provider")
    """

    dn = ucsc_base_dn + "/ldap-ext/provider-" + name
    return handle.query_dn(dn)


def ldap_provider_exists(handle, name, **kwargs):
    """
    checks if ldap provider exists

    Args:
        handle (UcscHandle)
        name (string): name of ldap provider
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        ldap_provider_exists(handle, name="test_ldap_provider")
    """

    mo = ldap_provider_get(handle, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_provider_modify(handle, name, **kwargs):
    """
    modifies a ldap provider

    Args:
        handle (UcscHandle)
        name (string): name of ldap provider
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        AaaLdapProvider : Managed Object

    Raises:
        UcscOperationError: If AaaLdapProvider is not present

    Example:
        ldap_provider_modify(handle, name="test_ldap_prov", enable_ssl="yes")
    """

    mo = ldap_provider_get(handle, name)
    if not mo:
        raise UcscOperationError("ldap_provider_modify",
                                 "Ldap Provider does not exist")

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def ldap_provider_delete(handle, name):
    """
    deletes a ldap provider

    Args:
        handle (UcscHandle)
        name (string): name of ldap provider

    Returns:
        None

    Raises:
        UcscOperationError: If AaaLdapProvider is not present

    Example:
        ldap_provider_delete(handle, name="test_ldap_prov")
    """

    mo = ldap_provider_get(handle, name)
    if not mo:
        raise UcscOperationError("ldap_provider_delete",
                                 "Ldap Provider does not exist")

    handle.remove_mo(mo)
    handle.commit()


def ldap_provider_group_rules_configure(handle, ldap_provider_name,
                                        authorization=None, traversal=None,
                                        target_attr=None, name=None,
                                        descr=None, **kwargs):
    """
    configures group rules of a ldap provider

    Args:
        handle (UcscHandle)
        ldap_provider_name (string): name of ldap provider
        authorization (string): authorization
        traversal (string): traversal
        target_attr (string): target_attr
        name (string): name
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaLdapGroupRule : Managed Object

    Example:
        ldap_provider_group_rules_configure(
              handle,
              ldap_provider_name="test_ldap_prov", authorization="enable")
    """

    from ucscsdk.mometa.aaa.AaaLdapGroupRule import AaaLdapGroupRule

    dn = ucsc_base_dn + "/ldap-ext/provider-" + ldap_provider_name
    obj = handle.query_dn(dn)
    if not obj:
        raise UcscOperationError("ldap_provider_group_rules_configure",
                                 "Ldap Provider does not exist.")

    mo = AaaLdapGroupRule(parent_mo_or_dn=obj)

    args = {'authorization': authorization,
            'traversal': traversal,
            'target_attr': target_attr,
            'name': name,
            'descr': descr
            }

    mo.set_prop_multiple(**args)
    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_group_map_create(handle, name, descr=None, **kwargs):
    """
    creates ldap group map

    Args:
        handle (UcscHandle)
        name (string): name
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaLdapGroup : Managed Object

    Example:
        ldap_group_map_create(handle, name="test_ldap_grp_map")
    """

    from ucscsdk.mometa.aaa.AaaLdapGroup import AaaLdapGroup

    mo = AaaLdapGroup(parent_mo_or_dn=ucsc_base_dn + "/ldap-ext",
                      name=name, descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_group_map_get(handle, name):
    """
    Gets ldap group map

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        AaaLdapGroup : Managed Object OR None

    Example:
        ldap_group_map_get(handle, name="test_ldap_group_map")
    """

    dn = ucsc_base_dn + "/ldap-ext/ldapgroup-" + name
    return handle.query_dn(dn)


def ldap_group_map_exists(handle, name, **kwargs):
    """
    checks if ldap group map exists

    Args:
        handle (UcscHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        ldap_group_map_exists(handle, name="test_ldap_group_map")
    """

    mo = ldap_group_map_get(handle, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_group_map_delete(handle, name):
    """
    removes ldap group map

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        None

    Raises:
        UcscOperationError: If AaaLdapGroup is not present

    Example:
        ldap_group_map_delete(handle, name="test_ldap_grp_map")
    """

    mo = ldap_group_map_get(handle, name)
    if not mo:
        raise UcscOperationError("ldap_group_map_delete",
                                 "Ldap Group does not exist")

    handle.remove_mo(mo)
    handle.commit()


def ldap_group_map_role_add(handle, ldap_group_map_name, name, descr=None,
                            **kwargs):
    """
    add role to ldap group map

    Args:
        handle (UcscHandle)
        ldap_group_map_name (string): name of ldap group
        name (string):  role name
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUserRole : Managed Object

    Example:
        ldap_group_map_role_add(
          handle, ldap_group_map_name="test_ldap_grp_map", name="storage")
    """

    from ucscsdk.mometa.aaa.AaaUserRole import AaaUserRole

    dn = ucsc_base_dn + "/ldap-ext/ldapgroup-" + ldap_group_map_name
    obj = handle.query_dn(dn)
    if not obj:
        raise UcscOperationError("ldap_group_map_role_add",
                                 "Ldap Group map '%s' does not exist" % dn)

    mo = AaaUserRole(parent_mo_or_dn=obj, name=name, descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_group_map_role_get(handle, ldap_group_map_name, name):
    """
    Gets the role  for the respective ldap group map

    Args:
        handle (UcscHandle)
        ldap_group_map_name (string): name of ldap group
        name (string):  role name

    Returns:
        AaaUserRole : Managed Object OR None

    Example:
        ldap_group_map_role_get(handle,
                                ldap_group_map_name="test_ldap_grp_map",
                                name="test_role")
    """

    ldap_dn = ucsc_base_dn + "/ldap-ext/ldapgroup-" + ldap_group_map_name
    dn = ldap_dn + "/role-" + name
    return handle.query_dn(dn)


def ldap_group_map_role_exists(handle, ldap_group_map_name, name, **kwargs):
    """
    checks if role exists for the respective ldap group map

    Args:
        handle (UcscHandle)
        ldap_group_map_name (string): name of ldap group
        name (string):  role name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        ldap_group_map_role_exists(handle,
                                   ldap_group_map_name="test_ldap_grp_map",
                                   name="test_role")
    """

    mo = ldap_group_map_role_get(handle, ldap_group_map_name, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_group_map_role_remove(handle, ldap_group_map_name, name):
    """
    removes role from the respective ldap group map

    Args:
        handle (UcscHandle)
        ldap_group_map_name (string): name of ldap group
        name (string):  role name

    Returns:
        None

    Raises:
        UcscOperationError: If AaaUserRole is not present

    Example:
        ldap_group_map_role_remove(handle,
                                   ldap_group_map_name="test_ldap_grp_map",
                                   name="test_role")
    """

    mo = ldap_group_map_role_get(handle, ldap_group_map_name, name)
    if not mo:
        raise UcscOperationError("ldap_group_map_role_remove",
                                 "Ldap Group Role does not exist")

    handle.remove_mo(mo)
    handle.commit()


def ldap_group_map_locale_add(handle, ldap_group_map_name, name, descr=None,
                            **kwargs):
    """
    add locale to ldap group map

    Args:
        handle (UcscHandle)
        ldap_group_map_name (string): name of ldap group
        name (string):  locale name
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaUserLocale : Managed Object

    Example:
        ldap_group_map_locale_add(
          handle, ldap_group_map_name="test_ldap_grp_map", name="locale1")
    """

    from ucscsdk.mometa.aaa.AaaUserLocale import AaaUserLocale

    dn = ucsc_base_dn + "/ldap-ext/ldapgroup-" + ldap_group_map_name
    obj = handle.query_dn(dn)
    if not obj:
        raise UcscOperationError("ldap_group_map_locale_add",
                                 "Ldap Group map '%s' does not exist" % dn)

    if not locale_exists(handle, name=name)[0]:
        raise UcscOperationError("ldap_group_map_locale_add",
                                 "Locale '%s' does not exist" % name)

    mo = AaaUserLocale(parent_mo_or_dn=obj, name=name, descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_group_map_locale_get(handle, ldap_group_map_name, name):
    """
    Gets the locale for the respective ldap group map

    Args:
        handle (UcscHandle)
        ldap_group_map_name (string): name of ldap group
        name (string):  locale name

    Returns:
        AaaUserLocale : Managed Object OR None

    Example:
        ldap_group_map_locale_get(handle,
                                ldap_group_map_name="test_ldap_grp_map",
                                name="locale1")
    """

    ldap_dn = ucsc_base_dn + "/ldap-ext/ldapgroup-" + ldap_group_map_name
    dn = ldap_dn + "/locale-" + name
    return handle.query_dn(dn)


def ldap_group_map_locale_exists(handle, ldap_group_map_name, name, **kwargs):
    """
    checks if locale exists for the respective ldap group map

    Args:
        handle (UcscHandle)
        ldap_group_map_name (string): name of ldap group
        name (string):  locale name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        ldap_group_map_locale_exists(handle,
                                   ldap_group_map_name="test_ldap_grp_map",
                                   name="locale1")
    """

    mo = ldap_group_map_locale_get(handle, ldap_group_map_name, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_group_map_locale_remove(handle, ldap_group_map_name, name):
    """
    removes locale from the respective ldap group map

    Args:
        handle (UcscHandle)
        ldap_group_map_name (string): name of ldap group
        name (string):  locale name

    Returns:
        None

    Raises:
        UcscOperationError: If AaaUserLocale is not present

    Example:
        ldap_group_map_locale_remove(handle,
                                   ldap_group_map_name="test_ldap_grp_map",
                                   name="locale1")
    """

    mo = ldap_group_map_locale_get(handle, ldap_group_map_name, name)
    if not mo:
        raise UcscOperationError("ldap_group_map_locale_remove",
                                 "Ldap Group Locale does not exist")

    if not locale_get(handle, name=name)[0]:
        raise UcscOperationError("ldap_group_map_locale_remove",
                                 "Locale '%s' does not exist" % name)
    handle.remove_mo(mo)
    handle.commit()

def ldap_provider_group_create(handle, name, descr=None, **kwargs):
    """
    creates ldap provider group

    Args:
        handle (UcscHandle)
        name (string): name
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaProviderGroup : Managed Object

    Example:
        ldap_provider_group_create(handle, name="test_ldap_group_map")
    """

    from ucscsdk.mometa.aaa.AaaProviderGroup import AaaProviderGroup

    mo = AaaProviderGroup(parent_mo_or_dn=ucsc_base_dn + "/ldap-ext",
                          name=name,
                          descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_provider_group_get(handle, name):
    """
    Gets ldap provider group

    Args:
        handle (UcscHandle)
        name (string): name

    Returns:
        AaaProviderGroup : Managed Object OR None

    Example:
        ldap_provider_group_get(handle, name="test_ldap_group_map")
    """

    dn = ucsc_base_dn + "/ldap-ext/providergroup-" + name
    return handle.query_dn(dn)


def ldap_provider_group_exists(handle, name, **kwargs):
    """
    checks if ldap provider group exists

    Args:
        handle (UcscHandle)
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        ldap_provider_group_exists(handle, name="test_ldap_group_map")
    """

    mo = ldap_provider_group_get(handle, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_provider_group_delete(handle, name):
    """
    deletes ldap provider group

    Args:
        handle (UcscHandle)
        name (string): name
        descr (string): descr

    Returns:
        None

    Raises:
        UcscOperationError: If AaaProviderGroup is not present

    Example:
        ldap_provider_group_delete(handle, name="test_ldap_group_map")
    """

    mo = ldap_provider_group_get(handle, name)
    if not mo:
        raise UcscOperationError("ldap_provider_group_delete",
                                 "Provider  Group does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def ldap_provider_group_provider_add(handle, group_name, name,
                                     order="lowest-available",
                                     descr=None, **kwargs):
    """
    adds provider to ldap provider group

    Args:
        handle (UcscHandle)
        group_name (string): ldap provider group name
        name (string): name
        order (string): order
        descr (string): descr
        **kwargs: Any additional key-value pair of managed object(MO)'s
                  property and value, which are not part of regular args.
                  This should be used for future version compatibility.
    Returns:
        AaaProviderRef : Managed Object

    Raises:
        UcscOperationError: If AaaProviderGroup or AaaProvider is not present

    Example:
        ldap_provider_group_provider_add(handle,
                                        group_name="test_ldap_provider_group",
                                        name="test_provider",
                                        order="1")
    """

    from ucscsdk.mometa.aaa.AaaProviderRef import AaaProviderRef

    group_dn = ucsc_base_dn + "/ldap-ext/providergroup-" + group_name
    group_mo = handle.query_dn(group_dn)
    if not group_mo:
        raise UcscOperationError("ldap_provider_group_provider_add",
                                 "Ldap Provider Group does not exist.")

    provider_dn = ucsc_base_dn + "/ldap-ext/provider-" + name
    provider_mo = handle.query_dn(provider_dn)
    if not provider_mo:
        raise UcscOperationError("ldap_provider_group_provider_add",
                                 "Ldap Provider does not exist.")

    mo = AaaProviderRef(parent_mo_or_dn=group_mo,
                        name=name,
                        order=order,
                        descr=descr)

    mo.set_prop_multiple(**kwargs)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def ldap_provider_group_provider_get(handle, group_name, name):
    """
    Gets provider for ldap provider group

    Args:
        handle (UcscHandle)
        group_name (string): ldap provider group name
        name (string): name

    Returns:
        AaaProviderRef : Managed Object OR None

    Example:
        ldap_provider_group_provider_get(handle,
                                         group_name="test_ldap_provider_group",
                                         name="test_provider",
                                         order="1")
    """

    group_dn = ucsc_base_dn + "/ldap-ext/providergroup-" + group_name
    provider_dn = group_dn + "/provider-ref-" + name
    return handle.query_dn(provider_dn)


def ldap_provider_group_provider_exists(handle, group_name, name, **kwargs):
    """
    checks if provider added ldap provider group

    Args:
        handle (UcscHandle)
        group_name (string): ldap provider group name
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        (True/False, MO/None)

    Example:
        ldap_provider_group_provider_exists(handle,
                                            group_name="test_ldap_provider_group",
                                            name="test_provider",
                                            order="1")
    """

    mo = ldap_provider_group_provider_get(handle, group_name, name)
    if not mo:
        return (False, None)
    mo_exists = mo.check_prop_match(**kwargs)
    return (mo_exists, mo if mo_exists else None)


def ldap_provider_group_provider_modify(handle, group_name, name, **kwargs):
    """
    modify provider of ldap provider group

    Args:
        handle (UcscHandle)
        group_name (string): ldap provider group name
        name (string): name
        **kwargs: key-value pair of managed object(MO) property and value, Use
                  'print(ucsccoreutils.get_meta_info(<classid>).config_props)'
                  to get all configurable properties of class

    Returns:
        True/False

    Raises:
        AaaProviderRef : Managed Object

    Example:
        ldap_provider_group_provider_modify(handle,
                                            group_name="test_ldap_provider_group",
                                            name="test_provider",
                                            order="1")
    """

    mo = ldap_provider_group_provider_get(handle, group_name, name)
    if not mo:
        raise UcscOperationError("ldap_provider_group_provider_modify",
                                 "Provider not available under group.")

    mo.set_prop_multiple(**kwargs)
    handle.set_mo(mo)
    handle.commit()
    return mo


def ldap_provider_group_provider_remove(handle, group_name, name):
    """
    removes provider from ldap provider group

    Args:
        handle (UcscHandle)
        group_name (string): ldap provider group name
        name (string): name

    Returns:
        None

    Raises:
        UcscOperationError: If AaaProviderRef is not present

    Example:
        ldap_provider_group_provider_remove(handle,
                                            group_name="test_ldap_provider_group",
                                            name="test_provider")
    """

    mo = ldap_provider_group_provider_get(handle, group_name, name)
    if not mo:
        raise UcscOperationError("ldap_provider_group_provider_remove",
                                 "Provider not available under group.")

    handle.remove_mo(mo)
    handle.commit()
