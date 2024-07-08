window.onload = function() {
    var usuario = localStorage.getItem("usuario");
    if (usuario) {
        document.getElementById("mensaje-bienvenida").textContent = "¡Hola, " + usuario + "!";
    }
}

document.getElementById("mensaje-bienvenida").addEventListener("click", function(event) {
    event.preventDefault(); // Evitar la acción predeterminada del enlace
    
    var usuario = localStorage.getItem("usuario");
    if (usuario) {
        var confirmacion = confirm("Se cerrara la sesión " + usuario + ", ¿esta seguro?");
        if (confirmacion) {
            localStorage.removeItem("usuario"); // Eliminar el usuario de localStorage
            window.location.href = "login.html"; // Redirigir a "login.html"
        }
    } else {
        // Si no hay usuario almacenado, redirigir a "login.html" directamente
        window.location.href = "login.html";
    }
});