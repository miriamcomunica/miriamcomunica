import flet as ft
import webbrowser
import json
import re
import unicodedata
from urllib.parse import quote
from urllib.request import urlopen

TIKTOK_URL = "https://www.tiktok.com/@miriam.comunica"
INSTAGRAM_URL = "https://www.instagram.com/miriam.comunica/"
WEB_URL = "https://miriamcomunica.com"
WHATSAPP_CLASSES_URL = "https://wa.me/34611090017"

AMETHYST = "#B174E7"
SOFT_AMETHYST = "#E8D8F8"
PALE_AMETHYST = "#F6F0FC"
TITLE_FONT = "Playfair Display"
BODY_FONT = "Garamond"
RED = AMETHYST
YELLOW = "#FFFFFF"
DARK_RED = "#7F4DB1"
SOFT_YELLOW = SOFT_AMETHYST
CREAM = PALE_AMETHYST
TEXT_DARK = "#40235C"
TEXT_MUTED = "#6B4A8A"

SURVIVAL_SECTIONS = {
    "administrativa": {
        "title": '1. El "Kit de Supervivencia" Administrativa',
        "body": (
            "España tiene una burocracia particular. Facilitar esto le quitará un peso enorme de encima.\n\n"
            "Guía del NIE/TIE:\n"
            "Un checklist paso a paso de qué documentos necesita, cómo pedir la cita previa y cómo pagar las tasas del Modelo 790.\n\n"
            "Empadronamiento:\n"
            "Explicación sencilla de qué es y por qué lo necesita para ir al médico o escolarizar a los niños.\n\n"
            "Seguridad Social:\n"
            "Cómo obtener el número de afiliación para empezar a trabajar."
        ),
    },
    "comunicacion": {
        "title": "2. Comunicación en Tiempo Real",
        "body": (
            "No basta con un traductor general, necesita soluciones para situaciones especificas.\n\n"
            'Traductor de voz con "Modo Médico":\n'
            "Frases hechas para urgencias, cuando los nervios bloquean el idioma.\n\n"
            "Escáner de documentos:\n"
            "Usar la camara para traducir cartas oficiales, facturas de luz o contratos de alquiler al instante.\n\n"
            'Diccionario de "Jerga Española":\n'
            'Explicar qué es "ir de tapeo", qué significa que algo está "guay" o la diferencia entre "ahora" y "ahora mismo".'
        ),
    },
    "integracion": {
        "title": "3. Integracion y Vida Diaria",
        "body": (
            "Mapa de servicios publicos:\n"
            "Ubicacion de centros de salud, comisarias, bibliotecas y oficinas de correos.\n\n"
            "Transporte:\n"
            "Tutoriales de cómo comprar bonos de metro o autobús en las principales ciudades.\n\n"
            "Emergencias:\n"
            "Un botón de pánico que llame al 112 y muestre en pantalla la dirección exacta del usuario en español para leerla al operador."
        ),
    },
    "comunidad": {
        "title": "4. Comunidad y Apoyo",
        "body": (
            'Foro de "Recién Llegados":\n'
            'Un espacio para preguntar cosas como "¿dónde compro este producto de mi país?" o "¿qué compañía de internet es mejor?".\n\n'
            "Intercambio de idiomas local:\n"
            "Conectar con personas locales que quieran aprender su idioma y le ayuden con el español a cambio de un café."
        ),
    },
}

ADMIN_SECTIONS = {
    "nie_tie": {
        "title": "NIE / TIE",
        "body": (
            "Checklist paso a paso de los documentos que necesitas.\n\n"
            "Cómo pedir la cita previa.\n\n"
            "Cómo pagar las tasas del Modelo 790."
        ),
    },
    "empadronamiento": {
        "title": "EMPADRONAMIENTO",
        "body": (
            "Explicación sencilla de qué es el empadronamiento.\n\n"
            "Por qué lo necesitas para ir al médico.\n\n"
            "Por qué es importante para escolarizar a los niños."
        ),
    },
    "seguridad_social": {
        "title": "SEGURIDAD SOCIAL",
        "body": (
            "Cómo obtener el número de afiliación.\n\n"
            "Qué necesitas para empezar a trabajar.\n\n"
            "Pasos básicos para tener tu situación en regla."
        ),
    },
}

COMMUNICATION_SECTIONS = {
    "modo_medico": {
        "title": "TRADUCTOR DE VOZ MODO MÉDICO",
        "body": (
            "Frases utiles para urgencias.\n\n"
            "Ayuda para explicar síntomas cuando los nervios bloquean el idioma.\n\n"
            "Apoyo rápido para consultas médicas."
        ),
    },
    "escaner_documentos": {
        "title": "ESCÁNER DE DOCUMENTOS",
        "body": (
            "Usar la camara para traducir cartas oficiales.\n\n"
            "Lectura rapida de facturas de luz.\n\n"
            "Ayuda para entender contratos de alquiler."
        ),
    },
    "jerga_espanola": {
        "title": "JERGA ESPAÑOLA",
        "body": (
            'Explica expresiones como "ir de tapeo".\n\n'
            'Aclara qué significa que algo está "guay".\n\n'
            'Ayuda a entender la diferencia entre "ahora" y "ahora mismo".'
        ),
    },
}

INTEGRATION_SECTIONS = {
    "mapa_servicios": {
        "title": "MAPA DE SERVICIOS PÚBLICOS",
        "body": (
            "Ubicación de centros de salud.\n\n"
            "Información de comisarías, bibliotecas y oficinas de correos.\n\n"
            "Acceso rápido a servicios útiles del día a día."
        ),
    },
    "transporte": {
        "title": "TRANSPORTE",
        "body": (
            "Tutoriales para comprar bonos de metro.\n\n"
            "Ayuda para usar bonos de autobús.\n\n"
            "Información pensada para principales ciudades."
        ),
    },
    "emergencias": {
        "title": "EMERGENCIAS",
        "body": (
            "Botón de pánico para llamar al 112.\n\n"
            "Mostrar la dirección exacta del usuario en pantalla.\n\n"
            "Apoyo rápido para leer la ubicación al operador."
        ),
    },
}

COMMUNITY_SECTIONS = {
    "foro_recien_llegados": {
        "title": "FORO DE RECIÉN LLEGADOS",
        "body": (
            "Espacio para resolver dudas prácticas.\n\n"
            "Preguntas sobre productos de tu país.\n\n"
            "Ayuda para comparar compañías de internet u otros servicios."
        ),
    },
    "intercambio_idiomas": {
        "title": "INTERCAMBIO DE IDIOMAS",
        "body": (
            "Conectar con personas locales.\n\n"
            "Practicar español a cambio de ayudar con tu idioma.\n\n"
            "Una forma cercana de integrarte y crear comunidad."
        ),
    },
}

FAQ_SECTIONS = {
    "cita_nie": {
        "title": "¿CÓMO PIDO LA CITA DEL NIE?",
        "body": (
            "Normalmente se pide por internet en la sede correspondiente.\n\n"
            "Ten a mano tu pasaporte, tus datos personales y el tramite exacto.\n\n"
            "Revisa bien la provincia antes de confirmar."
        ),
    },
    "empadronamiento_para_que": {
        "title": "¿PARA QUÉ SIRVE EL EMPADRONAMIENTO?",
        "body": (
            "Sirve para acreditar donde vives.\n\n"
            "Te lo pueden pedir para médico, colegio, ayudas o trámites.\n\n"
            "Es uno de los primeros pasos más importantes."
        ),
    },
    "numero_seguridad_social": {
        "title": "¿CÓMO CONSIGO EL NÚMERO DE SEGURIDAD SOCIAL?",
        "body": (
            "Puedes solicitarlo antes de empezar a trabajar.\n\n"
            "Te pediran identificacion y algunos datos personales.\n\n"
            "Es importante para contratos y altas laborales."
        ),
    },
    "llamar_112": {
        "title": "¿CUÁNDO TENGO QUE LLAMAR AL 112?",
        "body": (
            "Cuando haya una urgencia médica, policial o de bomberos.\n\n"
            "Habla despacio y explica que ocurre.\n\n"
            "Si puedes, di también tu dirección exacta."
        ),
    },
    "tarjeta_sanitaria": {
        "title": "¿CÓMO PIDO LA TARJETA SANITARIA?",
        "body": (
            "Depende de la comunidad autonoma, pero suele pedir empadronamiento y documentacion.\n\n"
            "Consulta tu centro de salud o la web oficial de sanidad.\n\n"
            "Conviene empezar este tramite cuanto antes."
        ),
    },
    "bono_transporte": {
        "title": "¿QUÉ BONO DE TRANSPORTE ME CONVIENE?",
        "body": (
            "Depende de la ciudad y de cuánto uses metro o autobús.\n\n"
            "Si viajas mucho, suele compensar un bono mensual o recargable.\n\n"
            "Pregunta también por descuentos especiales."
        ),
    },
}

SPANISH_SURVIVAL_SECTIONS = {
    "restaurante": {
        "title": "EN UN RESTAURANTE",
        "body": (
            "Hola, una mesa para una persona.\n\n"
            "Que me recomienda?\n\n"
            "La cuenta, por favor.\n\n"
            "No puedo comer gluten.\n\n"
            "Esta muy rico, gracias."
        ),
    },
    "hospital": {
        "title": "EN UN HOSPITAL",
        "body": (
            "Necesito ayuda, me encuentro mal.\n\n"
            "Me duele aqui.\n\n"
            "Tengo fiebre desde ayer.\n\n"
            "Soy alergica o alergico a este medicamento.\n\n"
            "Necesito un traductor, por favor."
        ),
    },
    "farmacia": {
        "title": "EN UNA FARMACIA",
        "body": (
            "Necesito algo para el dolor de cabeza.\n\n"
            "Tiene algo para la tos?\n\n"
            "Como se toma este medicamento?\n\n"
            "Necesito una crema para esta herida.\n\n"
            "Hace falta receta?"
        ),
    },
    "hotel": {
        "title": "EN UN HOTEL",
        "body": (
            "Tengo una reserva a nombre de...\n\n"
            "A que hora es el check-in?\n\n"
            "Necesito una habitacion tranquila.\n\n"
            "No funciona el aire acondicionado.\n\n"
            "Puede llamar un taxi, por favor?"
        ),
    },
    "transporte": {
        "title": "EN EL TRANSPORTE",
        "body": (
            "¿Este autobús va al centro?\n\n"
            "¿Dónde compro el billete?\n\n"
            "¿En qué parada tengo que bajar?\n\n"
            "¿Cuánto cuesta el bono?\n\n"
            "Gracias por su ayuda."
        ),
    },
    "supermercado": {
        "title": "EN UN SUPERMERCADO",
        "body": (
            "Donde esta la leche?\n\n"
            "Aceptan tarjeta?\n\n"
            "Cuanto cuesta esto?\n\n"
            "Tiene bolsa?\n\n"
            "Quiero pagar, por favor."
        ),
    },
    "tienda_ropa": {
        "title": "EN UNA TIENDA DE ROPA",
        "body": (
            "Tiene esta talla?\n\n"
            "Puedo probarmelo?\n\n"
            "Tiene otro color?\n\n"
            "Cuanto vale?\n\n"
            "Me lo llevo."
        ),
    },
    "taxi": {
        "title": "EN UN TAXI",
        "body": (
            "Lleveme a esta direccion, por favor.\n\n"
            "Cuanto tarda mas o menos?\n\n"
            "Puede parar aqui?\n\n"
            "Acepta tarjeta?\n\n"
            "Gracias, buen dia."
        ),
    },
    "comisaria": {
        "title": "EN UNA COMISARIA",
        "body": (
            "Necesito ayuda.\n\n"
            "Quiero poner una denuncia.\n\n"
            "He perdido mi documentacion.\n\n"
            "No hablo bien español.\n\n"
            "¿Puede hablar más despacio, por favor?"
        ),
    },
    "colegio": {
        "title": "EN UN COLEGIO",
        "body": (
            "Quiero informacion para matricular a mi hijo o hija.\n\n"
            "Que documentos necesito?\n\n"
            "A que hora empieza la clase?\n\n"
            "Donde esta la secretaria?\n\n"
            "Gracias por su ayuda."
        ),
    },
    "trabajo": {
        "title": "EN EL TRABAJO",
        "body": (
            "No entiendo esta tarea.\n\n"
            "Puede explicarmelo otra vez?\n\n"
            "A que hora empieza el turno?\n\n"
            "Necesito hablar con recursos humanos.\n\n"
            "Estoy aprendiendo espanol."
        ),
    },
    "banco": {
        "title": "EN UN BANCO",
        "body": (
            "Quiero abrir una cuenta.\n\n"
            "Que documentos necesito?\n\n"
            "Quiero sacar dinero.\n\n"
            "Tengo un problema con mi tarjeta.\n\n"
            "Puede ayudarme, por favor?"
        ),
    },
    "ayuntamiento": {
        "title": "EN EL AYUNTAMIENTO",
        "body": (
            "Quiero pedir informacion sobre este tramite.\n\n"
            "Necesito una cita previa?\n\n"
            "Que documentos tengo que traer?\n\n"
            "Puede explicarmelo mas despacio, por favor?\n\n"
            "Donde esta la oficina correcta?"
        ),
    },
    "extranjeria": {
        "title": "EN EXTRANJERIA",
        "body": (
            "Tengo cita para este tramite.\n\n"
            "Vengo por el NIE o la TIE.\n\n"
            "Me falta algun documento?\n\n"
            "Donde pago la tasa?\n\n"
            "Cuando puedo volver a recogerlo?"
        ),
    },
    "casero": {
        "title": "CON EL CASERO",
        "body": (
            "Estoy interesada o interesado en alquilar esta vivienda.\n\n"
            "Que incluye el precio?\n\n"
            "Puedo empadronarme aqui?\n\n"
            "Cuando se paga la fianza?\n\n"
            "Necesito una copia del contrato."
        ),
    },
    "centro_salud": {
        "title": "EN EL CENTRO DE SALUD",
        "body": (
            "Quiero pedir una cita medica.\n\n"
            "Me encuentro mal desde ayer.\n\n"
            "No hablo bien espanol.\n\n"
            "Donde tengo que esperar?\n\n"
            "Necesito una receta, por favor."
        ),
    },
    "correos": {
        "title": "EN CORREOS",
        "body": (
            "Quiero enviar este paquete.\n\n"
            "Cuanto cuesta?\n\n"
            "Cuando llegara?\n\n"
            "Necesito un sobre grande.\n\n"
            "Donde recojo una carta certificada?"
        ),
    },
    "movil": {
        "title": "EN UNA TIENDA DE MOVIL",
        "body": (
            "Quiero una tarjeta SIM.\n\n"
            "Necesito internet en el móvil.\n\n"
            "¿Cuánto cuesta este plan?\n\n"
            "Necesito ayuda para activar la línea.\n\n"
            "¿Puedo recargar aquí?"
        ),
    },
    "locutorio": {
        "title": "EN UN LOCUTORIO",
        "body": (
            "Quiero imprimir este documento.\n\n"
            "Necesito hacer una fotocopia.\n\n"
            "Puedo escanear esto?\n\n"
            "Cuanto cuesta enviar este correo?\n\n"
            "Tienen ordenadores para usar internet?"
        ),
    },
    "piso_compartido": {
        "title": "EN UN PISO COMPARTIDO",
        "body": (
            "Estoy buscando una habitación.\n\n"
            "¿Los gastos están incluidos?\n\n"
            "¿Puedo empadronarme aquí?\n\n"
            "Hay contrato?\n\n"
            "¿Cuándo podría entrar a vivir?"
        ),
    },
    "vecindario": {
        "title": "CON VECINOS O EN EL BARRIO",
        "body": (
            "Hola, acabo de mudarme.\n\n"
            "¿Sabe dónde está el centro de salud?\n\n"
            "¿A qué hora pasa el autobús?\n\n"
            "¿Dónde está el supermercado más cercano?\n\n"
            "Muchas gracias por su ayuda."
        ),
    },
}

