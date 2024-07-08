function validarIngreso() {
    var user = document.getElementById('usuario').value;
    var pass = document.getElementById('password').value;
    
    var jsonFile = new XMLHttpRequest();
    jsonFile.open("GET", "cuentas.json", true);
    jsonFile.onreadystatechange = function () {
            // Parseamos el JSON
            var data = JSON.parse(jsonFile.responseText);
            var cuentas = data.cuentas;
            
            // Verificamos si el usuario y la contraseña ingresados coinciden con algún usuario del JSON
            var usuarioValido = cuentas.find(function (cuenta) {
                return cuenta.usuario === user && cuenta.password === pass;
            });

            // Mostramos un mensaje de acuerdo al resultado
            if (usuarioValido) {
                alert("¡Bienvenido! Redirigiendo a página principal");
                localStorage.setItem("usuario", user);
                window.location.href = "index.html";
                
            } else {
                alert("Usuario o contraseña incorrectos. Por favor, intente nuevamente");
                window.location.href = "login.html";
            }
    };
    jsonFile.send();
}

document.getElementById("btn-ingresar").addEventListener("click",validarIngreso);

