import requests
import json

def obtener_token():
    # Aquí debes incluir la lógica para obtener tu token de acceso
    # Puedes usar el explorador de tokens de acceso de Facebook para obtener uno: https://developers.facebook.com/tools/explorer/
    return 'EAADdUDROBlkBO4BVr8woQ5xmbkacVCqg27u2vVHcSOGYxOZC8sVU3ARUhevIIitRzTywniEuEqzJYZBU3ZA5HY4nmi4xCZBXx17EM7bh9LE9qo8TQJQTPh0fZBxgdxmkYn5sshEjX97jNXxZBxJvKwrBsv1ywc8UrF3CsQCQsX8YzUHwhy7IVflnzvoPonEcvaMPoBz6F7Pman6Sp7LP9R7jJH6FzlBqgmfA3n3AZDZD'

def obtener_conversaciones_pagina(token, pagina_id, profundidad=5, cursor=None):
    conversaciones_totales = []

    if profundidad <= 0:
        return

    endpoint = f"https://graph.facebook.com/v13.0/{pagina_id}/conversations"
    parametros = {
        'access_token': token,
        'limit': 25,  # Puedes ajustar el límite según tus necesidades
        'after': cursor
    }

    try:
        respuesta = requests.get(endpoint, params=parametros)
        respuesta.raise_for_status()
        datos = respuesta.json()

        if 'data' in datos:
            # Procesar las conversaciones aquí
            for conversacion in datos['data']:
                id_conversacion = conversacion['id']
                print(f"ID de Conversación: {id_conversacion}")

                # Obtener mensajes de la conversación
                endpoint_mensajes = f"https://graph.facebook.com/v13.0/{id_conversacion}/messages"
                parametros_mensajes = {
                    'access_token': token,
                    'fields': 'from,created_time,message'
                }

                respuesta_mensajes = requests.get(endpoint_mensajes, params=parametros_mensajes)
                respuesta_mensajes.raise_for_status()
                datos_mensajes = respuesta_mensajes.json()

                # Procesar los mensajes
                if 'data' in datos_mensajes:
                    for mensaje in datos_mensajes['data']:
                        remitente = mensaje.get('from', {}).get('name', 'Desconocido')
                        fecha_creacion = mensaje.get('created_time', 'Fecha desconocida')
                        contenido = mensaje.get('message', 'Mensaje desconocido')

                        print(f"Remitente: {remitente}")
                        print(f"Fecha de Creación: {fecha_creacion}")
                        print(f"Contenido del Mensaje: {contenido}")
                        print("---")

                        # Guardar información en la lista
                        conversaciones_totales.append({
                            'ID de Conversación': id_conversacion,
                            'Remitente': remitente,
                            'Fecha de Creación': fecha_creacion,
                            'Contenido del Mensaje': contenido
                        })

            # Verificar si hay más páginas de resultados
            if 'paging' in datos and 'next' in datos['paging']:
                next_cursor = datos['paging']['cursors']['after']
                obtener_conversaciones_pagina(token, pagina_id, profundidad - 1, next_cursor)
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener conversaciones: {e}")

    # Guardar la lista de conversaciones en un archivo JSON
    with open('conversaciones_totales.json', 'w') as archivo_json:
        json.dump(conversaciones_totales, archivo_json, indent=2)

if __name__ == "__main__":
    token_acceso = obtener_token()
    pagina_id = '1643204302616358'  # Reemplaza con el ID de tu página

    obtener_conversaciones_pagina(token_acceso, pagina_id)
