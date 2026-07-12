document.addEventListener("DOMContentLoaded", function () {
  const dropdownContainer = document.getElementById("optionsDropdown");
  const dropdownBtn = document.getElementById("dropdownBtn");
  const dropdownMenu = document.getElementById("dropdownMenu");
  const readLaterLink = document.getElementById("readLaterLink");
  const editLink = document.getElementById("editLink");
  const deleteLink = document.getElementById("deleteLink");

  const postAuthorId = dropdownContainer.getAttribute("data-author-id");
  const currentAuthorId = localStorage.getItem("author_id");

  if (currentAuthorId && postAuthorId === currentAuthorId) {
    editLink.style.display = "block";
    deleteLink.style.display = "block";
  } else {
    editLink.style.display = "none";
    deleteLink.style.display = "none";
  }

  dropdownBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    dropdownMenu.classList.toggle("show");
  });

  window.addEventListener("click", function () {
    if (dropdownMenu.classList.contains("show")) {
      dropdownMenu.classList.remove("show");
    }
  });

  readLaterLink.addEventListener("click", function (e) {
    e.preventDefault();
    alert("Added to Read Later!");
  });
});
