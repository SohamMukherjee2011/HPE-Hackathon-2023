const signinBtn = document.querySelector(".signin");
const signupBtn = document.querySelector(".signup");
const formbg = document.querySelector(".formbG");
const menu = document.querySelector(".hamburg");
const ab = document.querySelector(".hamburg.active");
const listed = document.querySelector(".list");
signupBtn.onclick = function () {
  formbg.classList.remove("right");
  formbg.classList.add("left");
  document.title = "Sign Up | HackStopper";
};
signinBtn.onclick = function () {
  formbg.classList.remove("left");
  formbg.classList.add("right");
  document.title = "Log In | HackStopper";
};
menu.onclick = function () {
  if (menu.classList.contains("active")) {
    menu.classList.remove("active");
    listed.classList.remove("active");
  } else if (menu.classList.contains("active") != true) {
    menu.classList.add("active");
    listed.classList.add("active");
  } else {
    alert("Error");
  }
};
