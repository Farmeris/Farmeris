document.addEventListener('click', function(event) {
  var sidebarMenu = document.querySelector('.sidebar-menu');
  var menuToggleCheckbox = document.getElementById('menuToggle');

  // Check if the clicked area is outside the sidebar menu
  if (sidebarMenu && !sidebarMenu.contains(event.target)) {
    // Uncheck the menu toggle checkbox
    menuToggleCheckbox.checked = false;
  }
});
