document.addEventListener('DOMContentLoaded', function() {

    // Tabs and content
    const tabLinks = document.querySelectorAll('.tab-item-link');
    const contentSections = document.querySelectorAll('.snapper');

    // Function to update the active tab
    function updateActiveTab(tabLinkElement) {
        // Remove active class from all tabs and hide all sections
        tabLinks.forEach(link => {
            link.classList.remove('active');
        });
        contentSections.forEach(section => {
            section.style.display = 'none';  // We're using inline styles to hide and show, for simplicity.
        });

        // Add active class to the clicked tab and display the related section
        tabLinkElement.classList.add('active');
        const targetId = tabLinkElement.getAttribute('data-target');
        const targetElement = document.getElementById(targetId);
        targetElement.style.display = 'block';
    }

    // Initially hide all content sections except the one that's active
    contentSections.forEach(section => {
        if (!section.previousElementSibling || !section.previousElementSibling.classList.contains('active')) {
            section.style.display = 'none';  // Hide if the tab isn't active
        }
    });

    // Add click event to tab links
    tabLinks.forEach(tabLink => {
        tabLink.addEventListener('click', function(event) {
            event.preventDefault();  // Prevent default anchor behavior
            updateActiveTab(this);
        });
    });
    // Automatically click the "Personal Profile" tab when the page loads
    const offersTab = document.querySelector('.tab-item-link[data-target="offers"]');
    if (offersTab) {
        offersTab.click();
    }
});