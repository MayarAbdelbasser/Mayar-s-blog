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

  // delete post
  deleteLink.addEventListener("click", function (e) {
    e.preventDefault();

    const postSlug = slug.textContent;
    console.log(postSlug);

    Swal.fire({
      title: "Are you sure?",
      text: "You won't be able to revert this!",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      confirmButtonText: "Yes, delete it!",
    }).then((result) => {
      if (result.isConfirmed) {
        const token = localStorage.getItem("token");

        if (!token) {
          Swal.fire({
            title: "Error!",
            text: "You are not logged in. Please log in first.",
            icon: "error",
          });
          return;
        }

        fetch(`/api/posts/delete/${postSlug}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        })
          .then((response) => {
            if (response.status === 204) {
              Swal.fire({
                title: "Deleted!",
                text: "Your post has been deleted successfully.",
                icon: "success",
              }).then(() => {
                window.location.href = "/";
              });
            } else {
              return response.json().then((data) => {
                throw new Error(
                  data.detail || data.error || "Failed to delete post",
                );
              });
            }
          })
          .catch((error) => {
            Swal.fire({
              title: "Error!",
              text: error.message,
              icon: "error",
            });
          });
      }
    });
  });

  readLaterLink.addEventListener("click", function (e) {
    e.preventDefault();
    alert("Added to Read Later!");
  });
});
