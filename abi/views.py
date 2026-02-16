from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from .forms import ProjectForm
from .models import Project

User = get_user_model()


def abi(request):
    return render(request, "index.html")


def calendar(request):
    return render(request, "calendar.html")


@login_required
def projects(request):
    username_field = User.USERNAME_FIELD
    participants_queryset = User.objects.all().order_by(username_field)
    all_users = list(participants_queryset)
    projects = list(
        Project.objects.filter(starting_date__gte=now()).order_by("starting_date")
    )

    def build_project_form(*, instance=None, data=None, prefix=None):
        return ProjectForm(
            data=data,
            instance=instance,
            prefix=prefix,
            users=all_users,
            participants_queryset=participants_queryset,
        )

    def build_project_forms(overrides=None):
        overrides = overrides or {}
        return [
            (
                project,
                overrides.get(project.id)
                or build_project_form(instance=project, prefix=str(project.id)),
            )
            for project in projects
        ]

    if request.method == "POST":
        form_action = request.POST.get("form_action")

        if form_action == "create_project":
            create_form = build_project_form(data=request.POST, prefix="new")
            if create_form.is_valid():
                new_project = create_form.save(commit=False)
                new_project.creator = request.user
                new_project.save()
                create_form.save_m2m()
                return redirect("/projects")

            return render(
                request,
                "projects.html",
                {
                    "forms": build_project_forms(),
                    "create_form": create_form,
                    "form_media": create_form.media,
                    "initial_popup_id": "create-project-popup",
                },
            )

        project_id = request.POST.get("project_id")
        if project_id:
            project = get_object_or_404(Project, pk=project_id)
            edit_form = build_project_form(
                data=request.POST,
                instance=project,
                prefix=str(project.id),
            )

            if edit_form.is_valid():
                edit_form.save()
                return redirect("/projects")

            return render(
                request,
                "projects.html",
                {
                    "forms": build_project_forms(overrides={project.id: edit_form}),
                    "create_form": build_project_form(prefix="new"),
                    "form_media": edit_form.media,
                    "initial_popup_id": f"edit-{project.id}",
                },
            )

        return redirect("/projects")

    create_form = build_project_form(prefix="new")
    project_forms = build_project_forms()

    return render(
        request,
        "projects.html",
        {
            "forms": project_forms,
            "create_form": create_form,
            "form_media": create_form.media,
        },
    )


@login_required
def join_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        if user_id:
            user = get_object_or_404(User, id=user_id)
            project.participants.add(user)

    return redirect("/projects")
