document.getElementById("login-form").addEventListener("submit", async function (e) {
        e.preventDefault();

        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const errorMsg = document.getElementById("error-msg");
        errorMsg.classList.add("hidden"); // ocultar mensaje anterior
        const formData = new URLSearchParams();
        formData.append("username", username);
        formData.append("password", password);

        try {
          const response = await fetch(`https://gestor-de-tareas-r39h.onrender.com/users/login`, {
            method: "POST",
            headers: {
              "Content-Type": "application/x-www-form-urlencoded"
            },
            body: formData
            
          });
            if (!response.ok) {
                const err = await response.json();
                errorMsg.textContent = err.detail || "Error al iniciar sesión: " + err.message;
                errorMsg.classList.remove("hidden");
                return;
            }
          const data = await response.json();
          localStorage.setItem("access_token", data.access_token);
          const token = localStorage.getItem("access_token");
          console.log("Token de acceso:", token);
          window.location.href = "tasks_main.html"; // Redirigir a la página principal
        } catch (error) {
            errorMsg.textContent = error.detail || "Error al iniciar sesión: " + error.message;
            errorMsg.classList.remove("hidden");
      }
    });