SPANISH_SURVIVAL_DETAILS = {
    "restaurante": {
        "pedir_mesa": {
            "title": "PEDIR MESA",
            "body": "Hola, una mesa para dos, por favor.\n\nTenemos reserva a nombre de...\n\nPodemos sentarnos aqui?",
        },
        "pedir_comida": {
            "title": "PEDIR COMIDA",
            "body": "Que me recomienda?\n\nQuiero esto, por favor.\n\nSin gluten, por favor.",
        },
        "pedir_cuenta": {
            "title": "PEDIR LA CUENTA",
            "body": "La cuenta, por favor.\n\nPuedo pagar con tarjeta?\n\nMuchas gracias, estaba todo muy bueno.",
        },
        "alergias": {
            "title": "ALERGIAS o INTOLERANCIAS",
            "body": "Soy alergica o alergico a...\n\nEsto lleva leche o frutos secos?\n\nNecesito comida sin gluten.",
        },
        "reserva": {
            "title": "RESERVA",
            "body": "Quiero hacer una reserva.\n\nPara cuantas personas?\n\nA que hora tienen mesa libre?",
        },
        "menu": {
            "title": "MENU DEL DIA",
            "body": "Tienen menu del dia?\n\nQue incluye?\n\nHay opcion vegetariana?",
        },
        "comportamiento": {
            "title": "COMPORTAMIENTO y COSTUMBRES",
            "body": "Observa primero si se pide en mesa o en barra.\n\nPedir con por favor y dar las gracias se valora mucho.\n\nLa propina no siempre es obligatoria; si se deja, suele ser pequeña.",
        },
        "para_llevar": {
            "title": "PARA LLEVAR",
            "body": "Lo quiero para llevar.\n\nPuede ponerlo separado?\n\nNecesito cubiertos, por favor.",
        },
    },
    "hospital": {
        "urgencias": {
            "title": "EN URGENCIAS",
            "body": "Necesito ayuda, me encuentro muy mal.\n\nMe duele aqui.\n\nTengo fiebre desde ayer.",
        },
        "medicacion": {
            "title": "MEDICACION",
            "body": "Soy alergica o alergico a este medicamento.\n\nTomo esta medicacion.\n\nComo tengo que tomarlo?",
        },
        "idioma": {
            "title": "PROBLEMAS CON EL IDIOMA",
            "body": "No hablo bien espanol.\n\nPuede hablar mas despacio?\n\nNecesito un traductor, por favor.",
        },
        "cita": {
            "title": "CITA o ADMISION",
            "body": "Tengo cita para hoy.\n\nDonde tengo que ir?\n\nQue documento necesita?",
        },
        "acompanante": {
            "title": "ACOMPANANTE",
            "body": "Puede pasar conmigo?\n\nNecesito ayuda para entender.\n\nPuede esperar aqui, por favor?",
        },
    },
    "farmacia": {
        "dolor": {
            "title": "DOLOR Y FIEBRE",
            "body": "Necesito algo para el dolor.\n\nTiene algo para la fiebre?\n\nComo se toma este medicamento?",
        },
        "tos_resfriado": {
            "title": "TOS Y RESFRIADO",
            "body": "Tiene algo para la tos?\n\nEstoy resfriada o resfriado.\n\nNecesito algo para la garganta.",
        },
        "receta": {
            "title": "RECETA",
            "body": "Hace falta receta?\n\nTengo una receta del medico.\n\nPuede explicarme como usarlo?",
        },
        "piel": {
            "title": "PIEL o HERIDAS",
            "body": "Necesito una crema para esta herida.\n\nTiene algo para una quemadura?\n\nEsto pica mucho.",
        },
        "ninos": {
            "title": "MEDICINAS PARA NINOS",
            "body": "Es para un nino o una nina.\n\nCuanta cantidad tengo que darle?\n\nTiene jarabe infantil?",
        },
    },
    "hotel": {
        "checkin": {
            "title": "CHECK-IN",
            "body": "Tengo una reserva a nombre de...\n\nA que hora es el check-in?\n\nNecesito mi pasaporte?",
        },
        "habitacion": {
            "title": "PROBLEMAS EN LA HABITACION",
            "body": "No funciona el aire acondicionado.\n\nNecesito toallas limpias.\n\nLa habitacion no esta lista.",
        },
        "servicios": {
            "title": "SERVICIOS",
            "body": "Puede llamar un taxi?\n\nA que hora es el desayuno?\n\nHay wifi gratis?",
        },
        "checkout": {
            "title": "CHECK-OUT",
            "body": "A que hora tengo que dejar la habitacion?\n\nPuedo salir mas tarde?\n\nDonde dejo la llave?",
        },
        "pago": {
            "title": "PAGO",
            "body": "Quiero pagar ahora.\n\nMe da la factura, por favor?\n\nAceptan tarjeta?",
        },
    },
    "transporte": {
        "billete": {
            "title": "BILLETES",
            "body": "Donde compro el billete?\n\nCuanto cuesta?\n\nAceptan tarjeta?",
        },
        "ruta": {
            "title": "RUTA",
            "body": "Este autobus va al centro?\n\nEn que parada bajo?\n\nTengo que hacer transbordo?",
        },
        "bono": {
            "title": "BONOS",
            "body": "Que bono me conviene?\n\nCuanto cuesta el bono mensual?\n\nDonde puedo recargarlo?",
        },
        "andenes": {
            "title": "ANDENES Y PARADAS",
            "body": "De que anden sale?\n\nEsta es la parada correcta?\n\nCuanto falta para que llegue?",
        },
        "incidencias": {
            "title": "INCIDENCIAS",
            "body": "Hay retraso?\n\nEste tren no circula hoy?\n\nQue alternativa tengo?",
        },
    },
    "ayuntamiento": {
        "informacion": {
            "title": "PEDIR INFORMACION",
            "body": "Quiero informacion sobre este tramite.\n\nNecesito cita previa?\n\nDonde esta la oficina correcta?",
        },
        "documentos": {
            "title": "DOCUMENTOS",
            "body": "Que documentos tengo que traer?\n\nMe falta algo?\n\nNecesito una copia de este formulario.",
        },
        "padron": {
            "title": "PADRON",
            "body": "Quiero empadronarme.\n\nNecesito cita para el padron?\n\nCuanto tarda este tramite?",
        },
        "certificados": {
            "title": "CERTIFICADOS",
            "body": "Necesito un certificado.\n\nDonde lo solicito?\n\nCuando puedo recogerlo?",
        },
        "tasas": {
            "title": "TASAS MUNICIPALES",
            "body": "Donde pago esta tasa?\n\nPuedo pagar con tarjeta?\n\nNecesito justificante?",
        },
    },
    "extranjeria": {
        "nie_tie": {
            "title": "NIE Y TIE",
            "body": "Vengo por el NIE o la TIE.\n\nTengo cita para este tramite.\n\nMe falta algun documento?",
        },
        "tasas": {
            "title": "TASAS",
            "body": "Donde pago la tasa?\n\nQue modelo tengo que pagar?\n\nTengo que traer el justificante impreso?",
        },
        "recogida": {
            "title": "RECOGIDA",
            "body": "Cuando puedo volver a recogerlo?\n\nNecesito otra cita?\n\nQue tengo que traer ese dia?",
        },
        "huellas": {
            "title": "HUELLAS",
            "body": "Vengo para poner las huellas.\n\nTengo cita para hoy.\n\nNecesito foto o formulario?",
        },
        "resguardo": {
            "title": "RESGUARDO",
            "body": "Necesito un resguardo.\n\nEste documento sirve mientras espero?\n\nMe lo puede sellar, por favor?",
        },
    },
    "casero": {
        "alquiler": {
            "title": "ALQUILER",
            "body": "Estoy interesada o interesado en alquilar esta vivienda.\n\nQue incluye el precio?\n\nCuanto es la fianza?",
        },
        "contrato": {
            "title": "CONTRATO",
            "body": "Necesito una copia del contrato.\n\nCuanto dura el contrato?\n\nCuando se paga cada mes?",
        },
        "padron": {
            "title": "EMPADRONAMIENTO",
            "body": "Puedo empadronarme aqui?\n\nNecesito una autorizacion suya?\n\nMe puede firmar este documento?",
        },
        "averias": {
            "title": "AVERIAS",
            "body": "No funciona la calefaccion.\n\nHay una fuga de agua.\n\nPuede venir alguien a arreglarlo?",
        },
        "facturas": {
            "title": "FACTURAS Y GASTOS",
            "body": "Quien paga la luz y el agua?\n\nInternet esta incluido?\n\nCuando llegan las facturas?",
        },
    },
    "centro_salud": {
        "cita": {
            "title": "PEDIR CITA",
            "body": "Quiero pedir una cita medica.\n\nEs urgente?\n\nPara cuando hay cita disponible?",
        },
        "consulta": {
            "title": "EN CONSULTA",
            "body": "Me encuentro mal desde ayer.\n\nMe duele aqui.\n\nNecesito una receta, por favor.",
        },
        "idioma": {
            "title": "IDIOMA",
            "body": "No hablo bien espanol.\n\nPuede hablar mas despacio?\n\nPuede escribirlo, por favor?",
        },
        "tarjeta": {
            "title": "TARJETA SANITARIA",
            "body": "Quiero informacion sobre la tarjeta sanitaria.\n\nQue documentos necesito?\n\nDonde hago este tramite?",
        },
        "especialista": {
            "title": "ESPECIALISTA",
            "body": "Necesito cita con un especialista.\n\nMe pueden derivar?\n\nCuando recibire la cita?",
        },
    },
    "correos": {
        "enviar_paquete": {
            "title": "ENVIAR UN PAQUETE",
            "body": "Quiero enviar este paquete.\n\nCuanto cuesta?\n\nCuando llegara?",
        },
        "carta_certificada": {
            "title": "CARTA CERTIFICADA",
            "body": "Quiero enviar una carta certificada.\n\nNecesito un sobre grande.\n\nMe da el justificante, por favor?",
        },
        "recoger_envio": {
            "title": "RECOGER UN ENVIO",
            "body": "Vengo a recoger este envio.\n\nTengo este aviso.\n\nNecesito enseñar el pasaporte?",
        },
        "sobres_cajas": {
            "title": "SOBRES Y CAJAS",
            "body": "Necesito una caja mediana.\n\nTiene sobres acolchados?\n\nCual me recomienda para esto?",
        },
        "seguimiento": {
            "title": "SEGUIMIENTO",
            "body": "Quiero saber donde esta mi paquete.\n\nEste es el numero de seguimiento.\n\nHa habido algun problema con la entrega?",
        },
        "devoluciones": {
            "title": "DEVOLUCIONES",
            "body": "Quiero devolver este paquete.\n\nNecesito imprimir una etiqueta?\n\nDonde lo dejo?",
        },
        "apartado_postal": {
            "title": "APARTADO POSTAL",
            "body": "Quiero informacion sobre un apartado postal.\n\nCuanto cuesta?\n\nQue documentos necesito?",
        },
        "sellos": {
            "title": "SELLOS",
            "body": "Necesito sellos.\n\nCuantos necesito para esta carta?\n\nSirven para envio internacional?",
        },
        "envio_internacional": {
            "title": "ENVIO INTERNACIONAL",
            "body": "Quiero enviar este paquete a otro pais.\n\nCuanto tarda?\n\nNecesito rellenar algun formulario?",
        },
    },
    "supermercado": {
        "buscar_producto": {
            "title": "BUSCAR PRODUCTOS",
            "body": "Donde esta la leche?\n\nDonde estan los huevos?\n\nTiene este producto sin gluten?",
        },
        "pago": {
            "title": "PAGAR",
            "body": "Quiero pagar, por favor.\n\nAceptan tarjeta?\n\nTiene bolsa?",
        },
        "precio": {
            "title": "PRECIO",
            "body": "Cuanto cuesta esto?\n\nHay oferta?\n\nEste precio es por kilo?",
        },
        "devoluciones": {
            "title": "DEVOLUCIONES",
            "body": "Quiero devolver este producto.\n\nTengo el ticket.\n\nMe devuelven el dinero o un vale?",
        },
        "ingredientes": {
            "title": "INGREDIENTES",
            "body": "Donde puedo ver los ingredientes?\n\nEsto lleva cerdo?\n\nEs apto para vegetarianos?",
        },
    },
    "tienda_ropa": {
        "talla": {
            "title": "TALLAS",
            "body": "Tiene esta talla?\n\nTiene una talla mas?\n\nEs demasiado grande para mi.",
        },
        "probador": {
            "title": "PROBADOR",
            "body": "Puedo probarmelo?\n\nDonde estan los probadores?\n\nMe queda bien?",
        },
        "compra": {
            "title": "COMPRA",
            "body": "Cuanto vale?\n\nTiene otro color?\n\nMe lo llevo.",
        },
        "cambios": {
            "title": "CAMBIOS Y DEVOLUCIONES",
            "body": "Puedo cambiarlo?\n\nCuantos dias tengo para devolverlo?\n\nNecesito el ticket?",
        },
        "rebajas": {
            "title": "REBAJAS",
            "body": "Esto esta rebajado?\n\nHay descuento hoy?\n\nEl precio final cual es?",
        },
    },
    "taxi": {
        "destino": {
            "title": "INDICAR DESTINO",
            "body": "Lleveme a esta direccion, por favor.\n\nEs aqui.\n\nPuede parar en esta calle?",
        },
        "tiempo": {
            "title": "TIEMPO Y RUTA",
            "body": "Cuanto tarda mas o menos?\n\nHay mucho trafico?\n\nPuede ir por la ruta mas rapida?",
        },
        "pago": {
            "title": "PAGO",
            "body": "Acepta tarjeta?\n\nCuanto es?\n\nGracias, buen dia.",
        },
        "equipaje": {
            "title": "EQUIPAJE",
            "body": "Llevo una maleta grande.\n\nPuede abrir el maletero?\n\nAyudeme con el equipaje, por favor.",
        },
        "recibo": {
            "title": "RECIBO",
            "body": "Me da un recibo, por favor?\n\nLo necesito para el trabajo.\n\nPuede poner la fecha?",
        },
    },
    "comisaria": {
        "denuncia": {
            "title": "DENUNCIA",
            "body": "Quiero poner una denuncia.\n\nHe perdido mi documentacion.\n\nMe han robado la cartera.",
        },
        "ayuda": {
            "title": "PEDIR AYUDA",
            "body": "Necesito ayuda.\n\nNo se que tengo que hacer.\n\nPuede explicarmelo mas despacio?",
        },
        "idioma": {
            "title": "IDIOMA",
            "body": "No hablo bien espanol.\n\nPuede hablar mas despacio?\n\nNecesito un traductor, por favor.",
        },
        "cita": {
            "title": "CITA PREVIA",
            "body": "Tengo cita previa.\n\nVengo para este tramite.\n\nDonde tengo que esperar?",
        },
        "documentacion": {
            "title": "DOCUMENTACION",
            "body": "He perdido mi pasaporte.\n\nNecesito un justificante.\n\nQue tengo que hacer ahora?",
        },
    },
    "colegio": {
        "matricula": {
            "title": "MATRICULA",
            "body": "Quiero informacion para matricular a mi hijo o hija.\n\nQue documentos necesito?\n\nHay plazas disponibles?",
        },
        "horarios": {
            "title": "HORARIOS",
            "body": "A que hora empieza la clase?\n\nA que hora termina?\n\nHay comedor escolar?",
        },
        "secretaria": {
            "title": "SECRETARIA",
            "body": "Donde esta la secretaria?\n\nNecesito entregar estos documentos.\n\nCon quien puedo hablar?",
        },
        "comedor": {
            "title": "COMEDOR ESCOLAR",
            "body": "Hay comedor escolar?\n\nCuanto cuesta?\n\nMi hijo o hija tiene alergias.",
        },
        "tutor": {
            "title": "TUTOR o PROFESORADO",
            "body": "Quiero hablar con el tutor.\n\nCuando puedo tener una reunion?\n\nComo va mi hijo o hija en clase?",
        },
    },
    "trabajo": {
        "tareas": {
            "title": "TAREAS",
            "body": "No entiendo esta tarea.\n\nPuede explicarmelo otra vez?\n\nMe lo puede escribir, por favor?",
        },
        "horarios": {
            "title": "HORARIOS",
            "body": "A que hora empieza el turno?\n\nCuando es el descanso?\n\nMañana trabajo tambien?",
        },
        "rrhh": {
            "title": "RECURSOS HUMANOS",
            "body": "Necesito hablar con recursos humanos.\n\nTengo una duda sobre mi contrato.\n\nEstoy aprendiendo espanol.",
        },
        "nomina": {
            "title": "NOMINA",
            "body": "Tengo una duda sobre mi nomina.\n\nFalta una hora aqui.\n\nMe lo puede explicar?",
        },
        "vacaciones": {
            "title": "VACACIONES o AUSENCIAS",
            "body": "Quiero pedir vacaciones.\n\nNecesito ausentarme este dia.\n\nCon quien tengo que hablar?",
        },
    },
    "banco": {
        "cuenta": {
            "title": "ABRIR CUENTA",
            "body": "Quiero abrir una cuenta.\n\nQue documentos necesito?\n\nHay comisiones?",
        },
        "tarjeta": {
            "title": "TARJETA",
            "body": "Tengo un problema con mi tarjeta.\n\nNo funciona.\n\nQuiero pedir una nueva.",
        },
        "dinero": {
            "title": "DINERO",
            "body": "Quiero sacar dinero.\n\nQuiero ingresar dinero.\n\nPuede ayudarme, por favor?",
        },
        "transferencias": {
            "title": "TRANSFERENCIAS",
            "body": "Quiero hacer una transferencia.\n\nCuanto tarda en llegar?\n\nNecesito el IBAN.",
        },
        "clave_app": {
            "title": "APP Y CLAVES",
            "body": "No puedo entrar en la app.\n\nHe olvidado mi clave.\n\nPuede ayudarme a activarla?",
        },
        "cita": {
            "title": "CITA EN EL BANCO",
            "body": "Quiero pedir una cita.\n\nNecesito hablar con un gestor.\n\nCuando pueden atenderme?",
        },
    },
    "movil": {
        "sim": {
            "title": "TARJETA SIM",
            "body": "Quiero una tarjeta SIM.\n\nQue necesito para comprarla?\n\nLa quiero prepago.",
        },
        "datos": {
            "title": "INTERNET Y DATOS",
            "body": "Necesito internet en el movil.\n\nCuantos gigas incluye?\n\nHay permanencia?",
        },
        "recarga": {
            "title": "RECARGAS",
            "body": "Quiero recargar mi linea.\n\nCuanto cuesta?\n\nYa se ha hecho la recarga?",
        },
        "averia": {
            "title": "AVERIA o BLOQUEO",
            "body": "Mi movil no funciona.\n\nNo tengo cobertura.\n\nPuede ayudarme a configurarlo?",
        },
    },
    "locutorio": {
        "impresion": {
            "title": "IMPRIMIR DOCUMENTOS",
            "body": "Quiero imprimir este documento.\n\nCuanto cuesta por pagina?\n\nPuede imprimirlo en color?",
        },
        "fotocopia": {
            "title": "FOTOCOPIAS",
            "body": "Necesito una fotocopia del pasaporte.\n\nQuiero dos copias, por favor.\n\nTambien necesito escanearlo.",
        },
        "correo": {
            "title": "CORREO ELECTRONICO",
            "body": "Necesito enviar este correo.\n\nPuedo adjuntar un documento?\n\nPuede ayudarme a escribirlo?",
        },
        "internet": {
            "title": "USAR INTERNET",
            "body": "Quiero usar un ordenador.\n\nCuanto cuesta media hora?\n\nNecesito entrar en esta pagina.",
        },
    },
    "piso_compartido": {
        "habitacion": {
            "title": "BUSCAR HABITACION",
            "body": "Estoy buscando una habitacion.\n\nEsta disponible?\n\nCuanto cuesta al mes?",
        },
        "gastos": {
            "title": "GASTOS",
            "body": "Los gastos estan incluidos?\n\nCuanto se paga de luz y agua?\n\nInternet va aparte?",
        },
        "convivencia": {
            "title": "CONVIVENCIA",
            "body": "A que hora se puede usar la cocina?\n\nHay normas de la casa?\n\nCuantas personas viven aqui?",
        },
        "entrada": {
            "title": "ENTRADA",
            "body": "Cuando podria entrar a vivir?\n\nHay que pagar fianza?\n\nHay contrato?",
        },
    },
    "vecindario": {
        "presentarse": {
            "title": "PRESENTARSE",
            "body": "Hola, acabo de mudarme.\n\nSoy nueva o nuevo en el barrio.\n\nEncantada o encantado.",
        },
        "pedir_ayuda": {
            "title": "PEDIR AYUDA",
            "body": "Sabe donde esta el centro de salud?\n\nDonde esta el supermercado mas cercano?\n\nQue autobus va al centro?",
        },
        "ruidos": {
            "title": "RUIDOS o MOLESTIAS",
            "body": "Perdon por las molestias.\n\nHay mucho ruido esta noche.\n\nPuede bajar la musica, por favor?",
        },
        "basura": {
            "title": "BASURA Y RECICLAJE",
            "body": "Que dia pasan a recoger la basura?\n\nDonde estan los contenedores?\n\nDonde se recicla el vidrio?",
        },
    },
}

FIRST_STEPS_SECTIONS = {
    "empadronamiento": {
        "title": "EMPADRONAMIENTO",
        "body": (
            "Hazlo lo antes posible al llegar.\n\n"
            "Te sirve para centro de salud, colegio y otros tramites.\n\n"
            "Lleva identificacion y justificante de domicilio."
        ),
    },
    "nie_tie": {
        "title": "NIE / TIE",
        "body": (
            "Prepara pasaporte, formulario y cita previa.\n\n"
            "Revisa que la tasa este pagada antes de acudir.\n\n"
            "Guarda copia de todos tus documentos."
        ),
    },
    "seguridad_social": {
        "title": "SEGURIDAD SOCIAL",
        "body": (
            "Pide tu numero de afiliacion si vas a trabajar.\n\n"
            "Te lo pueden pedir para contrato o alta laboral.\n\n"
            "Ten a mano tu documento de identidad y datos personales."
        ),
    },
}

HEALTH_SECTIONS = {
    "modo_medico": {
        "title": "MODO MEDICO",
        "body": (
            "Frases utiles para urgencias y consultas.\n\n"
            "Ideal para explicar sintomas con claridad.\n\n"
            "Muy util cuando estas nerviosa o nervioso."
        ),
    },
    "centros_salud": {
        "title": "CENTROS DE SALUD",
        "body": (
            "Busca tu ambulatorio o centro de salud mas cercano.\n\n"
            "Localiza urgencias, farmacias y hospitales.\n\n"
            "Ten siempre una referencia cerca de casa."
        ),
    },
    "tarjeta_sanitaria": {
        "title": "TARJETA SANITARIA",
        "body": (
            "Infórmate de como pedir la tarjeta sanitaria en tu comunidad.\n\n"
            "Normalmente te pediran empadronamiento y documentacion.\n\n"
            "Es clave para acceder al sistema de salud."
        ),
    },
}

TRANSPORT_SECTIONS = {
    "bono_metro": {
        "title": "BONO DE METRO",
        "body": (
            "Consulta el bono que mas te conviene segun tu ciudad.\n\n"
            "Revisa opciones mensuales o por viajes.\n\n"
            "Suele salir mas barato que comprar billetes sueltos."
        ),
    },
    "bono_bus": {
        "title": "BONO DE AUTOBUS",
        "body": (
            "Muchas ciudades tienen tarjetas recargables.\n\n"
            "Pregunta por descuentos para estudiantes o familias.\n\n"
            "Guarda siempre la tarjeta recargada."
        ),
    },
    "como_moverse": {
        "title": "COMO MOVERSE",
        "body": (
            "Aprende las apps locales de transporte.\n\n"
            "Mira horarios, transbordos y estaciones principales.\n\n"
            "Te ayudara mucho durante los primeros dias."
        ),
    },
}

EMERGENCY_SECTIONS = {
    "llamar_112": {
        "title": "LLAMAR AL 112",
        "body": (
            "El 112 es el numero general de emergencias en Espana.\n\n"
            "Usalo para urgencias medicas, policia o bomberos.\n\n"
            "Habla despacio y da datos concretos."
        ),
    },
    "direccion_exacta": {
        "title": "DIRECCION EXACTA",
        "body": (
            "Ten preparada tu direccion escrita correctamente.\n\n"
            "Incluye calle, numero, piso y ciudad.\n\n"
            "Eso ayuda mucho al operador en una urgencia."
        ),
    },
    "documentos_urgentes": {
        "title": "DOCUMENTOS URGENTES",
        "body": (
            "Guarda copia del pasaporte, NIE o TIE y telefono de contacto.\n\n"
            "Lleva una nota con alergias o medicacion importante.\n\n"
            "Tenerlo listo puede ahorrarte mucho tiempo."
        ),
    },
}

HOUSING_SECTIONS = {
    "alquiler": {
        "title": "ALQUILER",
        "body": (
            "Antes de firmar, revisa precio, fianza y duracion del contrato.\n\n"
            "Pide siempre una copia del contrato.\n\n"
            "Pregunta si los gastos de luz, agua e internet estan incluidos."
        ),
    },
    "empadronarse": {
        "title": "EMPADRONARSE EN LA VIVIENDA",
        "body": (
            "El padrón es clave para medico, colegio y muchos tramites.\n\n"
            "Pregunta al casero si necesitas autorizacion o contrato.\n\n"
            "Guarda recibos o documentos que prueben donde vives."
        ),
    },
    "suministros": {
        "title": "LUZ, AGUA E INTERNET",
        "body": (
            "Comprueba a nombre de quien estan los suministros.\n\n"
            "Pregunta como se pagan y cada cuanto llegan las facturas.\n\n"
            "Ten a mano una compania de internet y un numero de telefono local."
        ),
    },
}

WORK_SECTIONS = {
    "buscar_trabajo": {
        "title": "BUSCAR TRABAJO",
        "body": (
            "Prepara un currículum sencillo y adaptado a Espana.\n\n"
            "Revisa si necesitas permiso de trabajo segun tu situacion.\n\n"
            "Ten listos telefono, correo y documentacion basica."
        ),
    },
    "contrato": {
        "title": "CONTRATO Y NOMINA",
        "body": (
            "Lee bien horario, salario y tipo de contrato.\n\n"
            "Guarda copia del contrato y de cada nomina.\n\n"
            "Pregunta cualquier termino que no entiendas antes de firmar."
        ),
    },
    "derechos_basicos": {
        "title": "DERECHOS BASICOS",
        "body": (
            "Tienes derecho a saber tus horarios, salario y condiciones.\n\n"
            "No entregues documentos originales sin necesidad.\n\n"
            "Si algo no esta claro, pide explicaciones por escrito."
        ),
    },
}

# Correcciones de texto visibles para tildes, eñes y posibles caracteres corruptos.
SPANISH_SURVIVAL_SECTIONS["transporte"]["body"] = (
    "¿Este autobús va al centro?\n\n"
    "¿Dónde compro el billete?\n\n"
    "¿En qué parada tengo que bajar?\n\n"
    "¿Cuánto cuesta el bono?\n\n"
    "Gracias por su ayuda."
)
SPANISH_SURVIVAL_SECTIONS["comisaria"]["title"] = "EN UNA COMISARÍA"
SPANISH_SURVIVAL_SECTIONS["comisaria"]["body"] = (
    "Necesito ayuda.\n\n"
    "Quiero poner una denuncia.\n\n"
    "He perdido mi documentación.\n\n"
    "No hablo bien español.\n\n"
    "¿Puede hablar más despacio, por favor?"
)
SPANISH_SURVIVAL_SECTIONS["movil"]["title"] = "EN UNA TIENDA DE MÓVIL"
SPANISH_SURVIVAL_SECTIONS["movil"]["body"] = (
    "Quiero una tarjeta SIM.\n\n"
    "Necesito internet en el móvil.\n\n"
    "¿Cuánto cuesta este plan?\n\n"
    "Necesito ayuda para activar la línea.\n\n"
    "¿Puedo recargar aquí?"
)
SPANISH_SURVIVAL_SECTIONS["piso_compartido"]["body"] = (
    "Estoy buscando una habitación.\n\n"
    "¿Los gastos están incluidos?\n\n"
    "¿Puedo empadronarme aquí?\n\n"
    "¿Hay contrato?\n\n"
    "¿Cuándo podría entrar a vivir?"
)
SPANISH_SURVIVAL_SECTIONS["vecindario"]["body"] = (
    "Hola, acabo de mudarme.\n\n"
    "¿Sabe dónde está el centro de salud?\n\n"
    "¿A qué hora pasa el autobús?\n\n"
    "¿Dónde está el supermercado más cercano?\n\n"
    "Muchas gracias por su ayuda."
)

