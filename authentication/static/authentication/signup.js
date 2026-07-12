// register
document
  .getElementById("signup-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();

    const firstName = document.getElementById("id_first_name").value.trim();
    const lastName = document.getElementById("id_last_name").value.trim();
    const email = document.getElementById("id_email").value.trim();
    const password = document.getElementById("id_password").value.trim();

    if (!firstName || !lastName || !email || !password) {
      Swal.fire({
        icon: "error",
        title: "Input Error",
        text: "Please fill in all the required fields.",
        confirmButtonColor: "#d33",
      });
      return;
    }

    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]",
    ).value;

    const formData = {
      first_name: firstName,
      last_name: lastName,
      email: email,
      password: password,
    };

    try {
      Swal.showLoading();

      const response = await fetch(REGISTER_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        Swal.fire({
          icon: "success",
          title: "Success",
          text: "Your account has been created successfully.",
          timer: 3000,
          showConfirmButton: true,
          confirmButtonText: "Go to Login",
          confirmButtonColor: "#211f1c",
        }).then((result) => {
          window.location.href = "/auth/signin";
        });
      } else {
        Swal.fire({
          icon: "error",
          title: "Registration Failed",
          text:
            data.error ||
            "Something went wrong during registration. Please try again later.",
          confirmButtonColor: "#d33",
        });
      }
    } catch (error) {
      // Handling network errors or server crashes
      console.error("Error:", error);
      Swal.fire({
        icon: "error",
        title: "Connection Error",
        text: "Could not connect to the server. Please check your internet connection.",
        confirmButtonColor: "#d33",
      });
    }
  });
