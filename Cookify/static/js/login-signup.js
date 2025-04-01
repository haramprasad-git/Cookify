const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');

const container = document.getElementById('container');

const fileInput = document.getElementById('profilePic');
const costomfileInput = document.getElementsByClassName('fake-profilePic')[0];

const editForm = document.getElementById('editForm');
const socialMediaForm = document.getElementById('socialMediaForm');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

fileInput.addEventListener('change', (event) => {
	costomfileInput.children[1].innerHTML = "Click to Change Profile Picture";

 	const fileInputIcon = costomfileInput.children[0];
	fileInputIcon.classList.add("fa-check");
	fileInputIcon.classList.remove("fa-folder-open");
});

if (socialMediaForm != undefined) {
	editForm.addEventListener('submit', () => {
		socialMediaForm.submit();
	});
}