HEALTH_SECTIONS["modo_medico"]["title"] = "MODO MÉDICO"
HEALTH_SECTIONS["modo_medico"]["body"] = (
    "Frases útiles para urgencias y consultas.\n\n"
    "Ideal para explicar síntomas con claridad.\n\n"
    "Muy útil cuando estás nerviosa o nervioso."
)
HEALTH_SECTIONS["centros_salud"]["body"] = (
    "Busca tu ambulatorio o centro de salud más cercano.\n\n"
    "Localiza urgencias, farmacias y hospitales.\n\n"
    "Ten siempre una referencia cerca de casa."
)
HEALTH_SECTIONS["tarjeta_sanitaria"]["body"] = (
    "Infórmate de cómo pedir la tarjeta sanitaria en tu comunidad.\n\n"
    "Normalmente te pedirán empadronamiento y documentación.\n\n"
    "Es clave para acceder al sistema de salud."
)

TRANSPORT_SECTIONS["bono_metro"]["body"] = (
    "Consulta el bono que más te conviene según tu ciudad.\n\n"
    "Revisa opciones mensuales o por viajes.\n\n"
    "Suele salir más barato que comprar billetes sueltos."
)
TRANSPORT_SECTIONS["bono_bus"]["title"] = "BONO DE AUTOBÚS"
TRANSPORT_SECTIONS["como_moverse"]["title"] = "CÓMO MOVERSE"
TRANSPORT_SECTIONS["como_moverse"]["body"] = (
    "Aprende las apps locales de transporte.\n\n"
    "Mira horarios, transbordos y estaciones principales.\n\n"
    "Te ayudará mucho durante los primeros días."
)

EMERGENCY_SECTIONS["llamar_112"]["body"] = (
    "El 112 es el número general de emergencias en España.\n\n"
    "Úsalo para urgencias médicas, policía o bomberos.\n\n"
    "Habla despacio y da datos concretos."
)
EMERGENCY_SECTIONS["direccion_exacta"]["title"] = "DIRECCIÓN EXACTA"
EMERGENCY_SECTIONS["direccion_exacta"]["body"] = (
    "Ten preparada tu dirección escrita correctamente.\n\n"
    "Incluye calle, número, piso y ciudad.\n\n"
    "Eso ayuda mucho al operador en una urgencia."
)
EMERGENCY_SECTIONS["documentos_urgentes"]["body"] = (
    "Guarda copia del pasaporte, NIE o TIE y teléfono de contacto.\n\n"
    "Lleva una nota con alergias o medicación importante.\n\n"
    "Tenerlo listo puede ahorrarte mucho tiempo."
)

HOUSING_SECTIONS["alquiler"]["body"] = (
    "Antes de firmar, revisa precio, fianza y duración del contrato.\n\n"
    "Pide siempre una copia del contrato.\n\n"
    "Pregunta si los gastos de luz, agua e internet están incluidos."
)
HOUSING_SECTIONS["empadronarse"]["body"] = (
    "El padrón es clave para médico, colegio y muchos trámites.\n\n"
    "Pregunta al casero si necesitas autorización o contrato.\n\n"
    "Guarda recibos o documentos que prueben dónde vives."
)
HOUSING_SECTIONS["suministros"]["body"] = (
    "Comprueba a nombre de quién están los suministros.\n\n"
    "Pregunta cómo se pagan y cada cuánto llegan las facturas.\n\n"
    "Ten a mano una compañía de internet y un número de teléfono local."
)

WORK_SECTIONS["buscar_trabajo"]["body"] = (
    "Prepara un currículum sencillo y adaptado a España.\n\n"
    "Revisa si necesitas permiso de trabajo según tu situación.\n\n"
    "Ten listos teléfono, correo y documentación básica."
)
WORK_SECTIONS["contrato"]["title"] = "CONTRATO Y NÓMINA"
WORK_SECTIONS["contrato"]["body"] = (
    "Lee bien horario, salario y tipo de contrato.\n\n"
    "Guarda copia del contrato y de cada nómina.\n\n"
    "Pregunta cualquier término que no entiendas antes de firmar."
)
WORK_SECTIONS["derechos_basicos"]["title"] = "DERECHOS BÁSICOS"
WORK_SECTIONS["derechos_basicos"]["body"] = (
    "Tienes derecho a saber tus horarios, salario y condiciones.\n\n"
    "No entregues documentos originales sin necesidad.\n\n"
    "Si algo no está claro, pide explicaciones por escrito."
)

SPANISH_SURVIVAL_SECTIONS["aeropuerto"] = {
    "title": "EN EL AEROPUERTO",
    "body": (
        "Donde esta la salida?\n\n"
        "De que terminal sale este vuelo?\n\n"
        "Donde recojo mi maleta?\n\n"
        "Necesito ayuda con este billete.\n\n"
        "Gracias por su ayuda."
    ),
}
SPANISH_SURVIVAL_SECTIONS["oficina_empleo"] = {
    "title": "EN LA OFICINA DE EMPLEO",
    "body": (
        "Quiero apuntarme como demandante de empleo.\n\n"
        "Tengo cita para hoy.\n\n"
        "Necesito ayuda con este trámite.\n\n"
        "Qué documentos necesito?\n\n"
        "Gracias por su ayuda."
    ),
}
SPANISH_SURVIVAL_SECTIONS["entrevista"] = {
    "title": "EN UNA ENTREVISTA DE TRABAJO",
    "body": (
        "Gracias por recibirme.\n\n"
        "Tengo experiencia en este tipo de trabajo.\n\n"
        "Estoy aprendiendo español.\n\n"
        "Puedo incorporarme pronto.\n\n"
        "¿Cuáles serían mis tareas?"
    ),
}
SPANISH_SURVIVAL_SECTIONS["servicios_sociales"] = {
    "title": "EN SERVICIOS SOCIALES",
    "body": (
        "Necesito información y orientación.\n\n"
        "Acabo de llegar y no sé por dónde empezar.\n\n"
        "Necesito ayuda con vivienda o ayudas.\n\n"
        "Tengo una cita hoy.\n\n"
        "¿Qué documentos debo traer?"
    ),
}
SPANISH_SURVIVAL_SECTIONS["ong"] = {
    "title": "EN UNA ONG O ASOCIACION",
    "body": (
        "Necesito orientación.\n\n"
        "Acabo de llegar a España.\n\n"
        "Busco apoyo con trámites o vivienda.\n\n"
        "¿Pueden ayudarme?\n\n"
        "Gracias."
    ),
}
SPANISH_SURVIVAL_SECTIONS["academia_espanol"] = {
    "title": "EN UNA ACADEMIA DE ESPANOL",
    "body": (
        "Quiero aprender español.\n\n"
        "¿Tienen cursos para principiantes?\n\n"
        "¿Cuánto cuesta?\n\n"
        "¿Qué horario tienen?\n\n"
        "Quiero apuntarme."
    ),
}
SPANISH_SURVIVAL_SECTIONS["guarderia"] = {
    "title": "EN UNA GUARDERIA",
    "body": (
        "Busco plaza para mi hijo o hija.\n\n"
        "¿Qué documentos necesito?\n\n"
        "¿Cuánto cuesta?\n\n"
        "¿Qué horario tienen?\n\n"
        "Gracias por la información."
    ),
}
SPANISH_SURVIVAL_SECTIONS["visita_piso"] = {
    "title": "AL VISITAR UN PISO",
    "body": (
        "Estoy interesada o interesado en este piso.\n\n"
        "¿Cuánto cuesta al mes?\n\n"
        "¿Qué gastos incluye?\n\n"
        "¿Puedo empadronarme aquí?\n\n"
        "Gracias."
    ),
}
SPANISH_SURVIVAL_SECTIONS["jerga"] = {
    "title": "JERGA Y EXPRESIONES",
    "body": (
        "No me comas la cabeza.\n\n"
        "Me da vergüenza ajena.\n\n"
        "Vamos de tapeo.\n\n"
        "Estoy desvelada o desvelado.\n\n"
        "Voy a estrenar esta chaqueta."
    ),
}

SPANISH_SURVIVAL_DETAILS["aeropuerto"] = {
    "facturacion": {
        "title": "FACTURACION",
        "body": "Donde facturo esta maleta?\n\nCuanto equipaje puedo llevar?\n\nNecesito imprimir la tarjeta de embarque?",
    },
    "embarque": {
        "title": "EMBARQUE",
        "body": "De que puerta sale el vuelo?\n\nA que hora empieza el embarque?\n\nVoy bien para esta terminal?",
    },
    "equipaje": {
        "title": "EQUIPAJE",
        "body": "Donde recojo mi maleta?\n\nMi maleta no ha llegado.\n\nDonde puedo poner una reclamacion?",
    },
    "controles": {
        "title": "CONTROLES",
        "body": "Que tengo que sacar de la mochila?\n\nPuedo pasar con esto?\n\nDonde esta el control de pasaportes?",
    },
}
SPANISH_SURVIVAL_DETAILS["oficina_empleo"] = {
    "demanda": {
        "title": "DEMANDA DE EMPLEO",
        "body": "Quiero apuntarme como demandante de empleo.\n\nTengo cita para hoy.\n\nQué documentos necesito?",
    },
    "cursos": {
        "title": "CURSOS",
        "body": "Hay cursos de formación?\n\nQuiero mejorar mi español para trabajar.\n\nCómo me apunto?",
    },
    "ofertas": {
        "title": "OFERTAS DE TRABAJO",
        "body": "Estoy buscando trabajo.\n\nHay ofertas para este perfil?\n\nPuede orientarme, por favor?",
    },
    "cita": {
        "title": "CITA",
        "body": "Tengo una cita previa.\n\nVengo para este trámite.\n\nDónde tengo que esperar?",
    },
}
SPANISH_SURVIVAL_DETAILS["entrevista"] = {
    "presentacion": {
        "title": "PRESENTACION",
        "body": "Gracias por recibirme.\n\nTengo experiencia en este sector.\n\nEstoy muy interesada o interesado en el puesto.",
    },
    "experiencia": {
        "title": "EXPERIENCIA",
        "body": "He trabajado en esto antes.\n\nEstas eran mis tareas principales.\n\nAprendo rápido y me adapto bien.",
    },
    "idioma": {
        "title": "IDIOMA",
        "body": "Estoy aprendiendo español.\n\nEntiendo bastante, pero a veces necesito que hablen más despacio.\n\nSigo mejorando cada día.",
    },
    "disponibilidad": {
        "title": "DISPONIBILIDAD",
        "body": "Puedo incorporarme pronto.\n\nTengo disponibilidad horaria.\n\nPuedo trabajar fines de semana si hace falta.",
    },
}
SPANISH_SURVIVAL_DETAILS["servicios_sociales"] = {
    "orientacion": {
        "title": "ORIENTACION",
        "body": "Acabo de llegar y no sé por dónde empezar.\n\nNecesito orientación.\n\nQué pasos me recomienda hacer primero?",
    },
    "ayudas": {
        "title": "AYUDAS",
        "body": "Quiero información sobre ayudas.\n\nHay apoyo para vivienda o alimentos?\n\nQué requisitos hay?",
    },
    "vivienda": {
        "title": "VIVIENDA",
        "body": "Necesito ayuda para encontrar vivienda.\n\nEstoy en una situación difícil.\n\nPueden orientarme, por favor?",
    },
    "cita": {
        "title": "CITA",
        "body": "Tengo cita para hoy.\n\nQué documentos debo traer?\n\nDónde tengo que esperar?",
    },
}
SPANISH_SURVIVAL_DETAILS["ong"] = {
    "orientacion": {
        "title": "ORIENTACION",
        "body": "Acabo de llegar a España.\n\nNecesito orientación.\n\n¿Pueden ayudarme, por favor?",
    },
    "tramites": {
        "title": "TRAMITES",
        "body": "Necesito ayuda con mis trámites.\n\nNo entiendo bien este documento.\n\n¿Me lo pueden explicar?",
    },
    "vivienda": {
        "title": "VIVIENDA",
        "body": "Busco ayuda con vivienda.\n\nEstoy en una situación difícil.\n\n¿Conocen algún recurso?",
    },
    "cita": {
        "title": "CITA",
        "body": "Tengo una cita para hoy.\n\nVengo a pedir información.\n\n¿Dónde tengo que esperar?",
    },
}
SPANISH_SURVIVAL_DETAILS["academia_espanol"] = {
    "niveles": {
        "title": "CURSOS Y NIVELES",
        "body": "Quiero aprender español.\n\n¿Tienen cursos para principiantes?\n\n¿Qué nivel me recomiendan?",
    },
    "horarios": {
        "title": "HORARIOS",
        "body": "¿Qué horario tienen?\n\nTrabajo por las mañanas.\n\n¿Hay clases por la tarde?",
    },
    "precio": {
        "title": "PRECIO",
        "body": "¿Cuánto cuesta el curso?\n\n¿Se paga al mes?\n\n¿Hay descuento?",
    },
    "matricula": {
        "title": "MATRICULA",
        "body": "Quiero apuntarme.\n\n¿Qué documentos necesito?\n\n¿Cuándo empieza el curso?",
    },
}
SPANISH_SURVIVAL_DETAILS["guarderia"] = {
    "plaza": {
        "title": "PLAZA",
        "body": "Busco plaza para mi hijo o hija.\n\n¿Tienen plazas disponibles?\n\n¿Desde qué edad aceptan niños?",
    },
    "documentos": {
        "title": "DOCUMENTOS",
        "body": "¿Qué documentos necesito?\n\n¿Hace falta empadronamiento?\n\n¿Tengo que pedir cita?",
    },
    "horarios": {
        "title": "HORARIOS",
        "body": "¿Qué horario tienen?\n\n¿Abren por la mañana?\n\n¿Hay servicio de comedor?",
    },
    "precio": {
        "title": "PRECIO",
        "body": "¿Cuánto cuesta?\n\n¿Hay ayudas o descuentos?\n\n¿Cómo se paga?",
    },
}
SPANISH_SURVIVAL_DETAILS["visita_piso"] = {
    "precio": {
        "title": "PRECIO",
        "body": "¿Cuánto cuesta al mes?\n\n¿La fianza está incluida?\n\n¿Qué gastos se pagan aparte?",
    },
    "empadronamiento": {
        "title": "EMPADRONAMIENTO",
        "body": "¿Puedo empadronarme aquí?\n\n¿Lo pondrían en el contrato?\n\n¿Necesito autorización del propietario?",
    },
    "condiciones": {
        "title": "CONDICIONES",
        "body": "¿Cuánto dura el contrato?\n\n¿Se puede entrar este mes?\n\n¿Aceptan familias o niños?",
    },
    "suministros": {
        "title": "SUMINISTROS",
        "body": "¿Incluye luz, agua o internet?\n\n¿A nombre de quién están?\n\n¿Cuánto se paga normalmente?",
    },
}
SPANISH_SURVIVAL_DETAILS["jerga"] = {
    "cotidianas": {
        "title": "EXPRESIONES COTIDIANAS",
        "body": "No me comas la cabeza.\n\nMe da vergüenza ajena.\n\nEstoy a tope hoy.",
    },
    "social": {
        "title": "PLANES y AMBIENTE",
        "body": "Vamos de tapeo.\n\nHay muy buen rollo.\n\nEse sitio está muy guay.",
    },
    "literal": {
        "title": "NO SE TRADUCE LITERAL",
        "body": "Estoy desvelada o desvelado.\n\nVoy a estrenar esta chaqueta.\n\nHoy hubo mucha sobremesa.",
    },
    "trabajo_calle": {
        "title": "TRABAJO y CALLE",
        "body": "Voy pillada o pillado de tiempo.\n\nEsto me viene fatal hoy.\n\nTe aviso ahora mismo.",
    },
}


DEFAULT_BEHAVIOUR_BODIES = {
    "restaurante": "Observa primero si se pide en mesa o en barra.\n\nPedir con por favor y dar las gracias se valora mucho.\n\nLa propina no siempre es obligatoria; si se deja, suele ser pequeña.",
    "hospital": "Hablar con calma y explicar lo importante primero ayuda mucho.\n\nSi no entiendes algo, pide que te lo repitan más despacio.\n\nTener a mano tus documentos puede facilitar la atención.",
    "farmacia": "Conviene explicar el síntoma con calma y sin vergüenza.\n\nEscucha bien cómo tomar el medicamento antes de irte.\n\nSi no entiendes una indicación, pregunta otra vez.",
    "hotel": "Un trato amable y claro suele funcionar muy bien.\n\nEs normal preguntar en recepción si tienes dudas prácticas.\n\nAvisar con educación facilita resolver problemas.",
    "aeropuerto": "Conviene tener documentación y billete preparados.\n\nObservar las filas y seguir las indicaciones del personal ayuda mucho.\n\nSi tienes dudas, pregunta antes de avanzar.",
    "transporte": "Respeta filas, turnos y espacio en andenes o paradas.\n\nSi no sabes dónde validar o subir, observa primero.\n\nPreguntar con educación suele funcionar bien.",
    "ayuntamiento": "Lleva documentos preparados y espera tu turno.\n\nUn tono respetuoso y claro ayuda mucho en trámites.\n\nSi no entiendes algo, pide que te indiquen el paso siguiente.",
    "extranjeria": "Conviene llevar toda la documentación preparada y seguir el turno indicado.\n\nMantener la calma ayuda mucho si hay espera o dudas.\n\nSi falta algo, pregunta con claridad qué necesitas exactamente.",
    "servicios_sociales": "Explica tu situación con calma y claridad.\n\nNo pasa nada por decir que no entiendes algo o que necesitas ayuda.\n\nLlevar papeles básicos puede facilitar la orientación.",
    "ong": "Hablar con sinceridad y calma suele ayudar mucho.\n\nEs normal pedir orientación si no sabes por dónde empezar.\n\nPregunta sin miedo si no entiendes un documento o trámite.",
    "oficina_empleo": "Conviene llegar con tiempo y con la documentación preparada.\n\nHablar claro sobre tu situación y experiencia ayuda mucho.\n\nSi no entiendes un paso, pide que te lo expliquen.",
    "academia_espanol": "No pasa nada por decir que estás empezando desde cero.\n\nPreguntar horarios, nivel y forma de pago es completamente normal.\n\nMostrar interés y constancia suele ayudar mucho.",
    "entrevista": "Saludar, escuchar y responder con calma transmite buena impresión.\n\nSi no entiendes una pregunta, puedes pedir que la repitan más despacio.\n\nEs mejor ser clara o claro que intentar aparentar seguridad sin entender.",
    "jerga": "No intentes usar todas las expresiones a la vez.\n\nPrimero conviene entender el tono y cuándo se usan.\n\nSi tienes dudas, mejor usar un lenguaje más neutro.",
    "guarderia": "Conviene hablar con calma y preguntar todo lo importante sin miedo.\n\nLlevar documentos preparados suele ayudar mucho.\n\nUn tono amable y claro facilita la comunicación.",
    "casero": "Es mejor dejar claras las condiciones desde el principio.\n\nPregunta con educación, pero no des nada por hecho si no está claro.\n\nSi algo es importante, intenta que quede por escrito.",
    "visita_piso": "Observa primero y pregunta con calma antes de decidir.\n\nEs normal preguntar por gastos, contrato o empadronamiento.\n\nNo tengas miedo de confirmar lo que incluye realmente.",
    "centro_salud": "Hablar con calma y explicar el problema principal primero ayuda mucho.\n\nSi no entiendes una indicación, pide que te la repitan o la escriban.\n\nRespetar turnos y tiempos de espera es importante.",
    "correos": "Lleva preparado lo que quieres enviar o recoger.\n\nObserva primero la fila y el funcionamiento del mostrador.\n\nPreguntar con educación suele resolver rápido las dudas.",
    "supermercado": "Respeta la fila y ten preparado el pago al llegar a caja.\n\nSi no encuentras algo, preguntar es totalmente normal.\n\nEn cajas rápidas conviene ir con agilidad si hay gente esperando.",
    "tienda_ropa": "Preguntar por talla, color o cambios es totalmente normal.\n\nUn tono amable suele facilitar mucho la atención.\n\nSi no te convence algo, puedes decirlo con naturalidad.",
    "taxi": "Conviene indicar el destino con claridad al empezar.\n\nSi tienes una preferencia de ruta o pago, dilo pronto y con educación.\n\nAl final, un gracias suele bastar.",
    "comisaria": "Habla con calma y céntrate en los hechos importantes.\n\nSi no entiendes algo, pide que te lo repitan despacio.\n\nLlevar documentación preparada ayuda mucho.",
    "colegio": "Conviene hablar con respeto y claridad, sobre todo al principio.\n\nPreguntar por horarios, documentos o tutorías es normal.\n\nEscuchar primero cómo funciona el centro ayuda mucho.",
    "trabajo": "Observar primero el tono y la dinámica del lugar ayuda mucho.\n\nSer puntual, clara o claro y respetuoso suele valorarse bastante.\n\nSi no entiendes algo, es mejor preguntar que improvisar.",
    "banco": "Hablar claro y llevar documentos preparados facilita mucho el trámite.\n\nSi no entiendes una comisión o condición, pregunta antes de aceptar.\n\nEs mejor confirmar bien cada paso.",
    "movil": "Conviene preguntar con claridad por precio, datos y permanencia.\n\nSi algo no queda claro, pide que te lo expliquen más despacio.\n\nNo tengas prisa en aceptar una tarifa sin entenderla bien.",
    "locutorio": "Suelen ser espacios muy prácticos y directos.\n\nPide lo que necesitas con claridad y pregunta el precio antes si quieres.\n\nEs normal pedir ayuda para imprimir, escanear o enviar algo.",
    "piso_compartido": "Observa el ambiente y pregunta con naturalidad por normas y gastos.\n\nEs mejor dejar claras convivencia, entrada y pagos desde el principio.\n\nSi algo es importante para ti, confírmalo antes de aceptar.",
    "vecindario": "Un saludo amable suele abrir muchas puertas.\n\nPedir ayuda con educación normalmente se recibe bien.\n\nObservar costumbres del barrio ayuda a integrarte mejor.",
}


def ensure_behaviour_sections() -> None:
    for key, details in list(SPANISH_SURVIVAL_DETAILS.items()):
        behaviour_body = DEFAULT_BEHAVIOUR_BODIES.get(
            key,
            "Observa primero cómo actúan los demás en esta situación.\n\nHablar con calma y con educación suele ayudar mucho.\n\nSi no entiendes algo, preguntar con respeto normalmente funciona bien.",
        )
        behaviour_entry = {
            "title": "COMPORTAMIENTO y COSTUMBRES",
            "body": behaviour_body,
        }
        if "comportamiento" in details:
            existing = details["comportamiento"]
            details = {"comportamiento": existing, **{k: v for k, v in details.items() if k != "comportamiento"}}
        else:
            details = {"comportamiento": behaviour_entry, **details}
        SPANISH_SURVIVAL_DETAILS[key] = details


