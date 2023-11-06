document.addEventListener("DOMContentLoaded", function() {
    var select = document.getElementById("itemsPerPageSelect");
  
    if (select) {
      select.addEventListener("change", function() {
        // Automatically submit the form when the select value changes
        select.form.submit();
      });
    }
  });