# Third Party
import rules


@rules.predicate
def is_owner(user, obj):
    if owner := getattr(obj, "owner", None):
        return owner == user
    return False
