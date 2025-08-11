// IMPORTANT: This script runs when you navigate to the page with the modal.
//            This script is modifying HTML elements on the page after they load.
//            This script needs run AFTER the HTML is ran.

// Get the modal
const myElement = document.getElementById("recipe-modals");
for (const child of myElement.children) {
  console.log(child.id)
  document.getElementById("open"+child.id).onclick = function() {
    child.style.display = "block";
    console.log(child.id)
  }
  document.getElementById("close"+child.id).onclick = function() {
    child.style.display = "none";
    console.log(child.id)
  }
}


// Get the <span> element that closes the modal


// When the user clicks on the button, open the modal


// When the user clicks on <span> (x), close the modal


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  for (var child of myElement.children) {
    if (event.target == child) {
      child.style.display = "none";
    }
  }
}