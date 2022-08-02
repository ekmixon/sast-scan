"""This module contains alias helper functions for the expr_visitor module."""


def as_alias_handler(alias_list):
    """Returns a list of all the names that will be called."""
    list_ = []
    for alias in alias_list:
        if alias.asname:
            list_.append(alias.asname)
        else:
            list_.append(alias.name)
    return list_


def handle_aliases_in_calls(name, import_alias_mapping):
    """Returns either None or the handled alias.
    Used in add_module.
    """
    return next(
        (
            name.replace(key, val)
            for key, val in import_alias_mapping.items()
            if name == key or name.startswith(f"{key}.")
        ),
        None,
    )


def handle_aliases_in_init_files(name, import_alias_mapping):
    """Returns either None or the handled alias.
    Used in add_module.
    """
    return next(
        (
            name.replace(val, key)
            for key, val in import_alias_mapping.items()
            if name == val or name.startswith(f"{val}.")
        ),
        None,
    )


def handle_fdid_aliases(module_or_package_name, import_alias_mapping):
    """Returns either None or the handled alias.
    Used in add_module.
    fdid means from directory import directory.
    """
    return next(
        (
            key
            for key, val in import_alias_mapping.items()
            if module_or_package_name == val
        ),
        None,
    )


def not_as_alias_handler(names_list):
    """Returns a list of names ignoring any aliases."""
    return [alias.name for alias in names_list]


def retrieve_import_alias_mapping(names_list):
    """Creates a dictionary mapping aliases to their respective name.
    import_alias_names is used in module_definitions.py and visit_Call"""
    return {alias.asname: alias.name for alias in names_list if alias.asname}


def fully_qualify_alias_labels(label, aliases):
    """Replace any aliases in label with the fully qualified name.

    Args:
        label -- A label : str representing a name (e.g. myos.system)
        aliases -- A dict of {alias: real_name} (e.g. {'myos': 'os'})

    >>> fully_qualify_alias_labels('myos.mycall', {'myos':'os'})
    'os.mycall'
    """
    for alias, full_name in aliases.items():
        if label == alias:
            return full_name
        elif label.startswith(f"{alias}."):
            return full_name + label[len(alias) :]
    return label
