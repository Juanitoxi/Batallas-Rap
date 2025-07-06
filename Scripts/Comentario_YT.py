import googleapiclient.discovery

youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey='AIzaSyCfPY53C9vfSyyauBrN14IDBecDrDqZqxU')

# Crear una solicitud para obtener el video
video_id = input("Video_Id: ")


# Inicializa variables para la paginación
next_page_token = ''
comments = []

while True:
    # Realiza una solicitud para obtener los comentarios con la página siguiente
    comments_response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100,  # Establece el número máximo de comentarios por página
        pageToken=next_page_token  # Utiliza el token de página siguiente
    ).execute()

    # Agrega los comentarios de la página actual a la lista
    comments.extend(comments_response['items'])

    # Obtiene el token de página siguiente
    next_page_token = comments_response.get('nextPageToken')

    # Si no hay más comentarios, detén el bucle
    if not next_page_token:
        break

# Imprime el total de comentarios y enumera e imprime los comentarios
total_comments = len(comments)
print(f"Total de comentarios: {total_comments}")
for index, comment in enumerate(comments, start=1):
    text = comment['snippet']['topLevelComment']['snippet']['textOriginal']
    print(f"{index}: {text}")