document.addEventListener("DOMContentLoaded", function () {
  const authBtn = document.getElementById("auth-btn");

  if (authBtn) {
    authBtn.addEventListener("click", async function () {
      const buttonText = authBtn.textContent.trim();

      if (buttonText === "Logout") {
        const logoutUrl = authBtn.getAttribute("data-logout-url");

        try {
          const result = await Swal.fire({
            title: "Are you sure?",
            text: "You will be logged out of your account!",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            confirmButtonText: "Yes, log me out",
            cancelButtonText: "Cancel",
          });

          if (result.isConfirmed) {
            localStorage.removeItem("author_id");
            localStorage.removeItem("token");
            localStorage.removeItem("author_first_name");
            localStorage.removeItem("author_last_name");
            window.location.href = logoutUrl;
          }
        } catch (err) {
          console.error("Alert closed unexpectedly", err);
        }
      } else if (buttonText === "Login") {
        const loginUrl = authBtn.getAttribute("data-login-url");
        window.location.href = loginUrl;
      }
    });
  }
});
