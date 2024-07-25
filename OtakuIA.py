import requests,csv,json,re
from groq import Groq


headers = {
    'X-MAL-CLIENT-ID': "00c6b41a52aa408f83141cc134982cfc",
    }

# Haz la solicitud GET
def get_anime(anime: str):
    maf_api_url = f"https://api.myanimelist.net/v2/anime?q={anime}&fields=synopsis,mean,rank,popularity,num_list_users,num_scoring_users,related_anime,related_manga,media_type,num_episodes,num_chapters,num_volumes,status,start_date,end_date,start_season,broadcast,studios,source,genres,average_episode_duration,serialization"
    response = requests.get(maf_api_url, headers=headers)
    anime_info = response.json()
    data = json.dumps(anime_info, indent=4)
    return f"El nombre del anime es: {anime} y el json es: {data}"


#Solo debes pasarle por parámetro el anime deseado

anime = get_anime("Death Note")



client = Groq(api_key= "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")

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": f""" eres un asistente con la siguiente tarea:
            dado el siguiente json que te proporcionaré puntos que debes cumplir:
            1) todo tiene que estar traducido al español sin perder la calidad
            de la sinopsis.
            2) convertir todo el json a texto y solo dar la informacion pedida del anime de de tal manera que quede la siguiente estructura donde absolutamente todo debe estar traducido al español (nota, los paréntesis se utilizan para dar aclarar instrucciones y debes acatarlas.)
            3) el formato de fecha debe ser dias/meses/años
            4) si el autor de la obra no existe en el json, autocompletar con el autor del anime
            5) donde dice "basado en"debes poner si esta basado en una novela ligera, manga,si es original o lo que corresponda según el json
            6) evitar saltos de linea dobles e innecesarios
            7) (si está finalizado no añadir y si lo está usar el horario para GMT-3 ARGENTINA y dar la siguiente aclaración: los horarios estan sujetos a errores y pueden ser imprecisos)
            8) usar * está estricamente prohibido prohibido
            9) si no se especifica una temporada en particular realizar lo pedido usando la primera temporada.
            10) Si el anime que se pide no existe en el json
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
            
            """,
        }
    ],
    model="gemma-7b-it", # Recomendación: No usar modelos de lenguajes grandes ya que el output suele ser de mala calidad.
    #Recomiendo MIxtral y Gemma 7b
)
temperature = 1 
max_tokens = 4000
top_p = 0.1 #0.1 recomendado
stop = None
stream = False
resultado = re.sub(r'\*{1,2}', '', chat_completion.choices[0].message.content) #limpia los * del archivo final.

with open("resultadoIA.txt","w+", encoding="UTF-8") as archivo:
    archivo.writelines(resultado)

# Mensaje super secreto de desarrolador.



