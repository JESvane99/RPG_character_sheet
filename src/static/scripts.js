document.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll("textarea").forEach(function(textarea) {
      textarea.style.height = textarea.scrollHeight + "px";
      textarea.style.overflowY = "hidden";

      textarea.addEventListener("input", function() {
          this.style.height = "auto";
          this.style.height = this.scrollHeight + "px";
      });
  });
});


function adjustHeight(element1Id, element2Id) {
  let height1 = document.getElementById(element1Id).offsetHeight;
  let height2 = document.getElementById(element2Id).offsetHeight;
  if (height1 > height2) {
    document.getElementById(element2Id).style.height = height1 + "px";
  } else {
    document.getElementById(element1Id).style.height = height2 + "px";
  }
}


document.addEventListener("DOMContentLoaded", function() {
  adjustHeight("trappings", "notes");
});

document.addEventListener("DOMContentLoaded", function() {
  adjustHeight("ap-figure", "combat-column");
});