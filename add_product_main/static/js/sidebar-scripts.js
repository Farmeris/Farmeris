function submitForm() {
    document.getElementById('languageForm').submit();
}

// Hide the submit button with JavaScript
document.getElementById('submitButton').style.display = 'none';

// Set Slovak as the default language for first-time visitors
window.onload = function() {
  // Check if the user has visited the site before using a cookie
  if (document.cookie.indexOf('visited_before=true') === -1) {
      // User hasn't visited before. Set the language to Slovak.
      let languageSelect = document.querySelector("select[name='language']");
      if (languageSelect) {
          languageSelect.value = 'sk';
          submitForm(); // Use the submitForm function to submit the language change form

          // Set a cookie to mark that the user has visited before
          var expires = new Date();
          expires.setTime(expires.getTime() + (365 * 24 * 60 * 60 * 1000)); // 1 year expiration
          document.cookie = "visited_before=true; expires=" + expires.toUTCString();
      }
  }
};
document.addEventListener('click', function(e) {
const sidebarMenuContent = document.querySelector('.sidebar-menu-content');
const sidebarMenuButton = document.querySelector('.sidebar-menu-button');
const menuToggle = document.getElementById('menuToggle');

let clickedInsideMenu = sidebarMenuContent.contains(e.target) || sidebarMenuButton.contains(e.target);

if (clickedInsideMenu) {
  // If the sidebar button was clicked, stop the default behavior
  if (sidebarMenuButton.contains(e.target)) {
    e.preventDefault();

    // Toggle the checkbox state
    menuToggle.checked = !menuToggle.checked;
  }
} else {
  menuToggle.checked = false;
}
});