ensure_behaviour_sections()


BG_GRADIENT = ft.LinearGradient(
    begin=ft.Alignment(-1, -1),
    end=ft.Alignment(1, 1),
    colors=["#FFFFFF", SOFT_AMETHYST, AMETHYST],
)


def card(content: list[ft.Control]) -> ft.Container:
    return ft.Container(
        content=ft.Column(content, spacing=18, tight=True),
        padding=24,
        border_radius=28,
        bgcolor=ft.Colors.with_opacity(0.96, "#FFFFFF"),
    )


def phone_frame(content: ft.Control) -> ft.Container:
    return ft.Container(
        width=360,
        height=760,
        padding=10,
        border_radius=36,
        bgcolor="#111111",
        border=ft.Border.all(3, AMETHYST),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=24,
            color=ft.Colors.with_opacity(0.28, "#000000"),
            offset=ft.Offset(0, 10),
        ),
        content=ft.Stack(
            [
                ft.Container(
                    expand=True,
                    border_radius=28,
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    content=content,
                ),
                ft.Container(
                    alignment=ft.Alignment(0, -1),
                    margin=ft.Margin.only(top=8),
                    ignore_interactions=True,
                    content=ft.Container(
                        width=110,
                        height=18,
                        border_radius=12,
                        bgcolor="#111111",
                    ),
                ),
            ]
        ),
    )


def mobile_button(text: str, on_click, bgcolor: str, color: str = "#FFFFFF") -> ft.Button:
    text = restore_spanish_accents(text)
    return ft.Button(
        content=ft.Text(text),
        on_click=on_click,
        width=300,
        style=ft.ButtonStyle(
            bgcolor=bgcolor,
            color=color,
            padding=18,
            side=ft.BorderSide(2, AMETHYST),
            shape=ft.RoundedRectangleBorder(radius=18),
            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_700, font_family=TITLE_FONT),
        ),
        height=56,
    )


