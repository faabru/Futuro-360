# -*- coding: utf-8 -*-
"""
Dataset oficial del Test Vocacional (30 preguntas).

Cada pregunta tiene 4 opciones (A-D), cada una mapeada a un área_profesional
del sistema, más la opción "Ninguna de las anteriores" (área Neutral) que
suma 0 puntos. El orden de la lista define el orden de aparición en el test.

Reemplaza el conjunto anterior (29 preguntas). El script `sync_preguntas.py`
aplica estos datos a la base ya creada; el dump `base de datos/futuro 360.sql`
se regenera con estas mismas preguntas para bases nuevas.

Aclaración: la pregunta 20 original ("¿Qué preferirías dejar como legado?")
fue reemplazada por una consigna nueva que no se parece a las anteriores.
"""

PREGUNTAS_NUEVAS = [
    {
        "texto": "Cuando tenés un día completamente libre, ¿qué te gustaría hacer?",
        "opciones": [
            ("Pasar tiempo al aire libre, recorrer lugares naturales o estar en contacto con animales o plantas.", "Agronomía"),
            ("Dibujar, diseñar, sacar fotos, hacer música o crear algo propio.", "Arte y Diseño"),
            ("Leer, conocer historias y culturas, y reflexionar sobre distintas ideas.", "Humanidades"),
            ("Pasar tiempo con computadoras, tecnología, videojuegos o herramientas digitales.", "Tecnología"),
        ],
    },
    {
        "texto": "Cuando aparece un problema difícil, ¿qué te sale naturalmente hacer?",
        "opciones": [
            ("Buscar una solución práctica y pensar cómo llevarla a la realidad.", "Ingeniería"),
            ("Investigar por qué ocurre antes de sacar una conclusión.", "Ciencias Naturales"),
            ("Revisar las reglas, derechos o normas que podrían estar involucrados.", "Derecho"),
            ("Pensar primero en quién puede verse afectado y cómo ayudarlo.", "Salud Mental"),
        ],
    },
    {
        "texto": "¿Qué tema podría hacer que te quedaras investigando durante horas?",
        "opciones": [
            ("El universo, los seres vivos o los fenómenos naturales.", "Ciencias Naturales"),
            ("Leyes, justicia, derechos y conflictos sociales.", "Derecho"),
            ("Historia, filosofía, literatura o culturas.", "Humanidades"),
            ("Programación, inteligencia artificial, videojuegos o innovación.", "Tecnología"),
        ],
    },
    {
        "texto": "Te dan un presupuesto para crear un proyecto. ¿Cuál elegirías?",
        "opciones": [
            ("Un proyecto de acompañamiento y bienestar para la comunidad.", "Salud Mental"),
            ("Un estudio creativo o proyecto artístico.", "Arte y Diseño"),
            ("Una empresa o emprendimiento.", "Negocios"),
            ("Diseñar y construir una solución para un problema concreto.", "Ingeniería"),
        ],
    },
    {
        "texto": "¿Qué situación te produciría mayor satisfacción?",
        "opciones": [
            ("Saber que ayudaste a una persona a mejorar su salud.", "Salud"),
            ("Conseguir que se haga justicia en una situación complicada.", "Derecho"),
            ("Ver a otras personas disfrutar algo que creaste.", "Arte y Diseño"),
            ("Hacer crecer un proyecto hasta convertirlo en algo exitoso.", "Negocios"),
        ],
    },
    {
        "texto": "Si pudieras aprender una actividad durante un año, ¿cuál elegirías?",
        "opciones": [
            ("Comunicación, periodismo o producción audiovisual.", "Humanidades"),
            ("Historia, literatura, filosofía o idiomas.", "Humanidades"),
            ("Psicología, emociones o relaciones humanas.", "Salud Mental"),
            ("Programación, robótica o inteligencia artificial.", "Tecnología"),
        ],
    },
    {
        "texto": "¿Qué te atraería más de un trabajo que nunca probaste?",
        "opciones": [
            ("Trabajar en contacto con la naturaleza.", "Agronomía"),
            ("Crear o transformar algo de manera original y visual.", "Arte y Diseño"),
            ("Organizar proyectos, negociar y tomar decisiones.", "Negocios"),
            ("Trabajar cuidando personas.", "Salud"),
        ],
    },
    {
        "texto": "¿Qué te gustaría que alguien dijera de vos dentro de 20 años?",
        "opciones": [
            ("Dejó ideas y conocimientos que todavía siguen siendo importantes.", "Humanidades"),
            ("Defendió a quienes necesitaban ayuda.", "Derecho"),
            ("Logró transmitir ideas que llegaron a muchísimas personas.", "Humanidades"),
            ("Ayudó a muchas personas a sentirse comprendidas y acompañadas.", "Salud Mental"),
        ],
    },
    {
        "texto": "Cuando aprendés algo nuevo, ¿qué te genera más curiosidad?",
        "opciones": [
            ("Por qué ocurre determinado fenómeno.", "Ciencias Naturales"),
            ("Cómo puede afectar al cuerpo humano.", "Salud"),
            ("Cómo llevarlo a la práctica.", "Ingeniería"),
            ("Cómo puede influir en las emociones y relaciones.", "Salud Mental"),
        ],
    },
    {
        "texto": "Imaginá que mañana tenés que elegir un lugar para pasar todo el día. ¿Cuál preferís?",
        "opciones": [
            ("Una finca, reserva o espacio natural.", "Agronomía"),
            ("Un estudio de arte o diseño.", "Arte y Diseño"),
            ("Un laboratorio.", "Ciencias Naturales"),
            ("Una empresa o espacio de negocios.", "Negocios"),
        ],
    },
    {
        "texto": "Si supieras que no podés equivocarte, ¿qué te animarías a intentar?",
        "opciones": [
            ("Crear algo que pueda influir en muchas personas.", "Humanidades"),
            ("Defender una causa en la que realmente creo.", "Derecho"),
            ("Construir una solución para un problema importante.", "Ingeniería"),
            ("Crear una tecnología que todavía no existe.", "Tecnología"),
        ],
    },
    {
        "texto": "¿Qué problema del mundo te gustaría poder solucionar?",
        "opciones": [
            ("El deterioro ambiental y la producción poco sustentable.", "Agronomía"),
            ("Las enfermedades y problemas de salud.", "Salud"),
            ("Los problemas emocionales y la falta de acompañamiento.", "Salud Mental"),
            ("La injusticia y la desigualdad ante la ley.", "Derecho"),
        ],
    },
    {
        "texto": "Pensando en tu futuro, ¿qué te gustaría tener más?",
        "opciones": [
            ("Contacto con la naturaleza.", "Agronomía"),
            ("Libertad para crear.", "Arte y Diseño"),
            ("Independencia económica.", "Negocios"),
            ("Tiempo para aprender y reflexionar.", "Humanidades"),
        ],
    },
    {
        "texto": "¿Qué sacrificio estarías más dispuesto/a a hacer por una profesión que realmente te apasionara?",
        "opciones": [
            ("Pasar mucho tiempo estudiando e investigando.", "Ciencias Naturales"),
            ("Estar constantemente frente a personas o exponiéndome públicamente.", "Humanidades"),
            ("Continuar estudiando y profundizando en ideas que me apasionen.", "Humanidades"),
            ("Escuchar y acompañar situaciones emocionales complicadas.", "Salud Mental"),
        ],
    },
    {
        "texto": "¿Qué te preocupa más cuando pensás en elegir una carrera?",
        "opciones": [
            ("No tener estabilidad económica.", "Negocios"),
            ("Quedarme atrás frente a los cambios tecnológicos.", "Tecnología"),
            ("Sentir que mi trabajo no tiene impacto social.", "Salud Mental"),
            ("No poder hacer algo creativo.", "Arte y Diseño"),
        ],
    },
    {
        "texto": "¿Cuál de estas frases se acerca más a tu manera de pensar?",
        "opciones": [
            ("Tenemos que aprender a producir sin destruir lo que tenemos.", "Agronomía"),
            ("Antes de opinar, quiero entender qué está pasando.", "Ciencias Naturales"),
            ("Entender el pasado ayuda a comprender el presente.", "Humanidades"),
            ("Los problemas se solucionan haciendo.", "Ingeniería"),
        ],
    },
    {
        "texto": "Si tuvieras garantizado un buen sueldo en cualquier profesión, ¿qué elegirías?",
        "opciones": [
            ("Trabajar en el cuidado de las personas.", "Salud"),
            ("Comunicar e informar.", "Humanidades"),
            ("Crear y diseñar.", "Arte y Diseño"),
            ("Programar, innovar o trabajar con tecnología.", "Tecnología"),
        ],
    },
    {
        "texto": "¿Qué te gustaría aprender sobre vos mismo antes de elegir una carrera?",
        "opciones": [
            ("Cómo manejo mis emociones y las de los demás.", "Salud Mental"),
            ("Qué tan cómodo/a me siento tomando decisiones y asumiendo riesgos.", "Negocios"),
            ("Aprender sobre prevención y cuidado de la salud.", "Salud"),
            ("Cómo me expreso y cómo logro comunicarme.", "Humanidades"),
        ],
    },
    {
        "texto": "Imaginá tu vida laboral ideal. ¿Qué tendría?",
        "opciones": [
            ("Naturaleza, espacios abiertos y proyectos sustentables.", "Agronomía"),
            ("Cultura, conocimiento y aprendizaje continuo.", "Humanidades"),
            ("Desafíos técnicos y problemas para resolver.", "Ingeniería"),
            ("Tecnología, innovación y herramientas digitales.", "Tecnología"),
        ],
    },
    {
        "texto": "Imaginá que te proponen armar una muestra o evento para tu comunidad. ¿En qué te gustaría colaborar?",
        "opciones": [
            ("En la investigación: elegir el contenido y los datos.", "Ciencias Naturales"),
            ("En lo visual: diseñar la identidad y los carteles.", "Arte y Diseño"),
            ("En la organización: coordinar, presupuestar y comunicar.", "Negocios"),
            ("En la logística: que todo funcione y esté en su lugar.", "Ingeniería"),
        ],
    },
    {
        "texto": "Cuando pensás en el trabajo ideal, ¿qué pesa más para vos?",
        "opciones": [
            ("El contacto con el ambiente y la naturaleza.", "Agronomía"),
            ("Sentir que estoy defendiendo algo importante.", "Derecho"),
            ("Comprender y acompañar a otras personas.", "Salud Mental"),
            ("Trabajar con innovación y tecnología.", "Tecnología"),
        ],
    },
    {
        "texto": "¿Qué esperás encontrar realmente en una profesión?",
        "opciones": [
            ("Un espacio para pensar, aprender y comprender el mundo.", "Humanidades"),
            ("Problemas interesantes que me obliguen a buscar soluciones.", "Ingeniería"),
            ("Una oportunidad para construir independencia y crecimiento.", "Negocios"),
            ("Historias, personas e ideas que pueda comunicar.", "Humanidades"),
        ],
    },
    {
        "texto": "Cuando tenés que tomar una decisión importante, ¿qué suele pesar más?",
        "opciones": [
            ("Cómo puede afectar al ambiente o a otras formas de vida.", "Agronomía"),
            ("Qué sería lo más justo en esa situación.", "Derecho"),
            ("Qué opción es más práctica y funciona mejor.", "Ingeniería"),
            ("Qué solución puedo encontrar utilizando tecnología.", "Tecnología"),
        ],
    },
    {
        "texto": "¿Qué clase de desafío te resulta más atractivo?",
        "opciones": [
            ("Resolver una pregunta difícil mediante investigación.", "Ciencias Naturales"),
            ("Lograr que un mensaje llegue y sea comprendido por muchas personas.", "Humanidades"),
            ("Convertir una idea en un proyecto exitoso.", "Negocios"),
            ("Encontrar una forma de mejorar la vida o salud de alguien.", "Salud"),
        ],
    },
    {
        "texto": "Dentro de diez años, ¿qué te gustaría pensar al mirar hacia atrás?",
        "opciones": [
            ("Hice algo para cuidar nuestro planeta.", "Agronomía"),
            ("Creé cosas que realmente representan quién soy.", "Arte y Diseño"),
            ("Nunca dejé de aprender y cuestionarme.", "Humanidades"),
            ("Construí cosas que realmente funcionan.", "Ingeniería"),
        ],
    },
    {
        "texto": "¿Qué preferirías hacer durante una jornada de trabajo?",
        "opciones": [
            ("Analizar información y hacer experimentos.", "Ciencias Naturales"),
            ("Entrevistar, grabar, escribir o comunicar.", "Humanidades"),
            ("Conversar y acompañar personas.", "Salud Mental"),
            ("Programar, probar herramientas o desarrollar tecnología.", "Tecnología"),
        ],
    },
    {
        "texto": "¿Cuál de estas preguntas te genera más curiosidad?",
        "opciones": [
            ("¿Cómo podemos vivir y producir sin destruir el ambiente?", "Agronomía"),
            ("¿Por qué ocurre determinado fenómeno?", "Ciencias Naturales"),
            ("¿Qué hace que una situación sea realmente justa?", "Derecho"),
            ("¿Qué podría llegar a hacer una tecnología que todavía no existe?", "Tecnología"),
        ],
    },
    {
        "texto": "Si pudieras mejorar una sola habilidad tuya, ¿cuál elegirías?",
        "opciones": [
            ("Comunicarme y expresarme mejor.", "Humanidades"),
            ("Resolver problemas prácticos.", "Ingeniería"),
            ("Liderar y tomar mejores decisiones.", "Negocios"),
            ("Comprender mejor las emociones.", "Salud Mental"),
        ],
    },
    {
        "texto": "Si pudieras cambiar algo de tu comunidad, ¿qué elegirías?",
        "opciones": [
            ("Mejorar los espacios verdes y el cuidado ambiental.", "Agronomía"),
            ("Ayudar a que las personas conozcan y defiendan sus derechos.", "Derecho"),
            ("Mejorar el acceso a la salud.", "Salud"),
            ("Mejorar la forma en que la comunidad se informa y comunica.", "Humanidades"),
        ],
    },
    {
        "texto": "Última pregunta: si nadie pudiera juzgarte por tu elección, ¿qué camino sentís que te gustaría explorar?",
        "opciones": [
            ("Arte, diseño, música o creatividad.", "Arte y Diseño"),
            ("Humanidades, cultura, historia, filosofía o literatura.", "Humanidades"),
            ("Ingeniería, construcción o resolución de problemas técnicos.", "Ingeniería"),
            ("Programación, informática, inteligencia artificial o tecnología.", "Tecnología"),
        ],
    },
]
