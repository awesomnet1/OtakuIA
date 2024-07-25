import requests,csv,json,re
from groq import Groq


headers = {
    'X-MAL-CLIENT-ID': "api_key",
    }

def get_anime(anime: str):
    maf_api_url = f"https://api.myanimelist.net/v2/anime?q={anime}&fields=synopsis,mean,rank,popularity,num_list_users,num_scoring_users,related_anime,related_manga,media_type,num_episodes,num_chapters,num_volumes,status,start_date,end_date,start_season,broadcast,studios,source,genres,average_episode_duration,serialization"
    response = requests.get(maf_api_url, headers=headers)
    anime_info = response.json()
    data = json.dumps(anime_info, indent=4)
    return f"El nombre del anime es: {anime} y el json es: {data}"



anime = get_anime("escribe tu anime")



client = Groq(api_key= "api_key")

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": f""" eres un asistente con la siguiente tarea:
            dado el siguiente json que te proporcionaré puntos que debes cumplir:
            1) todo tiene que estar traducido al español
            2) convertir todo el json a texto y solo dar la informacion pedida del anime
            3) el formato de fecha debe ser dias/meses/años
            4) si el autor de la obra no existe en el json, autocompletar con el autor del anime
            5) donde dice "basado en"debes poner si esta basado en una novela ligera, manga,si es original o lo que corresponda según el json
            6) evitar saltos de linea dobles e innecesarios
            7) (si está finalizado no añadir y si lo está usar el horario para GMT-3 ARGENTINA y dar la siguiente aclaración: los horarios estan sujetos a errores y pueden ser imprecisos)
            8) si no se especifica una temporada en particular realizar lo pedido usando la primera temporada.
            9) Si el anime que se pide no existe en el json
                {anime}
Nombre Del Anime:
Género:
Calificación:
Sinopsis:
Fecha de estreno:
Estudio de Animación:
Autor/a:
Esta basado en: 
Horario De emisión:
            
            """
        },
        client.chat.completions.create(
            messages
        )
    ],
    model="gemma-7b-it", # Recomendación: No usar modelos de lenguajes grandes ya que el output suele ser de mala calidad.
    #Recomiendo MIxtral y Gemma 7b
)
temperature = 1 
max_tokens = 4000
top_p = 0.1
stop = None
stream = False
resultado = re.sub(r'\*{1,2}', '', chat_completion.choices[0].message.content) #limpia los * del archivo final.

with open("resultadoIA.txt","w+", encoding="UTF-8") as archivo:
    archivo.writelines(resultado)
    



