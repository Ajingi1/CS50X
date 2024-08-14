document.addEventListener('DOMContentLoaded', function() {
    var sidebar = document.getElementById('sidebar');
    var sidebarToggle = document.getElementById('sidebarToggle');
    var sidebarTogglerCancel = document.getElementById('sidebar-toggler-cancel');
    var mainContent = document.getElementById('main-content');

    if (sidebar){
        // Initial check for sidebar display based on viewport width
        if (window.innerWidth < 768) {
            sidebar.classList.add('hide');
            mainContent.style.marginLeft = '0px'; 
        } else {
            sidebar.classList.add('show');
            mainContent.style.marginLeft = '100px';
        }
        // Function to toggle sidebar visibility
        function toggleSidebar() {
            if (sidebar.classList.contains('show')) {
                sidebar.classList.remove('show');
                sidebar.classList.add('hide');
                mainContent.style.marginLeft = '0px'; // Adjust as per your layout
            } else {
                sidebar.classList.remove('hide');
                sidebar.classList.add('show');
                mainContent.style.marginLeft = '100px';
            }
        }

        // Event listener for sidebar toggle button
        sidebarToggle.addEventListener('click', function() {
            toggleSidebar();
        });

        // Event listener for sidebar cancel button
        sidebarTogglerCancel.addEventListener('click', function () {
            toggleSidebar();
        });
    }
});
