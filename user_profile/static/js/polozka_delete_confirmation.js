function confirmDelete(productName) {
  if (typeof window.confirm === 'function') {
    return confirm(`Are you sure you want to delete the product "${productName}"?`);
  }
  return true;  // Allow deletion without confirmation if JavaScript is disabled
}
/*
document.addEventListener('DOMContentLoaded', function() {
  document.body.classList.add('js-enabled');
  
  let buttons = document.querySelectorAll('.product-vlastnosti-buttonx');

  function hidePopup(popup) {
      popup.style.opacity = '0';
      popup.style.visibility = 'hidden';
  }

  function showPopup(popup) {
      popup.style.opacity = '1';
      popup.style.visibility = 'visible';
  }

  buttons.forEach(button => {
      button.addEventListener('click', function() {
          let popupClass = this.getAttribute('data-popup');
          let popup = document.querySelector('.' + popupClass);

          // Positioning
          let rect = button.getBoundingClientRect();
          popup.style.top = rect.top + 'px';
          popup.style.left = rect.right + 'px';

          if(popup.style.opacity === '1') {
              hidePopup(popup);
          } else {
              // Hide all other popups first
              buttons.forEach(btn => {
                  let otherPopupClass = btn.getAttribute('data-popup');
                  let otherPopup = document.querySelector('.' + otherPopupClass);
                  hidePopup(otherPopup);
              });
              
              // Then, show the clicked popup
              showPopup(popup);
          }
      });
  });

  // Hide the popups when clicking outside of a button or popup
  document.addEventListener('click', function(event) {
      if (!event.target.matches('.product-vlastnosti-buttonx') && 
          !event.target.closest('.product-vlastnosti-popup1') && 
          !event.target.closest('.product-vlastnosti-popup2') && 
          !event.target.closest('.product-vlastnosti-popup3') && 
          !event.target.closest('.product-vlastnosti-popup4')) {
              
          buttons.forEach(btn => {
              let popupClass = btn.getAttribute('data-popup');
              let popup = document.querySelector('.' + popupClass);
              hidePopup(popup);
          });
      }
  });
});*/