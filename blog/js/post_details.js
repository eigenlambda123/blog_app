// Automatic Slideshow
var myIndex = 0;
carousel();

function carousel() {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  myIndex++;
  if (myIndex > slides.length) { myIndex = 1 }
  slides[myIndex - 1].style.display = "block";
  setTimeout(carousel, 4000);
}

// Toggle Navbar
function toggleNav() {
  var x = document.getElementById("navDemo");
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
  } else {
    x.className = x.className.replace(" w3-show", "");
  }
}
