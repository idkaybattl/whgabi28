function getPopupById(id) {
  if (!id) {
    return null;
  }
  return document.getElementById(id);
}

function openPopupById(id) {
  const popup = getPopupById(id);
  if (!popup) {
    return;
  }
  popup.classList.add("popup--open");
}

function closePopup(popup) {
  if (!popup) {
    return;
  }
  popup.classList.remove("popup--open");
}

function closeAllPopups() {
  document
    .querySelectorAll("[data-popup].popup--open")
    .forEach((popup) => closePopup(popup));
}

function pad2(value) {
  return String(value).padStart(2, "0");
}

function formatDateTimeLocal(date) {
  return (
    date.getFullYear() +
    "-" +
    pad2(date.getMonth() + 1) +
    "-" +
    pad2(date.getDate()) +
    "T" +
    pad2(date.getHours()) +
    ":" +
    pad2(date.getMinutes())
  );
}

function getNowRoundedToMinute() {
  const now = new Date();
  now.setSeconds(0, 0);
  return now;
}

function parseDateTimeLocal(value) {
  if (!value) {
    return null;
  }

  const [datePart, timePart] = value.split("T");
  if (!datePart || !timePart) {
    return null;
  }

  const [year, month, day] = datePart.split("-").map(Number);
  const [hours, minutes] = timePart.split(":").map(Number);

  if ([year, month, day, hours, minutes].some((number) => Number.isNaN(number))) {
    return null;
  }

  return new Date(year, month - 1, day, hours, minutes, 0, 0);
}

function updateProjectFormDateValidation(form) {
  const startInput = form.querySelector("input[name$='starting_date']");
  const endInput = form.querySelector("input[name$='ending_date']");

  if (!startInput || !endInput) {
    return true;
  }

  const now = getNowRoundedToMinute();
  const nowString = formatDateTimeLocal(now);

  startInput.min = nowString;
  endInput.min = startInput.value || nowString;

  startInput.setCustomValidity("");
  endInput.setCustomValidity("");

  const startDate = parseDateTimeLocal(startInput.value);
  const endDate = parseDateTimeLocal(endInput.value);

  if (startDate && startDate <= now) {
    startInput.setCustomValidity("Der Beginn muss in der Zukunft liegen.");
  }

  if (startDate && endDate && endDate <= startDate) {
    endInput.setCustomValidity("Das Ende muss nach dem Beginn liegen.");
  }

  return form.checkValidity();
}

function initProjectFormValidation(form) {
  const startInput = form.querySelector("input[name$='starting_date']");
  const endInput = form.querySelector("input[name$='ending_date']");
  if (!startInput || !endInput) {
    return;
  }

  const update = () => updateProjectFormDateValidation(form);
  startInput.addEventListener("input", update);
  startInput.addEventListener("change", update);
  endInput.addEventListener("input", update);
  endInput.addEventListener("change", update);

  form.addEventListener("submit", (event) => {
    const isValid = updateProjectFormDateValidation(form);
    if (!isValid) {
      event.preventDefault();
      form.reportValidity();
    }
  });

  update();
}

document.addEventListener("click", (event) => {
  const openTrigger = event.target.closest("[data-popup-open]");
  if (openTrigger) {
    openPopupById(openTrigger.dataset.popupOpen);
    return;
  }

  const switchTrigger = event.target.closest("[data-popup-switch]");
  if (switchTrigger) {
    closePopup(switchTrigger.closest("[data-popup]"));
    openPopupById(switchTrigger.dataset.popupSwitch);
    return;
  }

  const closeTrigger = event.target.closest("[data-popup-close]");
  if (closeTrigger) {
    closePopup(closeTrigger.closest("[data-popup]"));
    return;
  }

  if (event.target.matches("[data-popup]")) {
    closePopup(event.target);
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") {
    return;
  }
  closeAllPopups();
});

document.addEventListener("DOMContentLoaded", () => {
  document
    .querySelectorAll("form[data-project-form]")
    .forEach((form) => initProjectFormValidation(form));

  const initialPopupMarker = document.querySelector("[data-popup-initial]");
  if (!initialPopupMarker) {
    return;
  }
  openPopupById(initialPopupMarker.dataset.popupInitial);
});
