const btn = document.getElementById('to-step-2');

if (btn) {
  btn.addEventListener('click', function () {
    // hide step‑1, show step‑2
    document.getElementById('step-1').classList.add('hidden');
    document.getElementById('step-2').classList.remove('hidden');

    // focus the first input inside the form (if any)
    const firstInput = document.querySelector(
      '#step-2 form input, #step-2 form textarea, #step-2 form select'
    );
    if (firstInput) firstInput.focus();
  });
}
