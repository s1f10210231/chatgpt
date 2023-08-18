from django.shortcuts import render
from django.http import HttpResponse
import openai
from .models import Novel

openai.api_key = 'h6dzGnbQK82rizBXxHwruBY53JESXoPlUK8ydpL7Tb9om1SJlrVfyaZwPt2bUnVQab6_ParXOsla4RkO-yUnzLQ'
openai.api_base = 'https://api.openai.iniad.org/api/v1'

# Create your views here.

def index(request):
    return render(request,"story_app/index.html")

def generate_novel(genre,where,when,who,how):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[{"role": "system", "content": "You are a genius japanese novelist."},
                    {"role": "user", "content": f"Write a novel in the {genre} genre in japanese.And Please make a story in {where} with a development that {how}"},
                    {"role": "user", "content": f"The hero's setting is a {who}"},
                    {"role": "user", "content": f"The time setting is {when}."},
                    {"role":"user","content":"Don't show the title."},
                    {"role":"user","content":"Consider only the first episode."}

                    
                    ],
        max_tokens=500

    )

    return response['choices'][0]['message']['content']

def title_create(title):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[ {"role": "system", "content": "You are a genius japanese novelist."},
                    {"role": "user", "content": f"Think of the title {title} in 10 Japanese characters or less."}
                    
                    ],
        max_tokens=30
    )
    return response['choices'][0]['message']['content']

def create(request):
    if request.method == 'POST':
        input_genre = request.POST.get('genre_input', '')
        input_who = request.POST.get('who_input', '')
        input_where = request.POST.get('where_input', '')
        input_when = request.POST.get('when_input', '')
        input_how = request.POST.get('how_input', '')


        genre_text = "\n".join(input_genre)
        who_text = "\n".join(input_who)
        where_text = "\n".join(input_where)
        when_text = "\n".join(input_when)
        how_text = "\n".join(input_how)


        generated_novel = generate_novel(genre_text,where_text,when_text,who_text,how_text)

        title_novel = title_create(generated_novel)

        if generated_novel:
            novel = Novel(genre=input_genre, content=generated_novel,title=title_novel)
            novel.save()
 

        content = {
            "novels": Novel.objects.all(),
            'generated_novel': generated_novel,
            'title':title_novel
        }
        return render(request, "story_app/create.html", content)
    else:
        content = {"novels": Novel.objects.all()}
        return render(request, 'story_app/create.html', content)