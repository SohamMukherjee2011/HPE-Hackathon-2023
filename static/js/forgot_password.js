const button = document.getElementById("btn");
const text = document.getElementById("txt");
button.onclick = function () {
  if (
    document.getElementById("blank").value ==
    document.getElementById("blankOne").value
  ) {
    text.classList.remove("show");
    text.innerText = "Password changed successfully";
    text.classList.add("match");
  } else if (
    document.getElementById("blank").value !=
    document.getElementById("blankOne").value
  ) {
    event.preventDefault();
    text.classList.remove("match");
    text.innerText = "Passwords do not match";
    text.classList.add("show");
    document.getElementById("blankOne").value = "";
  } else if (
    document.getElementById("blank").value == "" &&
    document.getElementById("blankOne").value == ""
  ) {
    event.preventDefault();

    text.classList.remove("match");
    text.innerText = "Please type your password";
    text.classList.add("show");
  } else {
    return 0;
  }
};
