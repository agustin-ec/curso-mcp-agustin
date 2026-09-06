## Reflexión sobre la orquestación

**1. ¿En qué se sintió distinto invocar "agentes" comparado con invocar "skills" sueltas?**
La skill tiene capacidad puntual, sin personalidad, sin criterio propio — hace lo que le piden, no decide nada por su cuenta. El agente, en cambio, tiene rol, criterio y reglas de comportamiento propias.

Se notó al invocar al tester-agent: razonó sobre su rol ("Reviewing testing agent instructions") antes de actuar, algo que las skills sueltas de Spec Kit nunca hacían.

**2. ¿Qué pasaría si el security-agent intentara modificar tus tests? ¿Podría, con la configuración que armaron?**
Con la configuración de mínimo privilegio (tools: qa-security únicamente), el security-agent no debería poder tocar los tests. Sin embargo, ya vi un caso relacionado: el tester-agent
(no el security-agent) editó ordenes-agentes.md marcando sus propios checkboxes como [x], un archivo que su orden de trabajo no mencionaba explícitamente que pudiera modificar.

Esto muestra que un agente puede salirse de su alcance aunque su configuración de herramientas (tools:) sea restringida — la restricción de tools limita qué SKILLS puede usar, pero no necesariamente qué ARCHIVOS puede tocar directamente.

**3. Tú fuiste el orquestador hoy — invocando a cada agente en el momento correcto. ¿Cómo sería si otro agente (no ustedes) decidiera ese orden?**
Sería automatizar de forma completa el uso de los agentes con sus respectivas skills en el momento en que se los requiera.


## Hooks vs. Skills: no son competencia, son de naturaleza distinta

Un **hook** es como una alarma de humo — no piensa, no interpreta, no decide nada creativo. Solo revisa una condición fija ("¿hay humo? sí/no") y reacciona automáticamente sin que nadie se lo pida. Por eso no consume tokens: es puro código, sin ningún modelo de IA involucrado en el momento de ejecutarse.

Una **skill**, en cambio, casi siempre necesita que el agente interprete y genere algo nuevo. Mira qa-unit: su instrucción es "lee test-spec.md y genera un test que cumpla exactamente cada punto" — eso requiere que un modelo entienda tu spec en lenguaje natural y escriba código de prueba original. Una alarma de humo no puede escribir un ensayo; un hook tampoco puede "entender" tu spec y crear algo a partir de ella.

Un hook no puede reemplazar a una skill, porque hacen trabajos fundamentalmente distintos:

| | **Hook** | **Skill** |
| **¿Piensa o interpreta?**	| No, lógica fija |	Sí, necesita al modelo |
| **¿Consume tokens?** | No | Sí |
| **¿Puede generar código nuevo?** | No | Sí |
| **¿Cuándo actúa?** | Automático, en un momento fijo (ej. después de editar)	| Cuando el agente decide invocarla |
| **Ejemplo** |	gate-tests.sh (bloquea si algo falla) |	qa-unit (genera tests desde tu spec) |

Se complementan: el hook es el "guardián barato" que aplica una regla siempre, sin excepción y sin costo; la skill es el "trabajador con criterio" que hace algo que requiere comprensión.

## Hallazgo: el hook no se activó como se esperaba

Al configurar `hooks.json` con `"matcher": "edit_file|write_file"`, el hook nunca se activó tras las ediciones del agente. Al revisar la transcripción, la herramienta real que usa `agy` se llama `Edit` (no `edit_file`), así que corregí el matcher a `"Edit|Write"`. Aun así, el hook no se activó en la misma sesión.

Hipótesis: los hooks se cargan solo al iniciar la sesión de `agy`, así que el cambio requiere reiniciar la sesión para tomar efecto. 

Intento 2:
Se reinició la sesión en agy y se confirma que: el hook definitivamente no se está activando, ni con el nombre corregido ni con la sesión reiniciada.

Hipótesis: (Probablemente) el problema no es de sintaxis, sino de que agy simplemente no soporta hooks todavía, o la sintaxis correcta es distinta a la de Claude Code (para la que fue hecha la guía)

## Comparación: agentes a mano vs. /qa-orchestrate

Con /qa-orchestrate, los 3 agentes corrieron en secuencia con un solo comando, sin intervención manual entre fases. Sin embargo, como el hook no funciona en agy, la cadena NO se detuvo al fallar 4 tests -siguió hasta el Report-Agent de todas formas.

Esto confirma que "automático" no es sinónimo de "seguro": sin el hook como freno, la orquestación avanza igual aunque el código esté roto, algo que en Claude Code (con el hook activo) se habría detenido en el Tester-Agent.

## Cierre

**1. ¿Cuál fue el veredicto final?**
Definidas correctamente las skills (habilidades), los agentes y el agente orquestador, nuestro código no mostrará resultados no deseados, cumpliendo la premisa de que todo programa debe ser definido.

Realizar las auditorías de seguridad y de errores en el código, nos ayuda a entregar un proyecto pulido y documentado antes de entrar a su etapa de producción.

Los hooks no son una herramienta standard; es decir, probablemente todos los modelos no los tengan implementados o su sintaxis es distinta.
 
**2. Completa: "El inspector encontró ...**
... que al código del proyecto le faltaba mejorar la validación del dato de entrada; en este caso, que no se acepten datos de tipo boolean, ni valores no finitos.


