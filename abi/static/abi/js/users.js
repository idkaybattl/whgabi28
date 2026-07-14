
// global storage for all viewable projects
let allUsers = [];

function filterProjects(widget) {
  const searchInput = widget.querySelector("[data-user-search]");
  const term = searchInput.value.toLowerCase();
  const user_grid = widget.querySelector(".projects-grid");

  if (user_grid.querySelector(".empty-users")) { return; }

  if (term.trim() == "") {
    allUsers.forEach((option) => user_grid.appendChild(option));
    return;
  }

  const visibleOptions = term
    ? searchItems(term, allUsers, (option) => [
      option.querySelector("#name").innerHTML,
      option.querySelector("#mail").innerHTML,
      option.querySelector("#external-mail").innerHTML,
    ])
    : allUsers.sort(
      (a, b) =>
        a.querySelector("#name").innerHTML.localeCompare(
          b.querySelector("#name").innerHTML, "de"
        )
    );

  user_grid.innerHTML = "";
  visibleOptions.forEach((option) => user_grid.appendChild(option));
}

document.addEventListener("DOMContentLoaded", () => {
  const widget = document.querySelector(".user-page");

  const searchInput = widget.querySelector("[data-user-search]");
  searchInput.addEventListener("input", () => filterProjects(widget));

  allUsers = Array.from(document.querySelectorAll(".user-card"));
  filterProjects(widget);
});
