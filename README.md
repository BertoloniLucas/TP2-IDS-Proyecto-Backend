# TP2-IDS-Proyecto-Backend

Trabajo Práctico Nro 2 - Proyecto Backend (API).

Se puede acceder al enunciado acá abajo: 

[Ver PDF del enunciado](Informe_Proyecto_Backend_IDS.pdf)

La aplicación Flask se levanta desde [app_backend/app.py](app_backend/app.py) y expone tres grupos de endpoints:

- `/usuarios`
- `/partidos`
- `/ranking`

## Requisitos y ejecución

Antes de correr la API, instalá las dependencias definidas en `requirements.txt`.

La app principal está en [app_backend/app.py](app_backend/app.py), por lo que lo normal es ejecutar el proyecto desde esa carpeta:

```bash
cd app_backend
python app.py
```

Por defecto, el servidor corre en `http://localhost:5000`.

## Convenciones generales

- Las respuestas exitosas devuelven JSON.
- Los errores también devuelven JSON con una clave `error` o `mensaje`, según el caso.
- Los endpoints de listado usan paginación con `_limit` y `_offset`.
- En varios endpoints de creación se devuelve además un header `Location` con la ruta del recurso creado.

## Endpoints de usuarios

Base path: `/usuarios`

### `GET /usuarios/`

Devuelve el listado paginado de usuarios.

Query params:

- `_limit` opcional, entero. Default: `10`. Máximo: `100`.
- `_offset` opcional, entero. Default: `0`.

Respuesta `200`:

```json
{
	"usuarios": [
		{
			"id": 1,
			"nombre": "Juan Perez",
			"email": "juan@correo.com"
		}
	],
	"_links": {
		"_first": { "href": "http://localhost:5000/usuarios/?_limit=10&_offset=0" },
		"_last": { "href": "http://localhost:5000/usuarios/?_limit=10&_offset=20" },
		"_prev": { "href": "http://localhost:5000/usuarios/?_limit=10&_offset=0" },
		"_next": { "href": "http://localhost:5000/usuarios/?_limit=10&_offset=10" }
	}
}
```

Notas:

- `_prev` solo aparece si `_offset > 0`.
- `_next` solo aparece si todavía hay más registros.

Posibles códigos de estado:

- `200`: OK.
- `500`: error inesperado.

### `POST /usuarios/`

Crea un usuario nuevo.

Body JSON:

```json
{
	"nombre": "Juan Perez",
	"email": "juan@correo.com"
}
```

Validaciones:

- El body no puede estar vacío.
- `nombre` es obligatorio y no puede ser vacío.
- `email` es obligatorio y debe contener `@`.
- No puede existir otro usuario con el mismo email.

Respuesta `201`:

```json
{
	"id": 1,
	"nombre": "Juan Perez",
	"email": "juan@correo.com"
}
```

Header adicional:

- `Location: /usuarios/<id>`

Posibles códigos de estado:

- `201`: creado correctamente.
- `400`: body vacío, campo faltante, nombre inválido o email inválido.
- `500`: error inesperado.

### `GET /usuarios/<usuario_id>`

Devuelve un usuario por id.

Respuesta `200`:

```json
{
	"id": 1,
	"nombre": "Juan Perez",
	"email": "juan@correo.com"
}
```

Posibles códigos de estado:

- `200`: usuario encontrado.
- `404`: usuario no encontrado.
- `500`: error inesperado.

### `PUT /usuarios/<usuario_id>`

Actualiza un usuario existente.

Body JSON:

```json
{
	"nombre": "Juan Nuevo",
	"email": "juan.nuevo@correo.com"
}
```

Validaciones:

- El body no puede estar vacío.
- Debe venir al menos uno de los campos esperados, aunque la implementación actual exige `nombre` y `email` válidos para completar la actualización.
- `nombre` no puede ser vacío.
- `email` debe contener `@`.
- El email no puede estar en uso por otro usuario.
- El usuario debe existir.

Respuesta `200`:

