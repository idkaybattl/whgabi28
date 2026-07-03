from .forms import ProjectForm
from .models import Project
from .notifications import notify_participants


def save_project_form(form: ProjectForm, **kwargs) -> Project:
    project = form.instance

    if project.pk:  # if project instance existed before save
        old_participants = set(project.participants.all())
    else:
        old_participants = set()

    project = form.save(**kwargs)

    new_participants = set(project.participants.all())

    added = new_participants - old_participants
    removed = old_participants - new_participants

    notify_participants(project, added, removed)

    return project


def save_project(project: Project):

    project.save()

    old_project_state = Project.objects.get(pk=project.pk)
    if old_project_state:
        old_participants = set(old_project_state.participants.all())
    else:
        old_participants = set()

    new_participants = set(project.participants.all())  # pyright: ignore[reportAttributeAccessIssue]

    added = new_participants - old_participants
    removed = old_participants - new_participants

    notify_participants(project, added, removed)