def bilingual_mobile_button(
    text_es: str,
    text_en: str,
    on_click,
    bgcolor: str,
    color: str = "#FFFFFF",
    width: int = 300,
    height: int = 72,
) -> ft.Button:
    text_es = restore_spanish_accents(text_es)
    icon_name = BUTTON_ICONS.get(text_es)
    if icon_name is None and text_es.startswith("Volver"):
        icon_name = ft.Icons.ARROW_BACK_ROUNDED
    if icon_name is None and text_es.startswith("Clases online"):
        icon_name = ft.Icons.CHAT_OUTLINED
    title_size = 13 if len(text_es) >= 26 else 14 if len(text_es) >= 22 else 16
    title_width = max(180, width - 110)
    button_height = 84 if len(text_es) >= 28 else height
    title_row_controls: list[ft.Control] = []
    if icon_name:
        title_row_controls.append(
            ft.Icon(
                icon_name,
                size=15,
                color=color,
            )
        )
    title_row_controls.append(
        ft.Container(
            width=title_width,
            alignment=ft.Alignment(0, 0),
            content=ft.Text(
                text_es,
                text_align=ft.TextAlign.CENTER,
                size=title_size,
                weight=ft.FontWeight.W_700,
                font_family=TITLE_FONT,
                color=color,
                no_wrap=False,
                max_lines=2,
            ),
        )
    )

    return ft.Button(
        content=ft.Column(
            [
                ft.Row(
                    title_row_controls,
                    spacing=6,
                    tight=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Text(
                    text_en,
                    text_align=ft.TextAlign.CENTER,
                    size=11,
                    weight=ft.FontWeight.W_700,
                    italic=True,
                    color=color,
                    no_wrap=False,
                    max_lines=2,
                ),
            ],
            spacing=2,
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        on_click=on_click,
        width=width,
        style=ft.ButtonStyle(
            bgcolor=bgcolor,
            color=color,
            padding=14,
            side=ft.BorderSide(2, AMETHYST),
            shape=ft.RoundedRectangleBorder(radius=18),
        ),
        height=button_height,
    )


BUTTON_TRANSLATIONS = {
    "Primeros 7 días": "First 7 days",
    "Documentos": "Documents",
    "Salud": "Health",
    "Transporte": "Transport",
    "Emergencias": "Emergencies",
    "Vivienda": "Housing",
    "Trabajo": "Work",
    "Integración": "Integration",
    "Preguntas frecuentes": "Frequently asked questions",
    "Volver al inicio": "Back to home",
    "Volver al kit": "Back to kit",
    "Volver a administrativa": "Back to admin",
    "Volver a comunicación": "Back to communication",
    "Volver a comunidad": "Back to community",
    "Volver a integración": "Back to integration",
    "Volver a preguntas": "Back to questions",
    "Volver a primeros pasos": "Back to first steps",
    "Volver a tramites": "Back to procedures",
    "Volver a trámites": "Back to procedures",
    "Volver a salud": "Back to health",
    "Volver a transporte": "Back to transport",
    "Volver a emergencias": "Back to emergencies",
    "Volver a vivienda": "Back to housing",
    "Volver a trabajo": "Back to work",
    "NIE / TIE": "NIE / TIE",
    "Empadronamiento": "Registration",
    "Seguridad Social": "Social Security",
    "Modo médico": "Medical mode",
    "Escáner de documentos": "Document scanner",
    "Jerga española": "Spanish slang",
    "Mapa de servicios": "Service map",
    "Foro de recién llegados": "Newcomers forum",
    "Intercambio de idiomas": "Language exchange",
    "¿Cómo pido la cita del NIE?": "How do I book the NIE appointment?",
    "¿Para qué sirve el empadronamiento?": "What is registration for?",
    "¿Cómo consigo el número de Seguridad Social?": "How do I get a Social Security number?",
    "¿Cuándo tengo que llamar al 112?": "When should I call 112?",
    "¿Cómo pido la tarjeta sanitaria?": "How do I get the health card?",
    "¿Qué bono de transporte me conviene?": "Which transport pass suits me?",
    "Centros de salud": "Health centers",
    "Tarjeta sanitaria": "Health card",
    "Bono de metro": "Metro pass",
    "Bono de autobús": "Bus pass",
    "Cómo moverse": "Getting around",
    "Llamar al 112": "Call 112",
    "Dirección exacta": "Exact address",
    "Documentos urgentes": "Urgent documents",
    "Alquiler": "Renting",
    "Empadronarse": "Register address",
    "Luz, agua e internet": "Utilities and internet",
    "Buscar trabajo": "Find work",
    "Contrato y nómina": "Contract and payslip",
    "Derechos básicos": "Basic rights",
    "Volver": "Back",
}


BUTTON_ICONS = {
    "Seguir en TikTok": ft.Icons.MUSIC_NOTE,
    "Seguir en Instagram": ft.Icons.CAMERA_ALT,
    "Página web": ft.Icons.LANGUAGE,
    "Continuar": ft.Icons.ARROW_FORWARD_ROUNDED,
    "KIT DE SUPERVIVENCIA": ft.Icons.SHIELD_OUTLINED,
    "ESPAÑOL PARA LA VIDA DIARIA": ft.Icons.RECORD_VOICE_OVER_OUTLINED,
    "Primeros 7 días": ft.Icons.CALENDAR_MONTH_OUTLINED,
    "Documentos": ft.Icons.DESCRIPTION_OUTLINED,
    "Salud": ft.Icons.LOCAL_HOSPITAL_OUTLINED,
    "Transporte": ft.Icons.DIRECTIONS_BUS_OUTLINED,
    "Emergencias": ft.Icons.WARNING_AMBER_ROUNDED,
    "Vivienda": ft.Icons.HOME_OUTLINED,
    "Trabajo": ft.Icons.WORK_OUTLINE,
    "Integración": ft.Icons.PEOPLE_ALT_OUTLINED,
    "Preguntas frecuentes": ft.Icons.HELP_OUTLINE,
    "NIE / TIE": ft.Icons.BADGE_OUTLINED,
    "Empadronamiento": ft.Icons.HOW_TO_REG_OUTLINED,
    "Seguridad Social": ft.Icons.ADMIN_PANEL_SETTINGS_OUTLINED,
    "Modo médico": ft.Icons.MEDICAL_SERVICES_OUTLINED,
    "Escáner de documentos": ft.Icons.DOCUMENT_SCANNER_OUTLINED,
    "Jerga española": ft.Icons.TRANSLATE_OUTLINED,
    "Mapa de servicios": ft.Icons.MAP_OUTLINED,
    "Foro de recién llegados": ft.Icons.FORUM_OUTLINED,
    "Intercambio de idiomas": ft.Icons.CHAT_OUTLINED,
    "Buscar trabajo": ft.Icons.WORK_OUTLINE,
    "Contrato y nómina": ft.Icons.RECEIPT_LONG_OUTLINED,
    "Derechos básicos": ft.Icons.GAVEL_OUTLINED,
    "Bono de metro": ft.Icons.TRAIN_OUTLINED,
    "Bono de autobús": ft.Icons.DIRECTIONS_BUS_OUTLINED,
    "Cómo moverse": ft.Icons.ALT_ROUTE_OUTLINED,
    "Llamar al 112": ft.Icons.CALL_OUTLINED,
    "Dirección exacta": ft.Icons.PIN_DROP_OUTLINED,
    "Documentos urgentes": ft.Icons.FOLDER_SPECIAL_OUTLINED,
    "Alquiler": ft.Icons.KEY_OUTLINED,
    "Empadronarse": ft.Icons.APPROVAL_OUTLINED,
    "Luz, agua e internet": ft.Icons.ROUTER_OUTLINED,
}


SPANISH_SURVIVAL_LABELS = {
    "restaurante": "Restaurante / Restaurant",
    "hospital": "Hospital / Hospital",
    "farmacia": "Farmacia / Pharmacy",
    "hotel": "Hotel / Hotel",
    "aeropuerto": "Aeropuerto / Airport",
    "transporte": "Transporte / Transport",
    "ayuntamiento": "Ayuntamiento / City hall",
    "extranjeria": "Extranjería / Immigration",
    "servicios_sociales": "Servicios sociales / Social services",
    "ong": "ONG o asociación / NGO or association",
    "oficina_empleo": "Oficina de empleo / Employment office",
    "academia_espanol": "Academia de español / Spanish academy",
    "entrevista": "Entrevista de trabajo / Job interview",
    "jerga": "Jerga y expresiones / Real-life expressions",
    "guarderia": "Guardería / Nursery",
    "casero": "Casero / Landlord",
    "visita_piso": "Visitar un piso / Flat viewing",
    "centro_salud": "Centro de salud / Health center",
    "correos": "Correos / Post office",
    "supermercado": "Supermercado / Supermarket",
    "tienda_ropa": "Tienda de ropa / Clothing store",
    "taxi": "Taxi / Taxi",
    "comisaria": "Comisaría / Police station",
    "colegio": "Colegio / School",
    "trabajo": "Trabajo / Work",
    "banco": "Banco / Bank",
    "movil": "Tienda de móvil / Phone shop",
    "locutorio": "Locutorio / Call shop",
    "piso_compartido": "Piso compartido / Shared flat",
    "vecindario": "Vecinos o barrio / Neighbors or area",
}


def menu_bilingual_button(text: str, on_click, bgcolor: str = RED, color: str = "#FFFFFF") -> ft.Button:
    normalized_text = restore_spanish_accents(text)
    return bilingual_mobile_button(
        normalized_text,
        BUTTON_TRANSLATIONS.get(normalized_text, BUTTON_TRANSLATIONS.get(text, normalized_text)),
        on_click,
        bgcolor,
        color,
    )


TRANSLATION_UNAVAILABLE_EN = "English translation unavailable right now."


def is_unavailable_english_translation(text: str) -> bool:
    return normalize_translation_lookup(text) == normalize_translation_lookup(TRANSLATION_UNAVAILABLE_EN)


def formatted_english_heading(text: str) -> str:
    text = restore_spanish_accents(text)
    translated = translate_spanish_to_english(text)
    if is_unavailable_english_translation(translated):
        return ""
    normalized = " ".join(translated.split())
    if normalize_translation_lookup(normalized) == "sporadic":
        return ""
    if text.isupper():
        return normalized.title().replace(" Ia", " IA")
    return normalized


def sentence_case_heading(text: str) -> str:
    lowered = text.lower()
    if not lowered:
        return lowered
    return lowered[0].upper() + lowered[1:]


def bilingual_heading(
    text: str,
    size: int = 18,
    center: bool = True,
    show_english: bool = True,
) -> list[ft.Control]:
    text = restore_spanish_accents(text)
    heading_size = 15 if len(text) >= 14 else size
    english_heading = formatted_english_heading(text)
    return [
        ft.Text(
            text,
            size=heading_size,
            weight=ft.FontWeight.W_700,
            color=TEXT_DARK,
            text_align=ft.TextAlign.CENTER,
            width=300,
        ),
        ft.Text(
            english_heading,
            size=15,
            weight=ft.FontWeight.W_700,
            color=TEXT_DARK,
            italic=True,
            text_align=ft.TextAlign.CENTER,
            width=300,
            visible=show_english and bool(english_heading),
        ),
    ]


def kit_title_controls() -> list[ft.Control]:
    return [
        ft.Text(
            "KIT DE SUPERVIVENCIA",
            size=26,
            weight=ft.FontWeight.W_700,
            color=RED,
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Text(
            "Survival kit",
            size=15,
            weight=ft.FontWeight.W_700,
            color=RED,
            italic=True,
            text_align=ft.TextAlign.CENTER,
            width=300,
        ),
    ]


def bilingual_body_controls(body: str) -> list[ft.Control]:
    controls: list[ft.Control] = []
    parts = [part.strip() for part in body.split("\n\n") if part.strip()]

    for index, part in enumerate(parts):
        translated_part = translate_spanish_to_english(part)
        controls.append(
            ft.Text(
                part,
                size=15,
                color=TEXT_MUTED,
            )
        )
        if not is_unavailable_english_translation(translated_part):
            controls.append(
                ft.Text(
                    translated_part,
                    size=12,
                    color=TEXT_MUTED,
                    italic=True,
                )
            )
        if index < len(parts) - 1:
            controls.append(ft.Container(height=10))

    return controls


def spanish_survival_detail_options(situation_key: str) -> list[ft.dropdown.Option]:
    return [
        ft.dropdown.Option(
            key,
            f"{sentence_case_heading(data['title'])} / {formatted_english_heading(sentence_case_heading(data['title']))}",
        )
        for key, data in SPANISH_SURVIVAL_DETAILS[situation_key].items()
    ]


def spanish_survival_situation_options() -> list[ft.dropdown.Option]:
    preferred_order = [
        "restaurante",
        "jerga",
        "hospital",
        "farmacia",
        "hotel",
        "aeropuerto",
        "transporte",
        "ayuntamiento",
        "extranjeria",
        "servicios_sociales",
        "ong",
        "oficina_empleo",
        "academia_espanol",
        "entrevista",
        "guarderia",
        "casero",
        "visita_piso",
        "centro_salud",
        "correos",
        "supermercado",
        "tienda_ropa",
        "taxi",
        "comisaria",
        "colegio",
        "trabajo",
        "banco",
        "movil",
        "locutorio",
        "piso_compartido",
        "vecindario",
    ]
    return [
        ft.dropdown.Option(key, SPANISH_SURVIVAL_LABELS[key])
        for key in preferred_order
        if key in SPANISH_SURVIVAL_LABELS
    ]


def hero_button(text: str, on_click) -> ft.Button:
    text = restore_spanish_accents(text)
    return ft.Button(
        content=ft.Text(
            text,
            text_align=ft.TextAlign.CENTER,
            size=22,
            weight=ft.FontWeight.W_700,
            font_family=TITLE_FONT,
        ),
        on_click=on_click,
        width=300,
        height=110,
        style=ft.ButtonStyle(
            bgcolor="#FFFFFF",
            color=AMETHYST,
            padding=22,
            side=ft.BorderSide(3, AMETHYST),
            shape=ft.RoundedRectangleBorder(radius=24),
        ),
    )


def open_external_url(page: ft.Page, url: str) -> None:
    try:
        opened = webbrowser.open_new_tab(url)
        if not opened:
            page.launch_url(url)
    except Exception:
        page.launch_url(url)


TRANSLATION_CACHE: dict[str, str] = {}

MANUAL_TRANSLATIONS = {
    "KIT DE SUPERVIVENCIA": "Survival kit",
    "ADMINISTRATIVA": "Administrative help",
    "EMPADRONAMIENTO": "Address registration",
    "SEGURIDAD SOCIAL": "Social Security",
    "NIE / TIE": "NIE / TIE",
    "PRIMEROS PASOS": "First steps",
    "TRAMITES": "Procedures",
    "TRÁMITES": "Procedures",
    "SALUD": "Health",
    "TRANSPORTE": "Transport",
    "EMERGENCIAS": "Emergencies",
    "VIVIENDA": "Housing",
    "TRABAJO": "Work",
    "CONTRATO Y NÓMINA": "Contract and payslip",
    "DERECHOS BÁSICOS": "Basic rights",
    "PREGUNTAS FRECUENTES": "Frequently asked questions",
    "COMUNICACIÓN": "Communication",
    "INTEGRACIÓN": "Integration",
    "COMUNIDAD": "Community",
    "Información general de la Administración": "General public administration information",
    "Orientación general para trámites con la Administración": "General guidance for public administration procedures",
    "Información INSS": "INSS information",
    "Información INSS, puede tener coste según operador": "INSS information, call charges may apply",
    "Emergencias generales": "General emergencies",
    "Violencia contra las mujeres, 24 horas": "Violence against women, 24-hour helpline",
    "Policía Nacional": "National Police",
    "Guardia Civil": "Civil Guard",
    "Hazlo lo antes posible al llegar.": "Do it as soon as possible after arriving.",
    "Te sirve para centro de salud, colegio y otros tramites.": "You will need it for the health centre, school and other procedures.",
    "Lleva identificacion y justificante de domicilio.": "Bring identification and proof of address.",
    "Prepara pasaporte, formulario y cita previa.": "Prepare your passport, form and appointment.",
    "Revisa que la tasa este pagada antes de acudir.": "Check that the fee has been paid before you go.",
    "Guarda copia de todos tus documentos.": "Keep copies of all your documents.",
    "Pide tu numero de afiliacion si vas a trabajar.": "Request your Social Security number if you are going to work.",
    "Te lo pueden pedir para contrato o alta laboral.": "They may ask for it for your contract or job registration.",
    "Ten a mano tu documento de identidad y datos personales.": "Have your ID document and personal details ready.",
    (
        "Hazlo lo antes posible al llegar.\n\n"
        "Te sirve para centro de salud, colegio y otros tramites.\n\n"
        "Lleva identificacion y justificante de domicilio."
    ): (
        "Do it as soon as possible after arriving.\n\n"
        "You will need it for the health center, school and other procedures.\n\n"
        "Bring identification and proof of address."
    ),
    (
        "Prepara pasaporte, formulario y cita previa.\n\n"
        "Revisa que la tasa este pagada antes de acudir.\n\n"
        "Guarda copia de todos tus documentos."
    ): (
        "Prepare your passport, form and prior appointment.\n\n"
        "Check that the fee has been paid before you go.\n\n"
        "Keep copies of all your documents."
    ),
    (
        "Pide tu numero de afiliacion si vas a trabajar.\n\n"
        "Te lo pueden pedir para contrato o alta laboral.\n\n"
        "Ten a mano tu documento de identidad y datos personales."
    ): (
        "Request your Social Security number if you are going to work.\n\n"
        "They may ask for it for your contract or job registration.\n\n"
        "Have your ID document and personal details ready."
    ),
    (
        "Checklist paso a paso de los documentos que necesitas.\n\n"
        "Cómo pedir la cita previa.\n\n"
        "Cómo pagar las tasas del Modelo 790."
    ): (
        "Step-by-step checklist of the documents you need.\n\n"
        "How to book the appointment.\n\n"
        "How to pay the Model 790 fees."
    ),
    (
        "Explicación sencilla de qué es el empadronamiento.\n\n"
        "Por qué lo necesitas para ir al médico.\n\n"
        "Por qué es importante para escolarizar a los niños."
    ): (
        "A simple explanation of what local registration is.\n\n"
        "Why you need it to go to the doctor.\n\n"
        "Why it is important for enrolling children in school."
    ),
    (
        "Cómo obtener el número de afiliación.\n\n"
        "Qué necesitas para empezar a trabajar.\n\n"
        "Pasos básicos para tener tu situación en regla."
    ): (
        "How to get your Social Security number.\n\n"
        "What you need to start working.\n\n"
        "Basic steps to keep your situation in order."
    ),
    (
        "Frases útiles para urgencias y consultas.\n\n"
        "Ideal para explicar síntomas con claridad.\n\n"
        "Muy útil cuando estás nerviosa o nervioso."
    ): (
        "Useful phrases for emergencies and appointments.\n\n"
        "Ideal for explaining symptoms clearly.\n\n"
        "Very useful when you are nervous."
    ),
    (
        "Busca tu ambulatorio o centro de salud más cercano.\n\n"
        "Localiza urgencias, farmacias y hospitales.\n\n"
        "Ten siempre una referencia cerca de casa."
    ): (
        "Find your nearest clinic or health center.\n\n"
        "Locate emergency services, pharmacies and hospitals.\n\n"
        "Always keep a reference close to home."
    ),
    (
        "Infórmate de cómo pedir la tarjeta sanitaria en tu comunidad.\n\n"
        "Normalmente te pedirán empadronamiento y documentación.\n\n"
        "Es clave para acceder al sistema de salud."
    ): (
        "Find out how to apply for the health card in your region.\n\n"
        "They will usually ask for registration and documentation.\n\n"
        "It is key to accessing the health system."
    ),
    (
        "Consulta el bono que más te conviene según tu ciudad.\n\n"
        "Revisa opciones mensuales o por viajes.\n\n"
        "Suele salir más barato que comprar billetes sueltos."
    ): (
        "Check which pass suits you best depending on your city.\n\n"
        "Look at monthly or pay-per-trip options.\n\n"
        "It is usually cheaper than buying single tickets."
    ),
    (
        "Muchas ciudades tienen tarjetas recargables.\n\n"
        "Pregunta por descuentos para estudiantes o familias.\n\n"
        "Guarda siempre la tarjeta recargada."
    ): (
        "Many cities have rechargeable travel cards.\n\n"
        "Ask about discounts for students or families.\n\n"
        "Always keep the card topped up."
    ),
    (
        "Aprende las apps locales de transporte.\n\n"
        "Mira horarios, transbordos y estaciones principales.\n\n"
        "Te ayudara mucho durante los primeros dias."
    ): (
        "Learn the local transport apps.\n\n"
        "Check timetables, transfers and main stations.\n\n"
        "They will help you a lot during the first few days."
    ),
    (
        "El 112 es el numero general de emergencias en Espana.\n\n"
        "Usalo para urgencias medicas, policia o bomberos.\n\n"
        "Habla despacio y da datos concretos."
    ): (
        "112 is the general emergency number in Spain.\n\n"
        "Use it for medical emergencies, police or firefighters.\n\n"
        "Speak slowly and give clear details."
    ),
    (
        "Ten preparada tu direccion escrita correctamente.\n\n"
        "Incluye calle, numero, piso y ciudad.\n\n"
        "Eso ayuda mucho al operador en una urgencia."
    ): (
        "Have your address written down correctly.\n\n"
        "Include street, number, floor and city.\n\n"
        "This helps the operator a lot in an emergency."
    ),
    (
        "Guarda copia del pasaporte, NIE o TIE y telefono de contacto.\n\n"
        "Lleva una nota con alergias o medicacion importante.\n\n"
        "Tenerlo listo puede ahorrarte mucho tiempo."
    ): (
        "Keep a copy of your passport, NIE or TIE and a contact phone number.\n\n"
        "Carry a note with allergies or important medication.\n\n"
        "Having it ready can save you a lot of time."
    ),
    (
        "Antes de firmar, revisa precio, fianza y duracion del contrato.\n\n"
        "Pide siempre una copia del contrato.\n\n"
        "Pregunta si los gastos de luz, agua e internet estan incluidos."
    ): (
        "Before signing, check the price, deposit and contract length.\n\n"
        "Always ask for a copy of the contract.\n\n"
        "Ask whether electricity, water and internet bills are included."
    ),
    (
        "El padrón es clave para medico, colegio y muchos tramites.\n\n"
        "Pregunta al casero si necesitas autorizacion o contrato.\n\n"
        "Guarda recibos o documentos que prueben donde vives."
    ): (
        "Local registration is essential for healthcare, school and many procedures.\n\n"
        "Ask the landlord whether you need authorization or a contract.\n\n"
        "Keep receipts or documents that prove where you live."
    ),
    (
        "Comprueba a nombre de quien estan los suministros.\n\n"
        "Pregunta como se pagan y cada cuanto llegan las facturas.\n\n"
        "Ten a mano una compania de internet y un numero de telefono local."
    ): (
        "Check whose name the utilities are under.\n\n"
        "Ask how they are paid and how often the bills arrive.\n\n"
        "Keep an internet provider and a local phone number handy."
    ),
    (
        "Prepara un currículum sencillo y adaptado a Espana.\n\n"
        "Revisa si necesitas permiso de trabajo segun tu situacion.\n\n"
        "Ten listos telefono, correo y documentacion basica."
    ): (
        "Prepare a simple CV adapted to Spain.\n\n"
        "Check whether you need a work permit depending on your situation.\n\n"
        "Have your phone, email and basic documents ready."
    ),
    (
        "Lee bien horario, salario y tipo de contrato.\n\n"
        "Guarda copia del contrato y de cada nomina.\n\n"
        "Pregunta cualquier termino que no entiendas antes de firmar."
    ): (
        "Read the schedule, salary and type of contract carefully.\n\n"
        "Keep a copy of the contract and every payslip.\n\n"
        "Ask about any term you do not understand before signing."
    ),
    (
        "Tienes derecho a saber tus horarios, salario y condiciones.\n\n"
        "No entregues documentos originales sin necesidad.\n\n"
        "Si algo no esta claro, pide explicaciones por escrito."
    ): (
        "You have the right to know your schedule, salary and conditions.\n\n"
        "Do not hand over original documents unless necessary.\n\n"
        "If something is not clear, ask for an explanation in writing."
    ),
    "Estoy aprendiendo español.": "I am learning Spanish.",
    "Entiendo bastante, pero a veces necesito que hablen más despacio.": "I understand quite a lot, but sometimes I need people to speak more slowly.",
    "Sigo mejorando cada día.": "I am improving every day.",
    "EN URGENCIAS": "Emergency room",
    "MEDICACION": "Medication",
    "PROBLEMAS CON EL IDIOMA": "Language difficulties",
    "CITA o ADMISION": "Appointment or admissions",
    "ACOMPANANTE": "Companion",
    "NIE Y TIE": "NIE and TIE",
    "TASAS": "Fees",
    "RECOGIDA": "Collection",
    "HUELLAS": "Fingerprints",
    "RESGUARDO": "Receipt",
    "PEDIR INFORMACION": "Ask for information",
    "DOCUMENTOS": "Documents",
    "PADRON": "Registration",
    "CERTIFICADOS": "Certificates",
    "TASAS MUNICIPALES": "Local fees",
    "PEDIR CITA": "Book an appointment",
    "EN CONSULTA": "At the appointment",
    "IDIOMA": "Language",
    "TARJETA SANITARIA": "Health card",
    "ESPECIALISTA": "Specialist",
    "TAREAS": "Tasks",
    "HORARIOS": "Working hours",
    "RECURSOS HUMANOS": "Human resources",
    "NOMINA": "Payslip",
    "VACACIONES o AUSENCIAS": "Leave or absences",
    "Necesito ayuda, me encuentro muy mal.": "I need help, I feel very unwell.",
    "Me duele aqui.": "It hurts here.",
    "Tengo fiebre desde ayer.": "I have had a fever since yesterday.",
    "Soy alergica o alergico a este medicamento.": "I am allergic to this medicine.",
    "Tomo esta medicacion.": "I take this medication.",
    "Como tengo que tomarlo?": "How should I take it?",
    "No hablo bien espanol.": "I do not speak Spanish well.",
    "Puede hablar mas despacio?": "Could you speak more slowly?",
    "Necesito un traductor, por favor.": "I need an interpreter, please.",
    "Tengo cita para hoy.": "I have an appointment today.",
    "Donde tengo que ir?": "Where do I need to go?",
    "Que documento necesita?": "Which document do you need?",
    "Puede pasar conmigo?": "Can they come in with me?",
    "Necesito ayuda para entender.": "I need help understanding.",
    "Puede esperar aqui, por favor?": "Can you wait here, please?",
    "Vengo por el NIE o la TIE.": "I am here for the NIE or TIE.",
    "Tengo cita para este tramite.": "I have an appointment for this procedure.",
    "Me falta algun documento?": "Am I missing any documents?",
    "Donde pago la tasa?": "Where do I pay the fee?",
    "Que modelo tengo que pagar?": "Which form do I need to pay?",
    "Tengo que traer el justificante impreso?": "Do I need to bring the printed receipt?",
    "Cuando puedo volver a recogerlo?": "When can I come back to collect it?",
    "Necesito otra cita?": "Do I need another appointment?",
    "Que tengo que traer ese dia?": "What do I need to bring that day?",
    "Vengo para poner las huellas.": "I am here to give my fingerprints.",
    "Necesito foto o formulario?": "Do I need a photo or a form?",
    "Necesito un resguardo.": "I need a receipt.",
    "Este documento sirve mientras espero?": "Is this document valid while I wait?",
    "Me lo puede sellar, por favor?": "Could you stamp it for me, please?",
    "Quiero informacion sobre este tramite.": "I want information about this procedure.",
    "Necesito cita previa?": "Do I need an appointment?",
    "Donde esta la oficina correcta?": "Where is the correct office?",
    "Que documentos tengo que traer?": "What documents do I need to bring?",
    "Me falta algo?": "Am I missing anything?",
    "Necesito una copia de este formulario.": "I need a copy of this form.",
    "Quiero empadronarme.": "I want to register my address.",
    "Necesito cita para el padron?": "Do I need an appointment for registration?",
    "Cuanto tarda este tramite?": "How long does this procedure take?",
    "Necesito un certificado.": "I need a certificate.",
    "Donde lo solicito?": "Where do I request it?",
    "Cuando puedo recogerlo?": "When can I collect it?",
    "Donde pago esta tasa?": "Where do I pay this fee?",
    "Puedo pagar con tarjeta?": "Can I pay by card?",
    "Necesito justificante?": "Do I need a receipt?",
    "Quiero pedir una cita medica.": "I want to book a medical appointment.",
    "Es urgente?": "Is it urgent?",
    "Para cuando hay cita disponible?": "When is the next appointment available?",
    "Me encuentro mal desde ayer.": "I have been feeling unwell since yesterday.",
    "Necesito una receta, por favor.": "I need a prescription, please.",
    "Puede escribirlo, por favor?": "Could you write it down, please?",
    "Quiero informacion sobre la tarjeta sanitaria.": "I want information about the health card.",
    "Que documentos necesito?": "What documents do I need?",
    "Donde hago este tramite?": "Where do I do this procedure?",
    "Necesito cita con un especialista.": "I need an appointment with a specialist.",
    "Me pueden derivar?": "Can you refer me?",
    "Cuando recibire la cita?": "When will I receive the appointment?",
    "No entiendo esta tarea.": "I do not understand this task.",
    "Puede explicarmelo otra vez?": "Could you explain it to me again?",
    "Me lo puede escribir, por favor?": "Could you write it down for me, please?",
    "A que hora empieza el turno?": "What time does the shift start?",
    "Cuando es el descanso?": "When is the break?",
    "Mañana trabajo tambien?": "Am I working tomorrow as well?",
    "Necesito hablar con recursos humanos.": "I need to speak with human resources.",
    "Tengo una duda sobre mi contrato.": "I have a question about my contract.",
    "Tengo una duda sobre mi nomina.": "I have a question about my payslip.",
    "Falta una hora aqui.": "One hour is missing here.",
    "Me lo puede explicar?": "Could you explain it to me?",
    "Quiero pedir vacaciones.": "I would like to request leave.",
    "Necesito ausentarme este dia.": "I need to be absent that day.",
    "Con quien tengo que hablar?": "Who do I need to speak with?",
    "DOLOR Y FIEBRE": "Pain and fever",
    "TOS Y RESFRIADO": "Cough and cold",
    "RECETA": "Prescription",
    "PIEL o HERIDAS": "Skin or wounds",
    "MEDICINAS PARA NINOS": "Medicine for children",
    "DENUNCIA": "Police report",
    "CITA PREVIA": "Appointment",
    "DOCUMENTACION": "Documentation",
    "ABRIR CUENTA": "Open an account",
    "TARJETA": "Card",
    "DINERO": "Money",
    "TRANSFERENCIAS": "Transfers",
    "APP Y CLAVES": "App and passwords",
    "CITA EN EL BANCO": "Bank appointment",
    "ALQUILER": "Renting",
    "CONTRATO": "Contract",
    "EMPADRONAMIENTO": "Address registration",
    "AVERIAS": "Repairs",
    "FACTURAS Y GASTOS": "Bills and expenses",
    "DEMANDA DE EMPLEO": "Job seeker registration",
    "CURSOS": "Courses",
    "OFERTAS DE TRABAJO": "Job offers",
    "Necesito algo para el dolor.": "I need something for pain.",
    "Tiene algo para la fiebre?": "Do you have something for fever?",
    "Tiene algo para la tos?": "Do you have something for a cough?",
    "Estoy resfriada o resfriado.": "I have a cold.",
    "Necesito algo para la garganta.": "I need something for my throat.",
    "Hace falta receta?": "Do I need a prescription?",
    "Tengo una receta del medico.": "I have a prescription from the doctor.",
    "Puede explicarme como usarlo?": "Can you explain how to use it?",
    "Necesito una crema para esta herida.": "I need a cream for this wound.",
    "Tiene algo para una quemadura?": "Do you have something for a burn?",
    "Esto pica mucho.": "This itches a lot.",
    "Es para un nino o una nina.": "It is for a child.",
    "Cuanta cantidad tengo que darle?": "How much should I give them?",
    "Tiene jarabe infantil?": "Do you have children's syrup?",
    "Quiero poner una denuncia.": "I want to file a police report.",
    "He perdido mi documentacion.": "I have lost my documents.",
    "Me han robado la cartera.": "My wallet has been stolen.",
    "Necesito ayuda.": "I need help.",
    "No se que tengo que hacer.": "I do not know what I need to do.",
    "Puede explicarmelo mas despacio?": "Could you explain it more slowly?",
    "Tengo cita previa.": "I have an appointment.",
    "Vengo para este tramite.": "I am here for this procedure.",
    "Donde tengo que esperar?": "Where do I need to wait?",
    "He perdido mi pasaporte.": "I have lost my passport.",
    "Necesito un justificante.": "I need a receipt.",
    "Que tengo que hacer ahora?": "What do I need to do now?",
    "Quiero abrir una cuenta.": "I want to open an account.",
    "Hay comisiones?": "Are there any fees?",
    "Tengo un problema con mi tarjeta.": "I have a problem with my card.",
    "No funciona.": "It is not working.",
    "Quiero pedir una nueva.": "I want to request a new one.",
    "Quiero sacar dinero.": "I want to withdraw money.",
    "Quiero ingresar dinero.": "I want to deposit money.",
    "Puede ayudarme, por favor?": "Can you help me, please?",
    "Quiero hacer una transferencia.": "I want to make a transfer.",
    "Cuanto tarda en llegar?": "How long does it take to arrive?",
    "Necesito el IBAN.": "I need the IBAN.",
    "No puedo entrar en la app.": "I cannot log into the app.",
    "He olvidado mi clave.": "I have forgotten my password.",
    "Puede ayudarme a activarla?": "Can you help me activate it?",
    "Quiero pedir una cita.": "I want to book an appointment.",
    "Necesito hablar con un gestor.": "I need to speak with an adviser.",
    "Cuando pueden atenderme?": "When can you see me?",
    "Estoy interesada o interesado en alquilar esta vivienda.": "I am interested in renting this home.",
    "Que incluye el precio?": "What is included in the price?",
    "Cuanto es la fianza?": "How much is the deposit?",
    "Necesito una copia del contrato.": "I need a copy of the contract.",
    "Cuanto dura el contrato?": "How long does the contract last?",
    "Cuando se paga cada mes?": "When is the rent paid each month?",
    "Puedo empadronarme aqui?": "Can I register my address here?",
    "Necesito una autorizacion suya?": "Do I need your authorization?",
    "Me puede firmar este documento?": "Can you sign this document for me?",
    "No funciona la calefaccion.": "The heating is not working.",
    "Hay una fuga de agua.": "There is a water leak.",
    "Puede venir alguien a arreglarlo?": "Can someone come and fix it?",
    "Quien paga la luz y el agua?": "Who pays for electricity and water?",
    "Internet esta incluido?": "Is internet included?",
    "Cuando llegan las facturas?": "When do the bills arrive?",
    "Quiero apuntarme como demandante de empleo.": "I want to register as a job seeker.",
    "Qué documentos necesito?": "What documents do I need?",
    "Hay cursos de formación?": "Are there training courses?",
    "Quiero mejorar mi español para trabajar.": "I want to improve my Spanish for work.",
    "Cómo me apunto?": "How do I sign up?",
    "Estoy buscando trabajo.": "I am looking for work.",
    "Hay ofertas para este perfil?": "Are there job offers for this profile?",
    "Puede orientarme, por favor?": "Can you advise me, please?",
    "Vengo para este trámite.": "I am here for this procedure.",
    "Dónde tengo que esperar?": "Where do I need to wait?",
    "BILLETES": "Tickets",
    "RUTA": "Route",
    "BONOS": "Travel passes",
    "ANDENES Y PARADAS": "Platforms and stops",
    "INCIDENCIAS": "Disruptions",
    "BUSCAR PRODUCTOS": "Find products",
    "PAGAR": "Pay",
    "PRECIO": "Price",
    "DEVOLUCIONES": "Returns",
    "INGREDIENTES": "Ingredients",
    "MATRICULA": "Enrollment",
    "SECRETARIA": "School office",
    "COMEDOR ESCOLAR": "School canteen",
    "TUTOR o PROFESORADO": "Tutor or teachers",
    "ENVIAR UN PAQUETE": "Send a parcel",
    "CARTA CERTIFICADA": "Registered letter",
    "RECOGER UN ENVIO": "Collect a delivery",
    "SOBRES Y CAJAS": "Envelopes and boxes",
    "SEGUIMIENTO": "Tracking",
    "APARTADO POSTAL": "PO box",
    "SELLOS": "Stamps",
    "ENVIO INTERNACIONAL": "International shipping",
    "TARJETA SIM": "SIM card",
    "INTERNET Y DATOS": "Internet and data",
    "RECARGAS": "Top-ups",
    "AVERIA o BLOQUEO": "Fault or lockout",
    "Donde compro el billete?": "Where do I buy the ticket?",
    "Cuanto cuesta?": "How much does it cost?",
    "Aceptan tarjeta?": "Do you take card?",
    "Este autobus va al centro?": "Does this bus go to the city centre?",
    "En que parada bajo?": "Which stop do I get off at?",
    "Tengo que hacer transbordo?": "Do I need to change?",
    "Que bono me conviene?": "Which pass suits me best?",
    "Cuanto cuesta el bono mensual?": "How much is the monthly pass?",
    "Donde puedo recargarlo?": "Where can I top it up?",
    "De que anden sale?": "Which platform does it leave from?",
    "Esta es la parada correcta?": "Is this the right stop?",
    "Cuanto falta para que llegue?": "How long until it arrives?",
    "Hay retraso?": "Is it delayed?",
    "Este tren no circula hoy?": "Is this train not running today?",
    "Que alternativa tengo?": "What alternative do I have?",
    "Donde esta la leche?": "Where is the milk?",
    "Donde estan los huevos?": "Where are the eggs?",
    "Tiene este producto sin gluten?": "Do you have this product gluten-free?",
    "Quiero pagar, por favor.": "I would like to pay, please.",
    "Tiene bolsa?": "Do you have a bag?",
    "Cuanto cuesta esto?": "How much is this?",
    "Hay oferta?": "Is it on offer?",
    "Este precio es por kilo?": "Is this price per kilo?",
    "Quiero devolver este producto.": "I want to return this product.",
    "Tengo el ticket.": "I have the receipt.",
    "Me devuelven el dinero o un vale?": "Do I get a refund or a store voucher?",
    "Donde puedo ver los ingredientes?": "Where can I see the ingredients?",
    "Esto lleva cerdo?": "Does this contain pork?",
    "Es apto para vegetarianos?": "Is it suitable for vegetarians?",
    "Quiero informacion para matricular a mi hijo o hija.": "I would like information about enrolling my child.",
    "Hay plazas disponibles?": "Are there places available?",
    "A que hora empieza la clase?": "What time does class start?",
    "A que hora termina?": "What time does it finish?",
    "Hay comedor escolar?": "Is there a school canteen?",
    "Donde esta la secretaria?": "Where is the school office?",
    "Necesito entregar estos documentos.": "I need to hand in these documents.",
    "Mi hijo o hija tiene alergias.": "My child has allergies.",
    "Quiero hablar con el tutor.": "I would like to speak with the tutor.",
    "Cuando puedo tener una reunion?": "When can I have a meeting?",
    "Como va mi hijo o hija en clase?": "How is my child doing in class?",
    "Quiero enviar este paquete.": "I want to send this parcel.",
    "Cuando llegara?": "When will it arrive?",
    "Quiero enviar una carta certificada.": "I want to send a registered letter.",
    "Necesito un sobre grande.": "I need a large envelope.",
    "Me da el justificante, por favor?": "Can you give me the receipt, please?",
    "Vengo a recoger este envio.": "I am here to collect this delivery.",
    "Tengo este aviso.": "I have this collection notice.",
    "Necesito enseñar el pasaporte?": "Do I need to show my passport?",
    "Necesito una caja mediana.": "I need a medium-sized box.",
    "Tiene sobres acolchados?": "Do you have padded envelopes?",
    "Cual me recomienda para esto?": "Which one do you recommend for this?",
    "Quiero saber donde esta mi paquete.": "I want to know where my parcel is.",
    "Este es el numero de seguimiento.": "This is the tracking number.",
    "Ha habido algun problema con la entrega?": "Has there been any problem with the delivery?",
    "Quiero devolver este paquete.": "I want to return this parcel.",
    "Necesito imprimir una etiqueta?": "Do I need to print a label?",
    "Donde lo dejo?": "Where do I leave it?",
    "Quiero informacion sobre un apartado postal.": "I want information about a PO box.",
    "Necesito sellos.": "I need stamps.",
    "Cuantos necesito para esta carta?": "How many do I need for this letter?",
    "Sirven para envio internacional?": "Are they valid for international shipping?",
    "Quiero enviar este paquete a otro pais.": "I want to send this parcel to another country.",
    "Cuanto tarda?": "How long does it take?",
    "Necesito rellenar algun formulario?": "Do I need to fill in any form?",
    "Quiero una tarjeta SIM.": "I want a SIM card.",
    "Que necesito para comprarla?": "What do I need to buy it?",
    "La quiero prepago.": "I want it prepaid.",
    "Necesito internet en el movil.": "I need internet on my phone.",
    "Cuantos gigas incluye?": "How many gigabytes does it include?",
    "Hay permanencia?": "Is there a minimum contract period?",
    "Quiero recargar mi linea.": "I want to top up my line.",
    "Ya se ha hecho la recarga?": "Has the top-up gone through?",
    "Mi movil no funciona.": "My phone is not working.",
    "No tengo cobertura.": "I have no signal.",
    "Puede ayudarme a configurarlo?": "Can you help me set it up?",
    "PEDIR MESA": "Ask for a table",
    "PEDIR COMIDA": "Order food",
    "PEDIR LA CUENTA": "Ask for the bill",
    "ALERGIAS o INTOLERANCIAS": "Allergies or intolerances",
    "RESERVA": "Reservation",
    "MENU DEL DIA": "Set menu",
    "PARA LLEVAR": "Takeaway",
    "PROBLEMAS EN LA HABITACION": "Room problems",
    "SERVICIOS": "Services",
    "CHECK-OUT": "Check-out",
    "INDICAR DESTINO": "Give destination",
    "TIEMPO Y RUTA": "Time and route",
    "EQUIPAJE": "Luggage",
    "RECIBO": "Receipt",
    "IMPRIMIR DOCUMENTOS": "Print documents",
    "FOTOCOPIAS": "Photocopies",
    "CORREO ELECTRONICO": "Email",
    "USAR INTERNET": "Use internet",
    "PLAZA": "Place",
    "CONDICIONES": "Conditions",
    "SUMINISTROS": "Utilities",
    "ORIENTACION": "Guidance",
    "AYUDAS": "Support",
    "VIVIENDA": "Housing",
    "TRAMITES": "Procedures",
    "CURSOS Y NIVELES": "Courses and levels",
    "FACTURACION": "Check-in desk",
    "EMBARQUE": "Boarding",
    "CONTROLES": "Security checks",
    "PRESENTARSE": "Introduce yourself",
    "PEDIR AYUDA": "Ask for help",
    "RUIDOS o MOLESTIAS": "Noise or disturbance",
    "BASURA Y RECICLAJE": "Waste and recycling",
    "BUSCAR HABITACION": "Find a room",
    "GASTOS": "Expenses",
    "CONVIVENCIA": "Living together",
    "ENTRADA": "Move-in",
    "Hola, una mesa para dos, por favor.": "Hello, a table for two, please.",
    "Tenemos reserva a nombre de...": "We have a reservation under the name...",
    "Podemos sentarnos aqui?": "Can we sit here?",
    "Que me recomienda?": "What do you recommend?",
    "Quiero esto, por favor.": "I would like this, please.",
    "Sin gluten, por favor.": "Gluten-free, please.",
    "La cuenta, por favor.": "The bill, please.",
    "Muchas gracias, estaba todo muy bueno.": "Thank you very much, everything was very good.",
    "Soy alergica o alergico a...": "I am allergic to...",
    "Esto lleva leche o frutos secos?": "Does this contain milk or nuts?",
    "Necesito comida sin gluten.": "I need gluten-free food.",
    "Quiero hacer una reserva.": "I would like to make a reservation.",
    "Para cuantas personas?": "For how many people?",
    "A que hora tienen mesa libre?": "What time do you have a free table?",
    "Tienen menu del dia?": "Do you have a set menu?",
    "Que incluye?": "What does it include?",
    "Hay opcion vegetariana?": "Is there a vegetarian option?",
    "Lo quiero para llevar.": "I would like it to take away.",
    "Puede ponerlo separado?": "Can you pack it separately?",
    "Necesito cubiertos, por favor.": "I need cutlery, please.",
    "CHECK-IN": "Check-in",
    "PAGO": "Payment",
    "Tengo una reserva a nombre de...": "I have a reservation under the name...",
    "A que hora es el check-in?": "What time is check-in?",
    "Necesito mi pasaporte?": "Do I need my passport?",
    "No funciona el aire acondicionado.": "The air conditioning is not working.",
    "Necesito toallas limpias.": "I need clean towels.",
    "La habitacion no esta lista.": "The room is not ready.",
    "Puede llamar un taxi?": "Can you call a taxi?",
    "A que hora es el desayuno?": "What time is breakfast?",
    "Hay wifi gratis?": "Is there free Wi-Fi?",
    "A que hora tengo que dejar la habitacion?": "What time do I need to leave the room?",
    "Puedo salir mas tarde?": "Can I check out later?",
    "Donde dejo la llave?": "Where do I leave the key?",
    "Quiero pagar ahora.": "I would like to pay now.",
    "Me da la factura, por favor?": "Can you give me the invoice, please?",
    "Lleveme a esta direccion, por favor.": "Please take me to this address.",
    "Es aqui.": "It is here.",
    "Puede parar en esta calle?": "Can you stop on this street?",
    "Cuanto tarda mas o menos?": "How long does it take roughly?",
    "Hay mucho trafico?": "Is there much traffic?",
    "Puede ir por la ruta mas rapida?": "Can you take the fastest route?",
    "Cuanto es?": "How much is it?",
    "Gracias, buen dia.": "Thank you, have a good day.",
    "Llevo una maleta grande.": "I have a large suitcase.",
    "Puede abrir el maletero?": "Can you open the boot?",
    "Ayudeme con el equipaje, por favor.": "Please help me with the luggage.",
    "Me da un recibo, por favor?": "Can you give me a receipt, please?",
    "Lo necesito para el trabajo.": "I need it for work.",
    "Puede poner la fecha?": "Can you put the date on it?",
    "Quiero imprimir este documento.": "I want to print this document.",
    "Cuanto cuesta por pagina?": "How much is it per page?",
    "Puede imprimirlo en color?": "Can you print it in colour?",
    "Necesito una fotocopia del pasaporte.": "I need a photocopy of my passport.",
    "Quiero dos copias, por favor.": "I would like two copies, please.",
    "Tambien necesito escanearlo.": "I also need to scan it.",
    "Necesito enviar este correo.": "I need to send this email.",
    "Puedo adjuntar un documento?": "Can I attach a document?",
    "Puede ayudarme a escribirlo?": "Can you help me write it?",
    "Quiero usar un ordenador.": "I would like to use a computer.",
    "Cuanto cuesta media hora?": "How much is half an hour?",
    "Necesito entrar en esta pagina.": "I need to access this page.",
    "Busco plaza para mi hijo o hija.": "I am looking for a place for my child.",
    "¿Tienen plazas disponibles?": "Do you have places available?",
    "¿Desde qué edad aceptan niños?": "From what age do you accept children?",
    "¿Qué documentos necesito?": "What documents do I need?",
    "¿Hace falta empadronamiento?": "Is address registration required?",
    "¿Tengo que pedir cita?": "Do I need to book an appointment?",
    "¿Qué horario tienen?": "What are your opening hours?",
    "¿Abren por la mañana?": "Are you open in the morning?",
    "¿Hay servicio de comedor?": "Is there a meal service?",
    "¿Cuánto cuesta?": "How much does it cost?",
    "¿Hay ayudas o descuentos?": "Are there any grants or discounts?",
    "¿Cómo se paga?": "How do you pay?",
    "¿Cuánto cuesta al mes?": "How much is it per month?",
    "¿La fianza está incluida?": "Is the deposit included?",
    "¿Qué gastos se pagan aparte?": "Which expenses are paid separately?",
    "¿Puedo empadronarme aquí?": "Can I register my address here?",
    "¿Lo pondrían en el contrato?": "Would you put that in the contract?",
    "¿Necesito autorización del propietario?": "Do I need the landlord's authorisation?",
    "¿Se puede entrar este mes?": "Can I move in this month?",
    "¿Aceptan familias o niños?": "Do you accept families or children?",
    "¿Incluye luz, agua o internet?": "Does it include electricity, water or internet?",
    "¿A nombre de quién están?": "Whose name are they under?",
    "¿Cuánto se paga normalmente?": "How much is usually paid?",
    "Acabo de llegar y no sé por dónde empezar.": "I have just arrived and I do not know where to start.",
    "Necesito orientación.": "I need guidance.",
    "Qué pasos me recomienda hacer primero?": "Which steps do you recommend I take first?",
    "Quiero información sobre ayudas.": "I would like information about support.",
    "Hay apoyo para vivienda o alimentos?": "Is there support for housing or food?",
    "Qué requisitos hay?": "What are the requirements?",
    "Necesito ayuda para encontrar vivienda.": "I need help finding housing.",
    "Estoy en una situación difícil.": "I am in a difficult situation.",
    "Qué documentos debo traer?": "What documents should I bring?",
    "Acabo de llegar a España.": "I have just arrived in Spain.",
    "¿Pueden ayudarme, por favor?": "Can you help me, please?",
    "Necesito ayuda con mis trámites.": "I need help with my paperwork.",
    "No entiendo bien este documento.": "I do not understand this document well.",
    "¿Me lo pueden explicar?": "Can you explain it to me?",
    "Busco ayuda con vivienda.": "I am looking for help with housing.",
    "¿Conocen algún recurso?": "Do you know of any support service?",
    "Vengo a pedir información.": "I am here to ask for information.",
    "Quiero aprender español.": "I want to learn Spanish.",
    "¿Tienen cursos para principiantes?": "Do you have courses for beginners?",
    "¿Qué nivel me recomiendan?": "Which level do you recommend?",
    "Trabajo por las mañanas.": "I work in the mornings.",
    "¿Hay clases por la tarde?": "Are there classes in the afternoon?",
    "¿Cuánto cuesta el curso?": "How much does the course cost?",
    "¿Se paga al mes?": "Is it paid monthly?",
    "¿Hay descuento?": "Is there any discount?",
    "Quiero apuntarme.": "I would like to sign up.",
    "¿Cuándo empieza el curso?": "When does the course start?",
    "Donde facturo esta maleta?": "Where do I check in this suitcase?",
    "Cuanto equipaje puedo llevar?": "How much luggage can I take?",
    "Necesito imprimir la tarjeta de embarque?": "Do I need to print the boarding pass?",
    "De que puerta sale el vuelo?": "Which gate does the flight leave from?",
    "A que hora empieza el embarque?": "What time does boarding start?",
    "Voy bien para esta terminal?": "Am I going the right way for this terminal?",
    "Donde recojo mi maleta?": "Where do I collect my suitcase?",
    "Mi maleta no ha llegado.": "My suitcase has not arrived.",
    "Donde puedo poner una reclamacion?": "Where can I file a complaint?",
    "Que tengo que sacar de la mochila?": "What do I need to take out of my bag?",
    "Puedo pasar con esto?": "Can I go through with this?",
    "Donde esta el control de pasaportes?": "Where is passport control?",
    "Sabe donde esta el centro de salud?": "Do you know where the health centre is?",
    "Donde esta el supermercado mas cercano?": "Where is the nearest supermarket?",
    "Que autobus va al centro?": "Which bus goes to the city centre?",
    "Perdon por las molestias.": "Sorry for the disturbance.",
    "Hay mucho ruido esta noche.": "There is a lot of noise tonight.",
    "Puede bajar la musica, por favor?": "Could you turn the music down, please?",
    "Que dia pasan a recoger la basura?": "What day is the rubbish collected?",
    "Donde estan los contenedores?": "Where are the bins?",
    "Donde se recicla el vidrio?": "Where do I recycle glass?",
    "Estoy buscando una habitacion.": "I am looking for a room.",
    "Esta disponible?": "Is it available?",
    "Los gastos estan incluidos?": "Are the bills included?",
    "Cuanto se paga de luz y agua?": "How much is paid for electricity and water?",
    "Internet va aparte?": "Is internet paid separately?",
    "A que hora se puede usar la cocina?": "What time can the kitchen be used?",
    "Hay normas de la casa?": "Are there house rules?",
    "Cuantas personas viven aqui?": "How many people live here?",
    "Cuando podria entrar a vivir?": "When could I move in?",
    "Hay que pagar fianza?": "Is there a deposit to pay?",
    "Hay contrato?": "Is there a contract?",
    "JERGA Y EXPRESIONES": "Slang and real-life expressions",
    "EXPRESIONES COTIDIANAS": "Everyday expressions",
    "PLANES y AMBIENTE": "Plans and social vibe",
    "NO SE TRADUCE LITERAL": "Not translated literally",
    "TRABAJO y CALLE": "Work and everyday street talk",
    "COMPORTAMIENTO y COSTUMBRES": "Behaviour and customs",
    "CÓDIGOS SOCIALES Y COSTUMBRES": "Social customs and codes",
    "SALUDOS y CERCANÍA": "Greetings and closeness",
    "TURNOS y COLAS": "Queues and turns",
    "TÚ o USTED": "Tu or usted",
    "HORARIOS y COSTUMBRES": "Schedules and customs",
    "VISITAS y CASA": "Visits and home",
    "BARES y RESTAURANTES": "Bars and restaurants",
    "TRABAJO y TRATO": "Work and social tone",
    "CONVERSACIÓN y TEMAS": "Conversation and topics",
    "Saluda al entrar en una tienda o consulta.\n\nRespeta turnos y colas.\n\nObserva si conviene usar tú o usted.\n\nTen en cuenta que los horarios pueden ser más tarde.\n\nMira primero cómo actúan los demás.": "Say hello when entering a shop or appointment.\n\nRespect queues and turns.\n\nNotice whether it is better to use tú or usted.\n\nKeep in mind that schedules may be later.\n\nWatch first how other people behave.",
    "Es habitual saludar al entrar en una tienda, consulta o ascensor.\n\nUn hola o buenos días suele marcar buena educación.\n\nTambién es normal despedirse al salir.": "It is common to greet people when entering a shop, clinic or lift.\n\nA hello or good morning is usually seen as polite.\n\nIt is also normal to say goodbye when leaving.",
    "Respeta el turno y la cola aunque parezca informal.\n\nSi no sabes quién va antes, pregunta con educación.\n\nColarse suele sentar mal.": "Respect the turn and the queue even if it looks informal.\n\nIf you are not sure who is next, ask politely.\n\nJumping the queue is usually frowned upon.",
    "En muchos contextos cotidianos se usa tú.\n\nEn trámites, salud o con personas mayores conviene empezar con más cortesía.\n\nLuego puedes adaptarte al tono de la otra persona.": "In many everyday situations people use tú.\n\nFor paperwork, healthcare or older people, it is better to start more politely.\n\nThen you can adapt to the other person's tone.",
    "Comer y cenar puede ser más tarde que en otros países.\n\nAlgunas tiendas cierran al mediodía.\n\nObservar primero cómo funciona el entorno ayuda mucho.": "Lunch and dinner can be later than in other countries.\n\nSome shops close at midday.\n\nWatching first how the environment works helps a lot.",
    "Si vas a casa de alguien, suele valorarse avisar antes.\n\nLlegar muchísimo antes de la hora puede resultar incómodo.\n\nA veces se lleva un detalle pequeño, pero no siempre es obligatorio.": "If you go to someone's home, it is usually appreciated if you let them know first.\n\nArriving far too early can feel awkward.\n\nSometimes people bring a small gift, but it is not always necessary.",
    "En sitios informales a veces se pide en barra y otras en mesa; conviene observar primero.\n\nNo siempre se deja propina, y si se deja suele ser pequeña.\n\nPedir con un por favor y dar las gracias se valora mucho.": "In informal places, sometimes you order at the bar and other times at the table; it is best to watch first.\n\nTipping is not always expected, and when it is, it is usually small.\n\nAsking with a please and saying thank you is appreciated a lot.",
    "Conviene observar si el ambiente es formal o cercano antes de coger confianza.\n\nInterrumpir mucho o hablar encima de otra persona suele sentar mal.\n\nSer amable, claro y puntual ayuda mucho en el trabajo.": "It helps to notice whether the environment is formal or friendly before becoming too familiar.\n\nInterrupting a lot or talking over someone is usually frowned upon.\n\nBeing kind, clear and punctual helps a lot at work.",
    "Al principio es mejor evitar preguntas demasiado íntimas si no hay confianza.\n\nEl tono puede ser cercano, pero eso no siempre significa mucha confianza real.\n\nEscuchar primero ayuda a entender mejor el estilo de cada persona.": "At first, it is better to avoid very personal questions if there is no trust yet.\n\nThe tone may feel friendly, but that does not always mean real closeness.\n\nListening first helps you understand each person's style better.",
    "No me comas la cabeza.\n\nMe da vergüenza ajena.\n\nVamos de tapeo.\n\nEstoy desvelada o desvelado.\n\nVoy a estrenar esta chaqueta.": "Don't do my head in.\n\nThat gives me second-hand embarrassment.\n\nWe're going out for tapas.\n\nI couldn't sleep and now I'm wide awake.\n\nI'm going to wear this jacket for the first time.",
    "No me comas la cabeza.\n\nMe da vergüenza ajena.\n\nEstoy a tope hoy.": "Don't do my head in.\n\nThat gives me second-hand embarrassment.\n\nI'm swamped today.",
    "Vamos de tapeo.\n\nHay muy buen rollo.\n\nEse sitio está muy guay.": "We're going out for tapas.\n\nThe vibe is really good.\n\nThat place is really cool.",
    "Estoy desvelada o desvelado.\n\nVoy a estrenar esta chaqueta.\n\nHoy hubo mucha sobremesa.": "I couldn't sleep and now I'm wide awake.\n\nI'm going to wear this jacket for the first time.\n\nWe spent a long time chatting after the meal today.",
    "Voy pillada o pillado de tiempo.\n\nEsto me viene fatal hoy.\n\nTe aviso ahora mismo.": "I'm really short on time.\n\nThis is really bad for me today.\n\nI'll let you know right away.",
    "Observa primero si se pide en mesa o en barra.\n\nPedir con por favor y dar las gracias se valora mucho.\n\nLa propina no siempre es obligatoria; si se deja, suele ser pequeña.": "Watch first whether people order at the table or at the bar.\n\nUsing please and saying thank you is appreciated a lot.\n\nTipping is not always expected; if you do tip, it is usually small.",
    "No me comas la cabeza.": "Don't do my head in.",
    "Me da vergüenza ajena.": "That gives me second-hand embarrassment.",
    "Estoy a tope hoy.": "I'm swamped today.",
    "Vamos de tapeo.": "We're going out for tapas.",
    "Hay muy buen rollo.": "The vibe is really good.",
    "Ese sitio está muy guay.": "That place is really cool.",
    "Estoy desvelada o desvelado.": "I couldn't sleep and now I'm wide awake.",
    "Voy a estrenar esta chaqueta.": "I'm going to wear this jacket for the first time.",
    "Hoy hubo mucha sobremesa.": "We spent a long time chatting after the meal today.",
    "Voy pillada o pillado de tiempo.": "I'm really short on time.",
    "Esto me viene fatal hoy.": "This is really bad for me today.",
    "Te aviso ahora mismo.": "I'll let you know right away.",
    "Saluda al entrar en una tienda, consulta o ascensor; se percibe como cercanía y educación.\n\nRespeta turnos y colas, y pregunta antes de pasar si no tienes claro quién va primero.\n\nEn contextos informales suele usarse tú, pero en trámites, salud o con personas mayores conviene empezar con más cortesía.\n\nLos horarios pueden ser distintos: comer y cenar suele ser más tarde que en otros países.\n\nObservar primero cómo hablan y se relacionan otras personas ayuda mucho a integrarte.": "Say hello when entering a shop, clinic or lift; it is usually seen as polite and friendly.\n\nRespect queues and turns, and ask before stepping ahead if you are not sure who is next.\n\nIn informal settings people often use tú, but for paperwork, healthcare or older people it is better to start more politely.\n\nMeal times can be different: lunch and dinner are often later than in other countries.\n\nWatching first how other people speak and relate to each other helps a lot with fitting in.",
}


def clean_mojibake_text(value: str) -> str:
    if not isinstance(value, str):
        return value
    if not any(marker in value for marker in ("Ã", "Â", "â", "ð", "�")):
        return value
    try:
        return value.encode("latin-1").decode("utf-8")
    except Exception:
        return value


MACHINE_KEY_PATTERN = re.compile(r"^[a-z0-9_]+$")

ACCENT_WORD_REPLACEMENTS = {
    "identificacion": "identificación",
    "direccion": "dirección",
    "especifica": "específica",
    "especificas": "específicas",
    "alergica": "alérgica",
    "alergico": "alérgico",
    "medicacion": "medicación",
    "medico": "médico",
    "medica": "médica",
    "medicos": "médicos",
    "medicas": "médicas",
    "pagina": "página",
    "paginas": "páginas",
    "aplicacion": "aplicación",
    "comunicacion": "comunicación",
    "informacion": "información",
    "explicacion": "explicación",
    "explicarmelo": "explicármelo",
    "espanol": "español",
    "ingles": "inglés",
    "camara": "cámara",
    "rapida": "rápida",
    "rapido": "rápido",
    "tambien": "también",
    "mas": "más",
    "policia": "policía",
    "compania": "compañía",
    "numero": "número",
    "telefono": "teléfono",
    "secretaria": "secretaría",
    "autonoma": "autónoma",
    "autobus": "autobús",
    "pais": "país",
    "afiliacion": "afiliación",
    "tramite": "trámite",
    "tramites": "trámites",
    "sintomas": "síntomas",
    "movil": "móvil",
    "moviles": "móviles",
    "nomina": "nómina",
    "nominas": "nóminas",
    "reunion": "reunión",
    "habitacion": "habitación",
    "linea": "línea",
    "averia": "avería",
    "aqui": "aquí",
    "alli": "allí",
    "dias": "días",
    "situacion": "situación",
    "documentacion": "documentación",
    "basica": "básica",
    "basico": "básico",
    "basicos": "básicos",
    "algun": "algún",
    "dia": "día",
    "segun": "según",
    "trafico": "tráfico",
    "pediran": "pedirán",
    "recibire": "recibiré",
    "llegara": "llegará",
    "podria": "podría",
    "tecnico": "técnico",
    "tecnica": "técnica",
    "ayudara": "ayudará",
    "usalo": "úsalo",
    "lleveme": "lléveme",
}

QUESTION_START_REPLACEMENTS = {
    "A que": "A qué",
    "Que": "Qué",
    "Como": "Cómo",
    "Donde": "Dónde",
    "Cuando": "Cuándo",
    "Cuanto": "Cuánto",
    "Cual": "Cuál",
    "Cuales": "Cuáles",
    "Por que": "Por qué",
}


def _match_case(source: str, replacement: str) -> str:
    if source.isupper():
        return replacement.upper()
    if source[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def restore_spanish_accents(value: str) -> str:
    if not isinstance(value, str):
        return value
    if value.startswith(("http://", "https://")):
        return value

    fixed = clean_mojibake_text(value)

    for source, target in QUESTION_START_REPLACEMENTS.items():
        pattern = re.compile(rf"(^|[\n.!?]\s*){re.escape(source)}\b", re.MULTILINE)
        fixed = pattern.sub(lambda match: f"{match.group(1)}{_match_case(source, target)}", fixed)

    for source, target in ACCENT_WORD_REPLACEMENTS.items():
        pattern = re.compile(rf"\b{re.escape(source)}\b", re.IGNORECASE)
        fixed = pattern.sub(lambda match: _match_case(match.group(0), target), fixed)

    return fixed


def clean_nested_strings(value):
    if isinstance(value, dict):
        cleaned_dict = {}
        for key, item in value.items():
            cleaned_key = key
            if isinstance(key, str) and not MACHINE_KEY_PATTERN.fullmatch(key):
                cleaned_key = restore_spanish_accents(key)
            cleaned_dict[cleaned_key] = clean_nested_strings(item)
        return cleaned_dict
    if isinstance(value, list):
        return [clean_nested_strings(item) for item in value]
    if isinstance(value, tuple):
        return tuple(clean_nested_strings(item) for item in value)
    if isinstance(value, str):
        return restore_spanish_accents(value)
    return value


SURVIVAL_SECTIONS = clean_nested_strings(SURVIVAL_SECTIONS)
ADMIN_SECTIONS = clean_nested_strings(ADMIN_SECTIONS)
COMMUNICATION_SECTIONS = clean_nested_strings(COMMUNICATION_SECTIONS)
INTEGRATION_SECTIONS = clean_nested_strings(INTEGRATION_SECTIONS)
COMMUNITY_SECTIONS = clean_nested_strings(COMMUNITY_SECTIONS)
FAQ_SECTIONS = clean_nested_strings(FAQ_SECTIONS)
SPANISH_SURVIVAL_SECTIONS = clean_nested_strings(SPANISH_SURVIVAL_SECTIONS)
SPANISH_SURVIVAL_DETAILS = clean_nested_strings(SPANISH_SURVIVAL_DETAILS)
FIRST_STEPS_SECTIONS = clean_nested_strings(FIRST_STEPS_SECTIONS)
HEALTH_SECTIONS = clean_nested_strings(HEALTH_SECTIONS)
TRANSPORT_SECTIONS = clean_nested_strings(TRANSPORT_SECTIONS)
EMERGENCY_SECTIONS = clean_nested_strings(EMERGENCY_SECTIONS)
HOUSING_SECTIONS = clean_nested_strings(HOUSING_SECTIONS)
WORK_SECTIONS = clean_nested_strings(WORK_SECTIONS)
BUTTON_TRANSLATIONS = clean_nested_strings(BUTTON_TRANSLATIONS)
BUTTON_ICONS = clean_nested_strings(BUTTON_ICONS)
SPANISH_SURVIVAL_LABELS = clean_nested_strings(SPANISH_SURVIVAL_LABELS)
MANUAL_TRANSLATIONS = clean_nested_strings(MANUAL_TRANSLATIONS)


def normalize_translation_lookup(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text.lower())
    no_marks = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    cleaned = "".join(char if (char.isalnum() or char.isspace()) else " " for char in no_marks)
    return " ".join(cleaned.split())


BASIC_TRANSLATIONS_ES_EN = {
    "hola": "Hello",
    "adios": "Goodbye",
    "gracias": "Thank you",
    "por favor": "Please",
    "si": "Yes",
    "no": "No",
    "agua": "Water",
    "comida": "Food",
    "casa": "House",
    "trabajo": "Work",
    "hospital": "Hospital",
    "ayuda": "Help",
    "bano": "Bathroom",
}
BASIC_TRANSLATIONS_EN_ES = {
    "hello": "Hola",
    "goodbye": "Adiós",
    "thank you": "Gracias",
    "thanks": "Gracias",
    "please": "Por favor",
    "yes": "Sí",
    "no": "No",
    "water": "Agua",
    "food": "Comida",
    "house": "Casa",
    "work": "Trabajo",
    "hospital": "Hospital",
    "help": "Ayuda",
    "bathroom": "Baño",
}

MANUAL_TRANSLATIONS_NORMALIZED = {
    normalize_translation_lookup(key): value for key, value in MANUAL_TRANSLATIONS.items()
}
MANUAL_TRANSLATIONS_REVERSE_NORMALIZED = {}
for es_text, en_text in MANUAL_TRANSLATIONS.items():
    normalized_en = normalize_translation_lookup(en_text)
    if normalized_en and normalized_en not in MANUAL_TRANSLATIONS_REVERSE_NORMALIZED:
        MANUAL_TRANSLATIONS_REVERSE_NORMALIZED[normalized_en] = es_text


def lookup_manual_spanish_to_english(text: str) -> str | None:
    stripped = text.strip()
    if not stripped:
        return None
    if stripped in MANUAL_TRANSLATIONS:
        return MANUAL_TRANSLATIONS[stripped]

    normalized = normalize_translation_lookup(stripped)
    if normalized in MANUAL_TRANSLATIONS_NORMALIZED:
        return MANUAL_TRANSLATIONS_NORMALIZED[normalized]
    if normalized in BASIC_TRANSLATIONS_ES_EN:
        return BASIC_TRANSLATIONS_ES_EN[normalized]
    return None


def lookup_manual_english_to_spanish(text: str) -> str | None:
    stripped = text.strip()
    if not stripped:
        return None

    normalized = normalize_translation_lookup(stripped)
    if normalized in BASIC_TRANSLATIONS_EN_ES:
        return BASIC_TRANSLATIONS_EN_ES[normalized]
    if normalized in MANUAL_TRANSLATIONS_REVERSE_NORMALIZED:
        return MANUAL_TRANSLATIONS_REVERSE_NORMALIZED[normalized]
    return None


def translate_spanish_to_english(text: str) -> str:
    if not text.strip():
        return ""
    manual_translation = lookup_manual_spanish_to_english(text)
    if manual_translation:
        return manual_translation
    if text in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[text]

    try:
        encoded_text = quote(text)
        url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair=es|en"
        with urlopen(url, timeout=6) as response:
            payload = json.loads(response.read().decode("utf-8"))
        translated = payload.get("responseData", {}).get("translatedText", "").strip()
        if translated:
            TRANSLATION_CACHE[text] = translated
            return translated
    except Exception:
        pass

    fallback = "English translation unavailable right now."
    TRANSLATION_CACHE[text] = fallback
    return fallback


def translate_english_to_spanish(text: str) -> str:
    if not text.strip():
        return ""
    manual_translation = lookup_manual_english_to_spanish(text)
    if manual_translation:
        return manual_translation
    cache_key = f"en|es::{text}"
    if cache_key in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[cache_key]

    try:
        encoded_text = quote(text)
        url = f"https://api.mymemory.translated.net/get?q={encoded_text}&langpair=en|es"
        with urlopen(url, timeout=6) as response:
            payload = json.loads(response.read().decode("utf-8"))
        translated = payload.get("responseData", {}).get("translatedText", "").strip()
        if translated:
            TRANSLATION_CACHE[cache_key] = translated
            return translated
    except Exception:
        pass

    fallback = "La traducción al español no está disponible ahora mismo."
    TRANSLATION_CACHE[cache_key] = fallback
    return fallback


def detect_translation_direction(text: str) -> str:
    lowered = normalize_ai_text(text)
    spanish_tokens = {
        "el", "la", "los", "las", "un", "una", "de", "del", "que", "como", "donde", "hola",
        "gracias", "por", "para", "con", "sin", "quiero", "necesito", "tengo", "hoy", "manana",
    }
    english_tokens = {
        "the", "a", "an", "and", "or", "is", "are", "hello", "please", "thanks", "for", "with",
        "without", "need", "want", "have", "today", "tomorrow", "where", "how",
    }
    tokens = set(lowered.replace("?", " ").replace(".", " ").split())
    has_spanish_marks = any(char in text for char in "áéíóúñ¿¡")
    spanish_score = len(tokens.intersection(spanish_tokens)) + (2 if has_spanish_marks else 0)
    english_score = len(tokens.intersection(english_tokens))
    return "es_to_en" if spanish_score >= english_score else "en_to_es"


def normalize_ai_text(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text.lower())
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def ai_helper_card(page: ft.Page, context_getter) -> ft.Container:
    question_field = ft.TextField(
        hint_text="Escribe palabra o frase / Type word or phrase",
        multiline=True,
        min_lines=2,
        max_lines=4,
        border_color=AMETHYST,
        focused_border_color=RED,
        text_style=ft.TextStyle(size=15, color=TEXT_DARK, font_family=BODY_FONT),
        hint_style=ft.TextStyle(size=14, color=TEXT_MUTED, font_family=BODY_FONT),
        bgcolor=CREAM,
    )
    direction = ft.Dropdown(
        label="Dirección",
        value="auto",
        options=[
            ft.dropdown.Option("auto", "Automático"),
            ft.dropdown.Option("es_to_en", "Español -> Inglés"),
            ft.dropdown.Option("en_to_es", "English -> Spanish"),
        ],
        border_color=AMETHYST,
        focused_border_color=RED,
        text_style=ft.TextStyle(size=14, color=TEXT_DARK, font_family=BODY_FONT),
    )
    source_text = ft.Text("", size=11, color=TEXT_MUTED, italic=True, visible=False)
    answer_es = ft.Text("", size=15, color=TEXT_DARK)
    answer_en = ft.Text("", size=12, color=TEXT_MUTED, italic=True)
    answer_block = ft.Column([answer_es, answer_en], spacing=8, tight=True, visible=False)

    def handle_ai_question(e) -> None:
        text_to_translate = (question_field.value or "").strip()
        if not text_to_translate:
            source_text.value = "Escribe algo para traducir."
            source_text.visible = True
            answer_block.visible = False
            page.update()
            return

        source_text.value = "Traduciendo..."
        source_text.visible = True
        answer_block.visible = False
        page.update()

        selected_direction = direction.value or "auto"
        resolved_direction = selected_direction
        if selected_direction == "auto":
            resolved_direction = detect_translation_direction(text_to_translate)

        if resolved_direction == "es_to_en":
            translated = translate_spanish_to_english(text_to_translate)
            source_text.value = "Traducción: Español -> Inglés"
            answer_es.value = f"Español: {text_to_translate}"
            answer_en.value = f"English: {translated}"
        else:
            translated = translate_english_to_spanish(text_to_translate)
            source_text.value = "Traducción: Inglés -> Español"
            answer_es.value = f"Español: {translated}"
            answer_en.value = f"English: {text_to_translate}"

        answer_block.visible = True
        page.update()

    return ft.Container(
        padding=18,
        border_radius=22,
        bgcolor=ft.Colors.with_opacity(0.9, SOFT_YELLOW),
        content=ft.Column(
            [
                ft.Text(
                    "TRADUCTOR",
                    size=20,
                    weight=ft.FontWeight.W_700,
                    color=TEXT_DARK,
                    text_align=ft.TextAlign.CENTER,
                    font_family=TITLE_FONT,
                ),
                question_field,
                direction,
                bilingual_mobile_button(
                    "Traducir",
                    "Translate",
                    handle_ai_question,
                    RED,
                    "#FFFFFF",
                ),
                source_text,
                answer_block,
            ],
            spacing=12,
            tight=True,
        ),
    )


USEFUL_RESOURCES = {
    "cita_nie": {
        "links": [
            ("Cita previa AGE / Extranjería", "https://administracion.gob.es/pag_Home/atencionCiudadana/Solicitar_cita_previa-nueva.html"),
        ],
        "phones": [],
    },
    "nie_tie": {
        "links": [
            ("Cita previa AGE / Extranjería", "https://administracion.gob.es/pag_Home/atencionCiudadana/Solicitar_cita_previa-nueva.html"),
            ("Información general 060", "https://administracion.gob.es/pag_Home/atencionCiudadana/ayudame/necesito.html"),
        ],
        "phones": [
            ("060", "Información general de la Administración"),
        ],
    },
    "empadronamiento": {
        "links": [
            ("Información general 060", "https://administracion.gob.es/pag_Home/atencionCiudadana/ayudame/necesito.html"),
        ],
        "phones": [
            ("060", "Orientación general para trámites con la Administración"),
        ],
    },
    "numero_seguridad_social": {
        "links": [
            ("Sede Seguridad Social", "https://sede.seg-social.gob.es/"),
            ("Cita previa INSS", "https://sede.seg-social.gob.es/wps/portal/sede/sede/Ciudadanos/cita%20previa%20para%20pensiones%20y%20otras%20prestaciones/13cita%20previa%20para%20pensiones%20y%20otras%20prestaciones"),
            ("Trámites sin certificado", "https://tramites.seg-social.es/"),
        ],
        "phones": [
            ("915 42 11 76", "Información INSS"),
            ("901 16 65 65", "Información INSS, puede tener coste según operador"),
        ],
    },
    "seguridad_social": {
        "links": [
            ("Sede Seguridad Social", "https://sede.seg-social.gob.es/"),
            ("Cita previa INSS", "https://sede.seg-social.gob.es/wps/portal/sede/sede/Ciudadanos/cita%20previa%20para%20pensiones%20y%20otras%20prestaciones/13cita%20previa%20para%20pensiones%20y%20otras%20prestaciones"),
            ("Trámites sin certificado", "https://tramites.seg-social.es/"),
        ],
        "phones": [
            ("915 42 11 76", "Información INSS"),
            ("901 16 65 65", "Información INSS, puede tener coste según operador"),
        ],
    },
    "tarjeta_sanitaria": {
        "links": [
            ("Información tarjeta sanitaria SNS", "https://www.sanidad.gob.es/organizacion/sns/planCalidadSNS/tecInfo/tarjetaSanitaria/home.htm"),
        ],
        "phones": [],
    },
    "llamar_112": {
        "links": [
            ("Información 016", "https://violenciagenero.igualdad.gob.es/informacion-3/recursos/telefono016/"),
        ],
        "phones": [
            ("112", "Emergencias generales"),
            ("016", "Violencia contra las mujeres, 24 horas"),
            ("091", "Policía Nacional"),
            ("062", "Guardia Civil"),
        ],
    },
    "direccion_exacta": {
        "links": [
            ("Información 016", "https://violenciagenero.igualdad.gob.es/informacion-3/recursos/telefono016/"),
        ],
        "phones": [
            ("112", "Emergencias generales"),
            ("091", "Policía Nacional"),
            ("062", "Guardia Civil"),
        ],
    },
    "documentos_urgentes": {
        "links": [
            ("Información 016", "https://violenciagenero.igualdad.gob.es/informacion-3/recursos/telefono016/"),
        ],
        "phones": [
            ("112", "Emergencias generales"),
            ("091", "Policía Nacional"),
            ("062", "Guardia Civil"),
        ],
    },
}

USEFUL_RESOURCES = clean_nested_strings(USEFUL_RESOURCES)


def useful_resources_controls(page: ft.Page, resource_key: str | None) -> list[ft.Control]:
    if not resource_key or resource_key not in USEFUL_RESOURCES:
        return []

    resource = USEFUL_RESOURCES[resource_key]
    controls: list[ft.Control] = []

    for label, url in resource["links"]:
        controls.append(
            bilingual_mobile_button(
                label,
                translate_spanish_to_english(label),
                lambda e, target=url: open_external_url(page, target),
                YELLOW,
                RED,
            )
        )

    if resource["phones"]:
        controls.append(
            ft.Container(
                padding=18,
                border_radius=22,
                bgcolor=ft.Colors.with_opacity(0.9, SOFT_YELLOW),
                content=ft.Column(
                    [
                        *[
                            control
                            for idx, (phone, description) in enumerate(resource["phones"])
                            for control in (
                                [
                                    ft.Text(
                                        f"{phone}  •  {description}",
                                        size=15,
                                        color=TEXT_MUTED,
                                    ),
                                    ft.Text(
                                        translate_spanish_to_english(description),
                                        size=12,
                                        color=TEXT_MUTED,
                                        italic=True,
                                    ),
                                ]
                                + ([ft.Container(height=6)] if idx < len(resource["phones"]) - 1 else [])
                            )
                        ],
                    ],
                    spacing=10,
                    tight=True,
                ),
            )
        )

    return controls


def intro_view(page: ft.Page) -> ft.Container:
    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        padding=20,
        content=phone_frame(
            ft.Container(
                expand=True,
                gradient=BG_GRADIENT,
                padding=16,
                content=ft.SafeArea(
                    ft.Column(
                        [
                            ft.Container(height=2),
                            card(
                                [
                                    ft.Container(
                                        alignment=ft.Alignment(0, 0),
                                        content=ft.Image(
                                            src="miriam-logo.jpeg",
                                            width=170,
                                            height=170,
                                            border_radius=24,
                                        ),
                                    ),
                                    ft.Text(
                                        "Siéntete como en casa en España a través del idioma.",
                                        size=17,
                                        weight=ft.FontWeight.W_700,
                                        color=TEXT_DARK,
                                        text_align=ft.TextAlign.CENTER,
                                        font_family=TITLE_FONT,
                                    ),
                                    ft.Text(
                                        "Feel at home in Spain through language.",
                                        size=12,
                                        color=TEXT_DARK,
                                        italic=True,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Container(
                                        padding=12,
                                        border_radius=22,
                                        bgcolor=ft.Colors.with_opacity(0.9, SOFT_YELLOW),
                                        content=ft.Column(
                                            [
                                                ft.Text(
                                                    "Soy Miriam. Ayudo a expatriados y personas que se mudan a España a mejorar sus habilidades de comunicación para la vida cotidiana.",
                                                    size=14,
                                                    color=TEXT_MUTED,
                                                    text_align=ft.TextAlign.CENTER,
                                                ),
                                                ft.Text(
                                                    "I'm Miriam. I help expats and people moving to Spain improve their communication skills for everyday life.",
                                                    size=11,
                                                    color=TEXT_MUTED,
                                                    italic=True,
                                                    text_align=ft.TextAlign.CENTER,
                                                ),
                                            ],
                                            spacing=8,
                                            tight=True,
                                        ),
                                    ),
                                    ft.Button(
                                        content=ft.Row(
                                            [
                                                ft.Text(
                                                    "Entrar",
                                                    size=16,
                                                    weight=ft.FontWeight.W_700,
                                                    font_family=TITLE_FONT,
                                                    color=RED,
                                                ),
                                                ft.Icon(
                                                    ft.Icons.ARROW_FORWARD_ROUNDED,
                                                    size=18,
                                                    color=RED,
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            spacing=8,
                                            tight=True,
                                        ),
                                        on_click=lambda e: show_home(page),
                                        width=300,
                                        style=ft.ButtonStyle(
                                            bgcolor=YELLOW,
                                            color=RED,
                                            padding=14,
                                            side=ft.BorderSide(2, AMETHYST),
                                            shape=ft.RoundedRectangleBorder(radius=18),
                                        ),
                                        height=60,
                                    ),
                                ]
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    )
                ),
            )
        ),
    )


def home_view(page: ft.Page) -> ft.View:
    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        padding=20,
        content=phone_frame(
            ft.Container(
                expand=True,
                gradient=BG_GRADIENT,
                padding=20,
                content=ft.SafeArea(
                    ft.Column(
                        [
                            ft.Container(height=8),
                            card(
                                [
                                    ft.Text(
                                        "MIRIAM COMUNICA",
                                        size=24,
                                        weight=ft.FontWeight.W_700,
                                        color=RED,
                                        text_align=ft.TextAlign.CENTER,
                                        no_wrap=True,
                                    ),
                                    ft.Text(
                                        "Esta aplicación es gratuita. Si quieres agradecérmelo.",
                                        size=16,
                                        color=TEXT_MUTED,
                                    ),
                                    ft.Text(
                                        "This app is free. If you want to support me.",
                                        size=12,
                                        color=TEXT_MUTED,
                                        italic=True,
                                    ),
                                    bilingual_mobile_button(
                                        "Seguir en Instagram",
                                        "Follow on Instagram",
                                        lambda e: open_external_url(page, INSTAGRAM_URL),
                                        YELLOW,
                                        RED,
                                    ),
                                    bilingual_mobile_button(
                                        "Seguir en TikTok",
                                        "Follow on TikTok",
                                        lambda e: open_external_url(page, TIKTOK_URL),
                                        YELLOW,
                                        RED,
                                    ),
                                    bilingual_mobile_button(
                                        "Página web",
                                        "Website",
                                        lambda e: open_external_url(page, WEB_URL),
                                        YELLOW,
                                        RED,
                                    ),
                                    bilingual_mobile_button(
                                        "Continuar",
                                        "Continue",
                                        lambda e: show_entry_menu(page),
                                        YELLOW,
                                        RED,
                                    ),
                                ]
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    )
                ),
            )
        ),
    )


def show_home(page: ft.Page) -> None:
    page.app_host.content = home_view(page)
    page.update()


def show_intro(page: ft.Page) -> None:
    page.app_host.content = intro_view(page)
    page.update()


def entry_menu_view(page: ft.Page) -> ft.Container:
    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        gradient=BG_GRADIENT,
        padding=24,
        content=ft.SafeArea(
            ft.Container(
                expand=True,
                border_radius=32,
                bgcolor=ft.Colors.with_opacity(0.96, "#FFFFFF"),
                padding=32,
                content=ft.Column(
                    [
                        ft.Text(
                            "ELIGE CÓMO QUIERES EMPEZAR",
                            size=28,
                            weight=ft.FontWeight.W_700,
                            color=RED,
                            text_align=ft.TextAlign.CENTER,
                            font_family=TITLE_FONT,
                        ),
                        ft.Text(
                            "Choose how you want to start",
                            size=13,
                            italic=True,
                            color=TEXT_MUTED,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        bilingual_mobile_button(
                            "KIT DE SUPERVIVENCIA",
                            "Survival kit",
                            lambda e: show_survival(page),
                            YELLOW,
                            RED,
                            width=360,
                        ),
                        bilingual_mobile_button(
                            "ESPAÑOL PARA LA VIDA DIARIA",
                            "Spanish for daily life",
                            lambda e: show_spanish_survival(page),
                            YELLOW,
                            RED,
                            width=360,
                        ),
                        bilingual_mobile_button(
                            "Clases online con Miriam",
                            "WhatsApp +34 611 090 017",
                            lambda e: open_external_url(page, WHATSAPP_CLASSES_URL),
                            YELLOW,
                            RED,
                            width=360,
                            height=80,
                        ),
                        bilingual_mobile_button(
                            "Volver al inicio",
                            "Back to home",
                            lambda e: show_home(page),
                            RED,
                            "#FFFFFF",
                            width=360,
                        ),
                    ],
                    spacing=22,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.AUTO,
                ),
            )
        ),
    )


def spanish_survival_view(page: ft.Page) -> ft.Container:
    default_key = "restaurante"
    default_detail_key = "comportamiento"
    default_section = SPANISH_SURVIVAL_DETAILS[default_key][default_detail_key]
    title_group = ft.Column(
        bilingual_heading(default_section["title"], 22, True),
        spacing=6,
        tight=True,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    subtitle_text = ft.Text(
        "Spanish for everyday situations",
        size=14,
        weight=ft.FontWeight.W_700,
        color=TEXT_DARK,
        italic=True,
        text_align=ft.TextAlign.CENTER,
        width=300,
    )
    body_group = ft.Column(
        bilingual_body_controls(default_section["body"]),
        spacing=4,
        tight=True,
    )

    detail_dropdown = ft.Dropdown(
        value=default_detail_key,
        width=300,
        bgcolor=CREAM,
        border_color=RED,
        focused_border_color=RED,
        color=TEXT_DARK,
        text_size=15,
        options=spanish_survival_detail_options(default_key),
    )

    def refresh_spanish_detail(situation_key: str, detail_key: str) -> None:
        section = SPANISH_SURVIVAL_DETAILS[situation_key][detail_key]
        title_group.controls = bilingual_heading(section["title"], 22, True)
        body_group.controls = bilingual_body_controls(section["body"])

    def update_spanish_detail(e) -> None:
        refresh_spanish_detail(situation_dropdown.value, e.control.value)
        page.update()

    def update_spanish_situation(e) -> None:
        situation_key = e.control.value
        first_detail_key = next(iter(SPANISH_SURVIVAL_DETAILS[situation_key]))
        detail_dropdown.options = spanish_survival_detail_options(situation_key)
        detail_dropdown.value = first_detail_key
        refresh_spanish_detail(situation_key, first_detail_key)
        page.update()

    detail_dropdown.on_select = update_spanish_detail
    situation_dropdown = ft.Dropdown(
        value=default_key,
        width=300,
        bgcolor=CREAM,
        border_color=RED,
        focused_border_color=RED,
        color=TEXT_DARK,
        text_size=14,
        options=spanish_survival_situation_options(),
        on_select=update_spanish_situation,
    )

    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        padding=20,
        content=phone_frame(
            ft.Container(
                expand=True,
                gradient=BG_GRADIENT,
                padding=20,
                content=ft.SafeArea(
                    ft.Column(
                        [
                            ft.Container(height=8),
                            card(
                                [
                                    ft.Text(
                                        "ESPAÑOL PARA LA VIDA DIARIA",
                                        size=26,
                                        weight=ft.FontWeight.W_700,
                                        color=RED,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    subtitle_text,
                                    situation_dropdown,
                                    detail_dropdown,
                                    ft.Container(
                                        padding=18,
                                        border_radius=22,
                                        bgcolor=ft.Colors.with_opacity(0.9, SOFT_YELLOW),
                                        content=ft.Column(
                                            [
                                                title_group,
                                                body_group,
                                            ],
                                            spacing=12,
                                            tight=True,
                                        ),
                                    ),
                                    ai_helper_card(
                                        page,
                                        lambda: (
                                            f"{situation_dropdown.value} "
                                            f"{detail_dropdown.value} "
                                            f"{SPANISH_SURVIVAL_DETAILS[situation_dropdown.value][detail_dropdown.value]['title']} "
                                            f"{SPANISH_SURVIVAL_DETAILS[situation_dropdown.value][detail_dropdown.value]['body']}"
                                        ),
                                    ),
                                    bilingual_mobile_button(
                                        "Volver",
                                        "Back",
                                        lambda e: show_entry_menu(page),
                                        RED,
                                        "#FFFFFF",
                                    ),
                                ]
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    )
                ),
            )
        ),
    )


def show_entry_menu(page: ft.Page) -> None:
    page.app_host.content = entry_menu_view(page)
    page.update()


def survival_menu_view(page: ft.Page) -> ft.Container:
    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        padding=20,
        content=phone_frame(
            ft.Container(
                expand=True,
                gradient=BG_GRADIENT,
                padding=20,
                content=ft.SafeArea(
                    ft.Column(
                        [
                            ft.Container(height=8),
                            card(
                                [
                                    *kit_title_controls(),
                                    bilingual_mobile_button(
                                        "Primeros 7 días",
                                        "First 7 days",
                                        lambda e: show_survival_section(page, "primeros_pasos"),
                                        RED,
                                        "#FFFFFF",
                                    ),
                                    bilingual_mobile_button(
                                        "Salud",
                                        "Health",
                                        lambda e: show_survival_section(page, "salud"),
                                        RED,
                                        "#FFFFFF",
                                    ),
                                    bilingual_mobile_button(
                                        "Transporte",
                                        "Transport",
                                        lambda e: show_survival_section(page, "transporte"),
                                        RED,
                                        "#FFFFFF",
                                    ),
                                    bilingual_mobile_button(
                                        "Emergencias",
                                        "Emergencies",
                                        lambda e: show_survival_section(page, "emergencias"),
                                        RED,
                                        "#FFFFFF",
                                    ),
                                    bilingual_mobile_button(
                                        "Vivienda",
                                        "Housing",
                                        lambda e: show_survival_section(page, "vivienda"),
                                        RED,
                                        "#FFFFFF",
                                    ),
                                    bilingual_mobile_button(
                                        "Trabajo",
                                        "Work",
                                        lambda e: show_survival_section(page, "trabajo"),
                                        RED,
                                        "#FFFFFF",
                                    ),
                                    bilingual_mobile_button(
                                        "Preguntas frecuentes",
                                        "Frequently asked questions",
                                        lambda e: show_survival_section(page, "preguntas_frecuentes"),
                                        RED,
                                        "#FFFFFF",
                                    ),
                                    ai_helper_card(page, lambda: "kit de supervivencia primeros pasos documentos salud transporte emergencias vivienda trabajo"),
                                    bilingual_mobile_button(
                                        "Volver al inicio",
                                        "Back to home",
                                        lambda e: show_home(page),
                                        RED,
                                        "#FFFFFF",
                                    ),
                                ]
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    )
                ),
            )
        ),
    )


def survival_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = SURVIVAL_SECTIONS[section_key]
    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        padding=20,
        content=phone_frame(
            ft.Container(
                expand=True,
                gradient=BG_GRADIENT,
                padding=20,
                content=ft.SafeArea(
                    ft.Column(
                        [
                            ft.Container(height=8),
                            card(
                                [
                                    *kit_title_controls(),
                                    *bilingual_heading(section["title"], 28, False),
                                    ft.Container(
                                        padding=18,
                                        border_radius=22,
                                        bgcolor=ft.Colors.with_opacity(0.9, SOFT_YELLOW),
                                        content=ft.Column(
                                            bilingual_body_controls(section["body"]),
                                            spacing=0,
                                            tight=True,
                                        ),
                                    ),
                                    ai_helper_card(page, lambda: f"{section['title']} {section['body']}"),
                                    menu_bilingual_button(
                                        "Volver al kit",
                                        lambda e: show_survival(page),
                                    ),
                                    menu_bilingual_button(
                                        "Volver al inicio",
                                        lambda e: show_home(page),
                                    ),
                                ]
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    )
                ),
            )
        ),
    )


def admin_menu_view(page: ft.Page) -> ft.Container:
    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        padding=20,
        content=phone_frame(
            ft.Container(
                expand=True,
                gradient=BG_GRADIENT,
                padding=20,
                content=ft.SafeArea(
                    ft.Column(
                        [
                            ft.Container(height=8),
                            card(
                                [
                                    *kit_title_controls(),
                                    *bilingual_heading("ADMINISTRATIVA", 24, True),
                                    menu_bilingual_button(
                                        "NIE / TIE",
                                        lambda e: show_admin_section(page, "nie_tie"),
                                    ),
                                    menu_bilingual_button(
                                        "Empadronamiento",
                                        lambda e: show_admin_section(page, "empadronamiento"),
                                    ),
                                    menu_bilingual_button(
                                        "Seguridad Social",
                                        lambda e: show_admin_section(page, "seguridad_social"),
                                    ),
                                    ai_helper_card(page, lambda: "administrativa nie tie empadronamiento seguridad social"),
                                    menu_bilingual_button(
                                        "Volver al kit",
                                        lambda e: show_survival(page),
                                    ),
                                ]
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    )
                ),
            )
        ),
    )


def admin_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = ADMIN_SECTIONS[section_key]
    return detail_view(
        page,
        section["title"],
        section["body"],
        "Volver a administrativa",
        show_admin_menu,
        section_key,
    )


def submenu_view(
    page: ft.Page,
    subtitle: str,
    buttons: list[ft.Control],
    back_action,
    show_english_subtitle: bool = True,
) -> ft.Container:
    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        padding=20,
        content=phone_frame(
            ft.Container(
                expand=True,
                gradient=BG_GRADIENT,
                padding=20,
                content=ft.SafeArea(
                    ft.Column(
                        [
                            ft.Container(height=8),
                            card(
                                [
                                    *kit_title_controls(),
                                    *bilingual_heading(subtitle, 24, True, show_english_subtitle),
                                    *buttons,
                                    ai_helper_card(page, lambda: subtitle),
                                    menu_bilingual_button(
                                        "Volver al kit",
                                        lambda e: back_action(page),
                                    ),
                                ]
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    )
                ),
            )
        ),
    )


def detail_view(
    page: ft.Page,
    title: str,
    body: str,
    back_label: str,
    back_action,
    resource_key: str | None = None,
) -> ft.Container:
    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        padding=20,
        content=phone_frame(
            ft.Container(
                expand=True,
                gradient=BG_GRADIENT,
                padding=20,
                content=ft.SafeArea(
                    ft.Column(
                        [
                            ft.Container(height=8),
                            card(
                                [
                                    *kit_title_controls(),
                                    *bilingual_heading(title, 24, False),
                                    ft.Container(
                                        padding=18,
                                        border_radius=22,
                                        bgcolor=ft.Colors.with_opacity(0.9, SOFT_YELLOW),
                                        content=ft.Column(
                                            bilingual_body_controls(body),
                                            spacing=0,
                                            tight=True,
                                        ),
                                    ),
                                    *useful_resources_controls(page, resource_key),
                                    ai_helper_card(page, lambda: f"{title} {body}"),
                                    menu_bilingual_button(
                                        back_label,
                                        lambda e: back_action(page),
                                    ),
                                    menu_bilingual_button(
                                        "Volver al kit",
                                        lambda e: show_survival(page),
                                    ),
                                ]
                            ),
                        ],
                        scroll=ft.ScrollMode.AUTO,
                    )
                ),
            )
        ),
    )


def communication_menu_view(page: ft.Page) -> ft.Container:
    return submenu_view(
        page,
        "COMUNICACIÓN",
        [
            menu_bilingual_button("Modo médico", lambda e: show_communication_section(page, "modo_medico")),
            menu_bilingual_button("Escáner de documentos", lambda e: show_communication_section(page, "escaner_documentos")),
            menu_bilingual_button("Jerga española", lambda e: show_communication_section(page, "jerga_espanola")),
        ],
        show_survival,
    )


def communication_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = COMMUNICATION_SECTIONS[section_key]
    return detail_view(
        page,
        section["title"],
        section["body"],
        "Volver a comunicación",
        show_communication_menu,
    )


def integration_menu_view(page: ft.Page) -> ft.Container:
    return submenu_view(
        page,
        "INTEGRACIÓN",
        [
            menu_bilingual_button("Mapa de servicios", lambda e: show_integration_section(page, "mapa_servicios")),
            menu_bilingual_button("Transporte", lambda e: show_integration_section(page, "transporte")),
            menu_bilingual_button("Emergencias", lambda e: show_integration_section(page, "emergencias")),
        ],
        show_survival,
    )


def integration_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = INTEGRATION_SECTIONS[section_key]
    return detail_view(
        page,
        section["title"],
        section["body"],
        "Volver a integración",
        show_integration_menu,
    )


def community_menu_view(page: ft.Page) -> ft.Container:
    return submenu_view(
        page,
        "COMUNIDAD",
        [
            menu_bilingual_button("Foro de recién llegados", lambda e: show_community_section(page, "foro_recien_llegados")),
            menu_bilingual_button("Intercambio de idiomas", lambda e: show_community_section(page, "intercambio_idiomas")),
        ],
        show_survival,
    )


def community_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = COMMUNITY_SECTIONS[section_key]
    return detail_view(
        page,
        section["title"],
        section["body"],
        "Volver a comunidad",
        show_community_menu,
    )


def faq_menu_view(page: ft.Page) -> ft.Container:
    return submenu_view(
        page,
        "PREGUNTAS FRECUENTES",
        [
            menu_bilingual_button("¿Cómo pido la cita del NIE?", lambda e: show_faq_section(page, "cita_nie")),
            menu_bilingual_button("¿Para qué sirve el empadronamiento?", lambda e: show_faq_section(page, "empadronamiento_para_que")),
            menu_bilingual_button("¿Cómo consigo el número de Seguridad Social?", lambda e: show_faq_section(page, "numero_seguridad_social")),
            menu_bilingual_button("¿Cuándo tengo que llamar al 112?", lambda e: show_faq_section(page, "llamar_112")),
            menu_bilingual_button("¿Cómo pido la tarjeta sanitaria?", lambda e: show_faq_section(page, "tarjeta_sanitaria")),
            menu_bilingual_button("¿Qué bono de transporte me conviene?", lambda e: show_faq_section(page, "bono_transporte")),
        ],
        show_survival,
    )


def faq_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = FAQ_SECTIONS[section_key]
    return detail_view(
        page,
        section["title"],
        section["body"],
        "Volver a preguntas",
        show_faq_menu,
        section_key,
    )


def first_steps_menu_view(page: ft.Page) -> ft.Container:
    return submenu_view(
        page,
        "PRIMEROS PASOS",
        [
            menu_bilingual_button("Empadronamiento", lambda e: show_first_steps_section(page, "empadronamiento")),
            menu_bilingual_button("NIE / TIE", lambda e: show_first_steps_section(page, "nie_tie")),
            menu_bilingual_button("Seguridad Social", lambda e: show_first_steps_section(page, "seguridad_social")),
        ],
        show_survival,
    )


def first_steps_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = FIRST_STEPS_SECTIONS[section_key]
    return detail_view(
        page,
        section["title"],
        section["body"],
        "Volver a primeros pasos",
        show_first_steps_menu,
        section_key,
    )


def procedures_menu_view(page: ft.Page) -> ft.Container:
    return submenu_view(
        page,
        "TRÁMITES",
        [
            menu_bilingual_button("NIE / TIE", lambda e: show_procedures_section(page, "nie_tie")),
            menu_bilingual_button("Empadronamiento", lambda e: show_procedures_section(page, "empadronamiento")),
            menu_bilingual_button("Seguridad Social", lambda e: show_procedures_section(page, "seguridad_social")),
        ],
        show_survival,
    )


def procedures_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = ADMIN_SECTIONS[section_key]
    return detail_view(
        page,
        section["title"],
        section["body"],
        "Volver a trámites",
        show_procedures_menu,
        section_key,
    )


def health_menu_view(page: ft.Page) -> ft.Container:
    return submenu_view(
        page,
        "SALUD",
        [
            menu_bilingual_button("Modo médico", lambda e: show_health_section(page, "modo_medico")),
            menu_bilingual_button("Centros de salud", lambda e: show_health_section(page, "centros_salud")),
            menu_bilingual_button("Tarjeta sanitaria", lambda e: show_health_section(page, "tarjeta_sanitaria")),
        ],
        show_survival,
        show_english_subtitle=False,
    )


def health_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = HEALTH_SECTIONS[section_key]
    return detail_view(
        page,
        section["title"],
        section["body"],
        "Volver a salud",
        show_health_menu,
        section_key,
    )


def transport_menu_view(page: ft.Page) -> ft.Container:
    return submenu_view(
        page,
        "TRANSPORTE",
        [
            menu_bilingual_button("Bono de metro", lambda e: show_transport_section(page, "bono_metro")),
            menu_bilingual_button("Bono de autobús", lambda e: show_transport_section(page, "bono_bus")),
            menu_bilingual_button("Cómo moverse", lambda e: show_transport_section(page, "como_moverse")),
        ],
        show_survival,
    )


def transport_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = TRANSPORT_SECTIONS[section_key]
    return detail_view(
        page,
        section["title"],
        section["body"],
        "Volver a transporte",
        show_transport_menu,
    )


def emergency_menu_view(page: ft.Page) -> ft.Container:
    return submenu_view(
        page,
        "EMERGENCIAS",
        [
            menu_bilingual_button("Llamar al 112", lambda e: show_emergency_section(page, "llamar_112")),
            menu_bilingual_button("Dirección exacta", lambda e: show_emergency_section(page, "direccion_exacta")),
            menu_bilingual_button("Documentos urgentes", lambda e: show_emergency_section(page, "documentos_urgentes")),
        ],
        show_survival,
    )


def emergency_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = EMERGENCY_SECTIONS[section_key]
    return detail_view(
        page,
        section["title"],
        section["body"],
        "Volver a emergencias",
        show_emergency_menu,
        section_key,
    )


def housing_menu_view(page: ft.Page) -> ft.Container:
    return submenu_view(
        page,
        "VIVIENDA",
        [
            menu_bilingual_button("Alquiler", lambda e: show_housing_section(page, "alquiler")),
            menu_bilingual_button("Empadronarse", lambda e: show_housing_section(page, "empadronarse")),
            menu_bilingual_button("Luz, agua e internet", lambda e: show_housing_section(page, "suministros")),
        ],
        show_survival,
    )


def housing_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = HOUSING_SECTIONS[section_key]
    return detail_view(
        page,
        section["title"],
        section["body"],
        "Volver a vivienda",
        show_housing_menu,
    )


def work_menu_view(page: ft.Page) -> ft.Container:
    return submenu_view(
        page,
        "TRABAJO",
        [
            menu_bilingual_button("Buscar trabajo", lambda e: show_work_section(page, "buscar_trabajo")),
            menu_bilingual_button("Contrato y nómina", lambda e: show_work_section(page, "contrato")),
            menu_bilingual_button("Derechos básicos", lambda e: show_work_section(page, "derechos_basicos")),
        ],
        show_survival,
    )


def work_section_view(page: ft.Page, section_key: str) -> ft.Container:
    section = WORK_SECTIONS[section_key]
    return detail_view(
        page,
        section["title"],
        section["body"],
        "Volver a trabajo",
        show_work_menu,
    )


def show_survival(page: ft.Page) -> None:
    page.app_host.content = survival_menu_view(page)
    page.update()


def show_spanish_survival(page: ft.Page) -> None:
    page.app_host.content = spanish_survival_view(page)
    page.update()


def show_survival_section(page: ft.Page, section_key: str) -> None:
    if section_key == "primeros_pasos":
        page.app_host.content = first_steps_menu_view(page)
    elif section_key == "tramites":
        page.app_host.content = procedures_menu_view(page)
    elif section_key == "salud":
        page.app_host.content = health_menu_view(page)
    elif section_key == "transporte":
        page.app_host.content = transport_menu_view(page)
    elif section_key == "emergencias":
        page.app_host.content = emergency_menu_view(page)
    elif section_key == "vivienda":
        page.app_host.content = housing_menu_view(page)
    elif section_key == "trabajo":
        page.app_host.content = work_menu_view(page)
    elif section_key == "preguntas_frecuentes":
        page.app_host.content = faq_menu_view(page)
    else:
        page.app_host.content = survival_section_view(page, section_key)
    page.update()


def show_admin_menu(page: ft.Page) -> None:
    page.app_host.content = admin_menu_view(page)
    page.update()


def show_admin_section(page: ft.Page, section_key: str) -> None:
    page.app_host.content = admin_section_view(page, section_key)
    page.update()


def show_communication_menu(page: ft.Page) -> None:
    page.app_host.content = communication_menu_view(page)
    page.update()


def show_communication_section(page: ft.Page, section_key: str) -> None:
    page.app_host.content = communication_section_view(page, section_key)
    page.update()


def show_integration_menu(page: ft.Page) -> None:
    page.app_host.content = integration_menu_view(page)
    page.update()


def show_integration_section(page: ft.Page, section_key: str) -> None:
    page.app_host.content = integration_section_view(page, section_key)
    page.update()


def show_community_menu(page: ft.Page) -> None:
    page.app_host.content = community_menu_view(page)
    page.update()


def show_community_section(page: ft.Page, section_key: str) -> None:
    page.app_host.content = community_section_view(page, section_key)
    page.update()


def show_faq_menu(page: ft.Page) -> None:
    page.app_host.content = faq_menu_view(page)
    page.update()


def show_faq_section(page: ft.Page, section_key: str) -> None:
    page.app_host.content = faq_section_view(page, section_key)
    page.update()


def show_first_steps_menu(page: ft.Page) -> None:
    page.app_host.content = first_steps_menu_view(page)
    page.update()


def show_first_steps_section(page: ft.Page, section_key: str) -> None:
    page.app_host.content = first_steps_section_view(page, section_key)
    page.update()


def show_procedures_menu(page: ft.Page) -> None:
    page.app_host.content = procedures_menu_view(page)
    page.update()


def show_procedures_section(page: ft.Page, section_key: str) -> None:
    page.app_host.content = procedures_section_view(page, section_key)
    page.update()


def show_health_menu(page: ft.Page) -> None:
    page.app_host.content = health_menu_view(page)
    page.update()


def show_health_section(page: ft.Page, section_key: str) -> None:
    page.app_host.content = health_section_view(page, section_key)
    page.update()


def show_transport_menu(page: ft.Page) -> None:
    page.app_host.content = transport_menu_view(page)
    page.update()


def show_transport_section(page: ft.Page, section_key: str) -> None:
    page.app_host.content = transport_section_view(page, section_key)
    page.update()


def show_emergency_menu(page: ft.Page) -> None:
    page.app_host.content = emergency_menu_view(page)
    page.update()


def show_emergency_section(page: ft.Page, section_key: str) -> None:
    page.app_host.content = emergency_section_view(page, section_key)
    page.update()


def show_housing_menu(page: ft.Page) -> None:
    page.app_host.content = housing_menu_view(page)
    page.update()


def show_housing_section(page: ft.Page, section_key: str) -> None:
    page.app_host.content = housing_section_view(page, section_key)
    page.update()


def show_work_menu(page: ft.Page) -> None:
    page.app_host.content = work_menu_view(page)
    page.update()


def show_work_section(page: ft.Page, section_key: str) -> None:
    page.app_host.content = work_section_view(page, section_key)
    page.update()


def main(page: ft.Page) -> None:
    page.title = "Miriam Comunica"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(font_family=BODY_FONT)
    page.bgcolor = SOFT_YELLOW
    page.padding = 0
    page.spacing = 0
    page.window_width = 390
    page.window_height = 844
    page.window_resizable = False
    page.window_maximizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.app_host = ft.Container(expand=True)
    page.add(page.app_host)
    show_intro(page)


if __name__ == "__main__":
    ft.run(main)
