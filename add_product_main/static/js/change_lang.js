document.addEventListener('DOMContentLoaded', function() {
  var languageSelector = document.querySelector('.sidebar-menu-item-lang');
  console.log('Language selector:', languageSelector); // Should not be null

  if (languageSelector) {
    languageSelector.addEventListener('change', function() {
      console.log('Language changed to:', this.value); // Check if this logs
      var form = document.getElementById('languageForm');
      console.log('Form:', form); // Should not be null
      if (form) {
        form.submit();
      }
    });
  }
});
