const formulario = document.getElementById('form-venta');
const inputs = document.querySelectorAll('#form-venta input');
var errorFormulario = 0;
var camposToCheck = ['Nombre','Marca','Apellido','Modelo','Email','Telefono','Version','Domicilio','Kilometros'];

const expresiones = {
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
        version: /^[a-zA-ZÀ-ÿ0-9_.+-\s]{1,50}$/,
	modelo:/^[a-zA-Z0-9\s]{1,40}$/,
        correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	telefono: /^\d{7,14}$/, // 7 a 14 numeros.
        kilometros: /^\d{1,7}$/ // 1 a 7 numeros.
}

const validarFormulario = (e) => {
    switch(e.target.name){
        case "Nombre":
                validarCampo(expresiones.nombre, e.target, 'Nombre');
        break;
        case "Marca":
                validarCampo(expresiones.modelo, e.target, 'Marca');
        break;
        case "Apellido":
                validarCampo(expresiones.nombre, e.target, 'Apellido');
        break;
        case "Modelo":
                validarCampo(expresiones.modelo, e.target, 'Modelo');
        break;
        case "Email":
                validarCampo(expresiones.correo, e.target, 'Email');
        break;
        case "Telefono":
                validarCampo(expresiones.telefono, e.target, 'Telefono');
        break; 
        case "Version":
                validarCampo(expresiones.version, e.target, 'Version');
        break;    
        case "Domicilio":
                validarCampo(expresiones.modelo, e.target, 'Domicilio');
        break;    
        case "Kilometros":
                validarCampo(expresiones.kilometros, e.target, 'Kilometros');
        break;    
    }

}

inputs.forEach((input) => {
	input.addEventListener('keyup', validarFormulario);
	input.addEventListener('blur', validarFormulario);
});

const validarCampo = (expresion,input,campo) => {
if(expresion.test(input.value)){
        document.getElementById(`Icono-${campo}`).classList.add('fas');
        document.getElementById(`Icono-${campo}`).classList.add('fa-check-circle');
        document.getElementById(`Icono-${campo}`).classList.add('green');
        document.getElementById(`Icono-${campo}`).classList.remove('fa-times-circle');
        document.getElementById(`Icono-${campo}`).classList.remove('red');
}
else {
        document.getElementById(`Icono-${campo}`).classList.add('fas');
        document.getElementById(`Icono-${campo}`).classList.remove('fa-check-circle');
        document.getElementById(`Icono-${campo}`).classList.remove('green');
        document.getElementById(`Icono-${campo}`).classList.add('fa-times-circle');
        document.getElementById(`Icono-${campo}`).classList.add('red');
}
}

const erroresFormulario = () => {
        camposToCheck.forEach((campo) => {
                // Obtener el elemento por su ID
                var elemento = document.getElementById(`Icono-${campo}`);
                
                // Verificar si el elemento existe y si su clase NO contiene "green"
                if (elemento && !elemento.classList.value.includes("green")) {
                    // Incrementar el contador de errores
                    errorFormulario++;
                }
            });

        if(document.getElementById('checkbox').checked==false) {
                alert('Para continuar debe aceptar que un vendedor se comunique con usted')
        }
        else {
        if(errorFormulario==0) {
                alert('Formulario enviado correctamente!')
                window.location.href = "index.html";
        }
        else {
                alert('Alguno de los campos es incorrecto o esta incompleto. Por favor volver a verificar!')
        }
}
}

document.getElementById("btn-solicitar-cotizacion").addEventListener("click",erroresFormulario);