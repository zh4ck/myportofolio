def roles(request):
    is_editor = False
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        is_editor = user.groups.filter(name="Editor").exists() or user.has_perm("main.change_experience")
    return {
        "is_editor": is_editor,
    }
