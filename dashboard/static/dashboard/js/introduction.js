document.getElementById('to-step-2')?.addEventListener('click', function () {
  document.getElementById('step-1').classList.add('hidden');
  document.getElementById('step-2').classList.remove('hidden');

  // If you want to focus the first input in the form:
  const firstInput = document.querySelector('#step-2 form input, #step-2 form textarea, #step-2 form select');
  if (firstInput) firstInput.focus();
});
