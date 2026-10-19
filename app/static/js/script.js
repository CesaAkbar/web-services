document.addEventListener("DOMContentLoaded", function() {
  document.documentElement.style.visibility = "visible";
  document.documentElement.style.opacity = "1";
});

const sidebarButton = document.getElementById('sidebar-button')
const sidebar = document.getElementById('sidebar')

sidebarButton.addEventListener('click', () => {
    sidebar.classList.toggle('d-none')
})

console.log('javascript is running...')