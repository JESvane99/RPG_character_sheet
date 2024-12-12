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

document.addEventListener("DOMContentLoaded", function() {
  let height = 0;
  document.querySelectorAll(".part-container").forEach(function(part) {
    height += Math.max(part.scrollHeight, part.offsetHeight) / 3.779528;
    if (height > 290) {
      part.style.breakBefore = "page";
      part.childNodes.forEach(function(child) {
        child.style.breakBefore = "avoid";
        child.style.breakInside = "avoid";
        child.style.breakAfter = "avoid";
      });
      return
    }
  });

});