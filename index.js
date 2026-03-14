const AboutButton = document.querySelector("#AboutButton");
const PreviousWorkButton = document.querySelector("#PreviousWorkButton");
const ProjectsButton = document.querySelector("#ProjectsButton");
const ContactsButton = document.querySelector("#ContactsButton");
var AboutSection = document.getElementById("About");
var PreviousWorkSection = document.getElementById("PreviousWork");
var ProjectsSection = document.getElementById("Projects");
var ContactSection = document.getElementById("Contact");

AboutButton.addEventListener("click", handleAboutClick);
PreviousWorkButton.addEventListener("click", handlePreviousWorkClick);
ProjectsButton.addEventListener("click", handleProjectsClick);
ContactsButton.addEventListener("click", handleContactClick);

function handleAboutClick(event) {
  console.log("About Button Clicked");
  AboutSection.style.display = "grid";
  PreviousWorkSection.style.display = "none";
  ProjectsSection.style.display = "none";
  ContactSection.style.display = "none";
}

function handlePreviousWorkClick(event) {
  console.log("Previous Work Button Clicked");
  AboutSection.style.display = "none";
  PreviousWorkSection.style.display = "block";
  ProjectsSection.style.display = "none";
  ContactSection.style.display = "none";
}

function handleProjectsClick(event) {
  console.log("Projects Button Clicked");
  AboutSection.style.display = "none";
  PreviousWorkSection.style.display = "none";
  ProjectsSection.style.display = "block";
  ContactSection.style.display = "none";
}

function handleContactClick(event) {
  console.log("Contact Button Clicked");
  AboutSection.style.display = "none";
  PreviousWorkSection.style.display = "none";
  ProjectsSection.style.display = "none";
  ContactSection.style.display = "block";
}
