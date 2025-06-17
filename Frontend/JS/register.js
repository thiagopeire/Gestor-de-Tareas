document.getElementById("registro-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const data = {
        id: null,
        name: document.getElementById("first-name").value,
        lastname: document.getElementById("last-name").value,
        birthdate: document.getElementById("birthdate").value,
        username: document.getElementById("username").value,
        email: document.getElementById("email").value,
        password: document.getElementById("password").value,
        disabled: false
        };

    try {
        const response = await fetch("https://gestor-de-tareas-r39h.onrender.com/users/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
            });
        if (!response.ok) {
            const err = await response.json();
            document.getElementById("error-msg").textContent = err.detail || "Error al registrar usuario: " + err.message;
            document.getElementById("error-msg").classList.remove("hidden");
            return;
        }

        document.getElementById("success-msg").textContent = "Usuario registrado con éxito. Puedes iniciar sesión ahora.";
        document.getElementById("success-msg").classList.remove("hidden");
    } catch (err) {
        document.getElementById("error-msg").textContent = err.detail || "Error al registrar usuario: " + err.message;
        document.getElementById("error-msg").classList.remove("hidden");
        }
    }
);