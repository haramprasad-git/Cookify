const rightPanelButton = document.getElementById('rightPanel');
const leftPanelButton = document.getElementById('leftPanel');

const container = document.getElementById('container');

const fileInput = document.getElementById('profilePic');
const costomfileInput = document.getElementsByClassName('fake-profilePic')[0];

const editForm = document.getElementById('editForm');
const socialMediaForm = document.getElementById('socialMediaForm');

rightPanelButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

leftPanelButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});
