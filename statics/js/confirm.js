!function(){"use strict";var e=document.querySelector(".menu-toggle"),a=document.querySelector("#sidebar-wrapper");e&&e.addEventListener("click",(function(s){s.preventDefault(),a.classList.toggle("active"),e.classList.toggle("active");var t=e.querySelector(".fa-bars, .fa-times");t&&(t.classList.contains("fa-times")?(t.classList.remove("fa-times"),t.classList.add("fa-bars")):t.classList.contains("fa-bars")&&(t.classList.remove("fa-bars"),t.classList.add("fa-times")))}));var s=document.querySelector(".navbar-collapse");if(s){var t=s.querySelectorAll("a");for(var r of t)r.addEventListener("click",(function(s){a.classList.remove("active"),e.classList.remove("active");var t=e.querySelector(".fa-bars, .fa-times");t&&(t.classList.contains("fa-times")?(t.classList.remove("fa-times"),t.classList.add("fa-bars")):t.classList.contains("fa-bars")&&(t.classList.remove("fa-bars"),t.classList.add("fa-times")))}))}var i=document.querySelector(".scroll-to-top");i&&window.addEventListener("scroll",(function(){var e=window.pageYOffset;i.style.display=e>100?"block":"none"}))}();var onMapMouseleaveHandler=function(e){this.addEventListener("click",onMapClickHandler),this.removeEventListener("mouseleave",onMapMouseleaveHandler);var a=this.querySelector("iframe");a&&(a.style.pointerEvents="none")},onMapClickHandler=function(e){this.removeEventListener("click",onMapClickHandler),this.addEventListener("mouseleave",onMapMouseleaveHandler);var a=this.querySelector("iframe");a&&(a.style.pointerEvents="auto")},maps=document.querySelectorAll(".map");for(var map of maps)map.addEventListener("click",onMapClickHandler);