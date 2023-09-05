from django.shortcuts import render
import openai
import requests
from .models import Novel,NovelImage
from collections import defaultdict
from django.http import Http404

from django.core.files.base import ContentFile




openai.api_key = '6sVanUSz6_O1xHHq5BxslXRVW8jFYx93uSzqNXSI7KHni7q8BViv1ec8YMS4Cfc2pUr4sH0gZPTtTPtVd70M7pA'
openai.api_base = 'https://api.openai.iniad.org/api/v1'

# Create your views here.



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


def translation(text):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[{"role": "system", "content": "you are the translator If you have Japanese text, you can convert it to English."},
                    {"role":"user","content":f"Translate the {text} from Japanese to English.At that time, please display only the translated version."}

                    
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

# トップページ
def index(request):
    novels = Novel.objects.all()

    grouped_by_genre = defaultdict(list)
    for novel in novels:
        genre = novel.genre
        grouped_by_genre[genre].append(novel)
    
    unique_by_genre = {}
    for genre, novels in grouped_by_genre.items():
        unique_by_genre[genre] = list(set(novels))

    content = {
        "genres_and_novels": unique_by_genre,
    }
    return render(request, "story_app/index.html", content)

# 投稿ページ
def create(request):
    if request.method == 'POST':
        
        form_type = request.POST.get('formType', '')  # フォームの種類を取得

        if form_type == 'userInput':
                # ユーザー手動入力フォームからのデータを取得
                genre = request.POST.get('genre_input', '')
                who = request.POST.get('who_input', '')
                where = request.POST.get('where_input', '')
                when = request.POST.get('when_input', '')
                how = request.POST.get('how_input', '')


        elif form_type == 'autoInput':
                # 組み合わせ選択フォームからのデータを取得
                genre = request.POST.get('genre','')  # リストとして取得されるので getlist を使用
                who = request.POST.get('whose', '')
                where = request.POST.get('where', '')
                when = request.POST.get('when', '')
                how = request.POST.get('how', '')
        else:
                # ユーザー手動入力フォーム以外の場合、適切な初期値を設定
                genre = ''
                who = ''
                where = ''
                when = ''
                how = ''
                            
        genre_text = "\n".join(genre)
        who_text = "\n".join(who)
        where_text = "\n".join(where)
        when_text = "\n".join(when)
        how_text = "\n".join(how)


        generated_novel = generate_novel(genre_text,where_text,when_text,who_text,how_text)
        title_novel = title_create(generated_novel)

        img_url =  "https://source.unsplash.com/180x90?" + str(translation(title_novel)) 

        response = requests.get(img_url)
        if response.status_code == 200:
            novel_image = NovelImage(image_text=title_novel)
            novel_image.image.save(f'{title_novel}.jpg', ContentFile(response.content), save=True)
        
        novel_images = NovelImage.objects.all()

        if generated_novel:
            novel = Novel(genre=genre, content=generated_novel,title=title_novel,image=novel_image)
            novel.save()
    

        content = {
            "novels": Novel.objects.all(),
            'generated_novel': generated_novel,
            'title':title_novel,
            "images":novel_images,
        }
        return render(request, "story_app/create.html", content)
    else:
        content = {"novels": Novel.objects.all()}
        return render(request, 'story_app/create.html', content)
    
def browse(request):
    return render(request, "story_app/browse.html")


def detail(request, novel_id):
    try:
        novel = Novel.objects.get(pk=novel_id)
    except Novel.DoesNotExist:
        raise Http404("Novel does not exist")
    
    context = {
        "novel": novel,
    }
    return render(request, "story_app/detail.html", context)