```json
{
	"message": "Usuario actualizado correctamente"
}
```

Posibles códigos de estado:

- `200`: actualizado correctamente.
- `400`: body vacío, campos inválidos o email duplicado.
- `404`: usuario no encontrado.
- `500`: error inesperado.

### `DELETE /usuarios/<usuario_id>`

Elimina un usuario. Antes borra sus predicciones asociadas.

Respuesta `200`:

```json
{
	"message": "Usuario eliminado correctamente"
}
```

Posibles códigos de estado:

- `200`: eliminado correctamente.
- `404`: usuario no encontrado.
- `500`: error inesperado.

## Endpoints de partidos

Base path: `/partidos`

### `GET /partidos/`

Devuelve el listado paginado de partidos con filtros opcionales.

Query params:

- `fecha` opcional, formato `YYYY-MM-DD`.
- `fase` opcional.
- `equipo` opcional. Filtra por nombre del equipo local o visitante.
- `_limit` opcional, entero. Default: `10`.
- `_offset` opcional, entero. Default: `0`.

Respuesta `200`:

```json
{
	"partidos": [
		{
			"ID": 1,
			"equipo_local": "Argentina",
			"equipo_visitante": "Brasil",
			"fecha": "2026-06-01",
			"fase": "Grupos"
		}
	],
	"_links": {
		"_first": { "href": "http://localhost:5000/partidos/?_limit=10&_offset=0" },
		"_last": { "href": "http://localhost:5000/partidos/?_limit=10&_offset=20" },
		"_prev": { "href": "http://localhost:5000/partidos/?_limit=10&_offset=0" },
		"_next": { "href": "http://localhost:5000/partidos/?_limit=10&_offset=10" }
	}
}
```

Los links de paginación conservan los filtros enviados.

Posibles códigos de estado:

- `200`: OK.
- `500`: error inesperado.

### `POST /partidos/`

Crea un partido.

Body JSON:

```json
{
	"equipo_local": "Argentina",
	"equipo_visitante": "Brasil",
	"fecha": "2026-06-01",
	"fase": "Grupos"
}
```

Validaciones:

- El body no puede estar vacío.
- Deben venir `equipo_local`, `equipo_visitante`, `fecha` y `fase`.
- Los equipos deben existir.
- `equipo_local` y `equipo_visitante` no pueden ser iguales.
- `fecha` debe tener formato `YYYY-MM-DD`.

Respuesta `201`:

```json
{
	"ID": 1,
	"equipo_local": 2,
	"equipo_visitante": 5,
	"fecha": "2026-06-01",
	"fase": "Grupos"
}
```

Header adicional:

- `Location: /partidos/<id>`

Posibles códigos de estado:

- `201`: creado correctamente.
- `400`: body vacío, campos faltantes, equipos inválidos, equipos inexistentes o fecha inválida.
- `500`: error inesperado.

### `GET /partidos/<partido_id>`

Devuelve el detalle de un partido, incluyendo el resultado si existe.

Respuesta `200`:

```json
{
	"id": 1,
	"equipo_local": "Argentina",
	"equipo_visitante": "Brasil",
	"fecha": "2026-06-01",
	"fase": "Grupos",
	"resultado": {
		"goles_local": 2,
		"goles_visitante": 1
	}
}
```

Si no hay resultado cargado, `resultado` devuelve `null`.

Posibles códigos de estado:

- `200`: partido encontrado.
- `404`: partido no encontrado.
- `500`: error inesperado.

### `DELETE /partidos/<partido_id>`

Elimina un partido. También borra sus resultados y predicciones asociadas.

Respuesta `200`:

```json
{
	"mensaje": "Partido eliminado correctamente"
}
```

Posibles códigos de estado:

- `200`: eliminado correctamente.
- `404`: partido no encontrado.
- `500`: error inesperado.

### `PATCH /partidos/<partido_id>`

Actualiza uno o más campos del partido.

Body JSON posible:

```json
{
	"equipo_local": "Argentina",
	"fecha": "2026-06-10",
	"fase": "Cuartos"
}
```

