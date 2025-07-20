// script.js

document.addEventListener("DOMContentLoaded", () => {
    // Seleccionar elementos del DOM
    const form = document.querySelector("form");
    const emailInput = document.querySelector("input[name='email']");
    const passwordInput = document.querySelector("input[name='password']");
    const socialIcons = document.querySelectorAll(".social-icons a");

    // Validación básica del formulario
    form.addEventListener("submit", (event) => {
        let isValid = true;
        let errorMessage = "";

        // Validar correo electrónico
        if (!validateEmail(emailInput.value)) {
            isValid = false;
            errorMessage += "Por favor, introduce un correo electrónico válido.\n";
        }

        // Validar contraseña
        if (passwordInput.value.trim().length < 6) {
            isValid = false;
            errorMessage += "La contraseña debe tener al menos 6 caracteres.\n";
        }

        // Mostrar mensaje de error y prevenir envío si no es válido
        if (!isValid) {
            alert(errorMessage);
            event.preventDefault();
        }
    });

    // Efecto hover para redes sociales
    socialIcons.forEach(icon => {
        icon.addEventListener("mouseenter", () => {
            icon.style.color = "#3498db"; // Cambiar el color al pasar el ratón
        });

        icon.addEventListener("mouseleave", () => {
            icon.style.color = ""; // Restaurar el color original
        });
    });

    // Función para validar un correo electrónico
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Opcional: Agregar funcionalidad para alternar visibilidad de contraseña
    const togglePassword = document.createElement("span");
    togglePassword.textContent = "Mostrar contraseña";
    togglePassword.style.cursor = "pointer";
    togglePassword.style.marginLeft = "10px";
    
    passwordInput.parentNode.appendChild(togglePassword);

    togglePassword.addEventListener("click", () => {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            togglePassword.textContent = "Ocultar contraseña";
        } else {
            passwordInput.type = "password";
            togglePassword.textContent = "Mostrar contraseña";
        }
    });
});