$(function(){

/* Creando alerta para el botón de LOGIN no habilitado */

    $(".log-in").click(function() {
    alert('Oops! LogIn not available');
    })

/* Ocultando secciones de registro y solo mostrar el splash con la vista de inicio*/

    $("#lyft-access").hide();
    $("#register").hide();

  setTimeout(function() {
    $("#splash").fadeOut(500);
    $("#lyft-access").show();
    }, 1000); 

/* Añadiendo función al boton SignUp */

    $(".sign-up").click(function() {
    $('#lyft-access').hide();
    $('#register').show();
    })

/* Añadiendo función al botón de regreso*/    

    $(".previous-btn").click(function() {
    $("#lyft-access").show();
    $("#register").hide();
    })

    $(".next-btn").click(function() {
    $('#verify').show();
    $('#register').hide();

    getCode();

    })

    /* Función para generar código y re-enviarlo al dar click el botón*/

    function getCode() {
    var code = Math.floor((Math.random() * 108) + 808);
    document.getElementById("input-code").innerHTML = code;
    alert('Your code LAB - ' + code);
    }

    $('#resend-code').click(getCode);
  

   
});