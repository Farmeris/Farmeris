// Event listener for hiding the submit button and setting the default language
document.addEventListener('DOMContentLoaded', function() {
  // Hide the submit button
  var submitButton = document.getElementById('submitButton');
  if (submitButton) {
    submitButton.style.display = 'none';
  }

  // Set Slovak as the default language for first-time visitors
  if (document.cookie.indexOf('visited_before=true') === -1) {
    var languageSelect = document.querySelector("select[name='language']");
    if (languageSelect) {
      languageSelect.value = 'sk';
      submitForm(); // Use the submitForm function to submit the language change form

      // Set a cookie to mark that the user has visited before
      var expires = new Date();
      expires.setTime(expires.getTime() + (365 * 24 * 60 * 60 * 1000)); // 1 year expiration
      document.cookie = "visited_before=true; expires=" + expires.toUTCString();
    }
  }
});

// Function to submit the language form
function submitForm() {
  document.getElementById('languageForm').submit();
}

// Event listener for sidebar menu interactions
document.addEventListener('click', function(e) {
  const sidebarMenuContent = document.querySelector('.sidebar-menu-content');
  const sidebarMenuButton = document.querySelector('.sidebar-menu-button');
  const menuToggle = document.getElementById('menuToggle');

  let clickedInsideMenu = sidebarMenuContent.contains(e.target) || sidebarMenuButton.contains(e.target);

  if (clickedInsideMenu) {
    if (sidebarMenuButton.contains(e.target)) {
      e.preventDefault();
      menuToggle.checked = !menuToggle.checked;
    }
  } else {
    menuToggle.checked = false;
  }
});
