// login
document
  .getElementById("signin-form")
  .addEventListener("submit", async function (e) {
    // Prevent the default form submission (page reload)
    e.preventDefault();

    // 1. Get input values
    const email = document.getElementById("id_email").value.trim();
    const password = document.getElementById("id_password").value.trim();

    // 2. Frontend Validation
    if (!email || !password) {
      Swal.fire({
        icon: "error",
        title: "Input Error",
        text: "Please fill in all the required fields.",
        confirmButtonColor: "#7a6f64",
      });
      return; // Stop execution
    }

    // Get Django CSRF token from the form
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]",
    ).value;

    // Prepare data payload
    const formData = {
      email: email,
      password: password,
    };

    try {
      // Show loading indicator
      Swal.showLoading();

      // 3. Send API Request to backend login endpoint
      const response = await fetch("/api/users/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      // 4. Handle Backend Response
      if (response.ok) {
        // Success: Save tokens to localStorage (or cookies) to use them in future requests
        localStorage.setItem("author_id", data.author_id);
        localStorage.setItem("token", data.access);

        Swal.fire({
          icon: "success",
          title: "Welcome Back!",
          text: "Logged in successfully.",
          timer: 2000,
          showConfirmButton: false,
        }).then(() => {
          // Redirect to your homepage or dashboard after success
          window.location.href = "/";
        });
      } else {
        // Error from backend (e.g., Invalid credentials or missing fields)
        Swal.fire({
          icon: "error",
          title: "Login Failed",
          text: data.error || "Invalid email or password. Please try again.",
          confirmButtonColor: "#d33",
        });
      }
    } catch (error) {
      // Handle network or server errors
      console.error("Error:", error);
      Swal.fire({
        icon: "error",
        title: "Connection Error",
        text: "Could not connect to the server. Please check your internet connection.",
        confirmButtonColor: "#d33",
      });
    }
  });