Campos permitidos:

- `equipo_local`
- `equipo_visitante`
- `fecha`
- `fase`

Validaciones:

- El body no puede estar vacío.
- El partido debe existir.
- Si se envía `equipo_local` o `equipo_visitante`, el equipo debe existir.
- Si se envía `fecha`, debe tener formato `YYYY-MM-DD`.
- Si se envían ambos equipos, no pueden quedar iguales.

Respuesta `200`:

```json
{
	"mensaje": "Partido actualizado correctamente"
}
```

Posibles códigos de estado:

- `200`: actualizado correctamente.
- `400`: body vacío, no hay campos para actualizar, fecha inválida o equipos inválidos.
- `404`: partido no encontrado.
- `500`: error inesperado.

### `PUT /partidos/<partido_id>/resultados`

Crea o actualiza el resultado de un partido.

Body JSON:

```json
{
	"goles_local": 2,
	"goles_visitante": 1
}
```

Validaciones:

- El body no puede estar vacío.
- Deben venir `goles_local` y `goles_visitante`.
- Los goles no pueden ser negativos.
- El partido debe existir.

Respuesta `200`:

```json
{
	"mensaje": "Resultado actualizado correctamente",
	"resultado": {
		"ID": 1,
		"id_partido": 1,
		"goles_local": 2,
		"goles_visitante": 1
	}
}
```

Posibles códigos de estado:

- `200`: creado o actualizado correctamente.
- `400`: body vacío, campos faltantes o goles negativos.
- `404`: partido no encontrado.
- `500`: error inesperado.

### `POST /partidos/<partido_id>/prediccion`

Registra la predicción de un usuario para un partido.

Body JSON:

```json
{
	"id_usuario": 1,
	"local": 2,
	"visitante": 1
}
```

Validaciones:

- El body no puede estar vacío.
- Deben venir `id_usuario`, `local` y `visitante`.
- El partido debe existir.
- El partido no puede estar ya jugado. La validación actual compara la fecha del partido con la fecha actual.
- El usuario debe existir.
- El usuario no puede tener ya una predicción para ese partido.

Respuesta `200`:

```json
{
	"mensaje": "prediccion agregada correctamente",
	"prediccion": {
		"ID": 1,
		"partido_id": 1,
		"local": 2,
		"visitante": 1,
		"usuario_id": 1
	}
}
```

Posibles códigos de estado:

- `200`: predicción cargada correctamente.
- `400`: body vacío, campos faltantes, partido ya jugado o predicción duplicada.
- `404`: partido inexistente o usuario inexistente.
- `500`: error inesperado.

## Endpoints de ranking

Base path: `/ranking`

### `GET /ranking/`

Devuelve el ranking de usuarios ordenado por puntos descendentes.

Los puntos se calculan así:

- `3` puntos por acertar exactamente el resultado.
- `1` punto por acertar el signo del partido: victoria local, empate o victoria visitante.
- `0` puntos en cualquier otro caso.

Query params:

- `_limit` opcional, entero. Default: `10`.
- `_offset` opcional, entero. Default: `0`.

Respuesta `200`:

```json
{
	"ranking": [
		{
			"id": 1,
			"nombre": "Juan Perez",
			"puntos": 12
		}
	],
	"_links": {
		"_first": { "href": "http://localhost:5000/ranking/?_limit=10&_offset=0" },
		"_last": { "href": "http://localhost:5000/ranking/?_limit=10&_offset=20" },
		"_prev": { "href": "http://localhost:5000/ranking/?_limit=10&_offset=0" },
		"_next": { "href": "http://localhost:5000/ranking/?_limit=10&_offset=10" }
	}
}
```

Posibles códigos de estado:

- `200`: OK.
- `500`: error inesperado.

## Aclaraciones del equipo: 

Creemos que una mejora a imlpementar podría ser la de agregar un ´ON DELETE CASCADE´
para no tener que ir borrando registros asociados a otro registro que haya sido 
eliminado.

