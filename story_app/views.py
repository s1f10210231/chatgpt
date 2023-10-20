from django.shortcuts import render, redirect
import openai
import requests
from .models import Novel,NovelImage
from collections import defaultdict
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.base import ContentFile
from .forms import NovelEditForm




openai.api_key = '6sVanUSz6_O1xHHq5BxslXRVW8jFYx93uSzqNXSI7KHni7q8BViv1ec8YMS4Cfc2pUr4sH0gZPTtTPtVd70M7pA'
openai.api_base = 'https://api.openai.iniad.org/api/v1'

# Create your views here.



def generate_novel(genre,where,when,who,how):
    response = openai.ChatCompletion.create(
        model = 'gpt-3.5-turbo',
        messages=[{"role": "system", "content": "あなたは1500文字を専門とする天才的な日本の短編作家です。制約条件を絶対に守り命令文に従ってください"},
                    {"role": "user", "content": f'''
                    #制約条件
                    ・主人公の設定は{who}とすること。
                    ・小説は日本語
                    ・時間設定は {when} 。
                    ・タイトルを表示しない。
                    ・お話は一つだけで、一話完結。次回には続かない。
                    ・起承転結
                    ・ジャンルは{genre}。
                    ・場面設定は{where}。
                    ・{how}のような展開にすること。
                    #命令文
                    以上の制約条件を絶対に守り、三十段落程度の短編小説を書いてください。

                    #出力

                    --本文--
                    '''},
                    ],
        max_tokens=1500

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
    novels_time= Novel.objects.all().order_by('-created_at')
    grouped_by_genre = defaultdict(list)
    for novel in novels:
        genre = novel.genre
        grouped_by_genre[genre].append(novel)
    
    unique_by_genre = {}
    for genre, novels in grouped_by_genre.items():
        unique_by_genre[genre] = list(set(novels))

    content = {
        "genres_and_novels": unique_by_genre,
        "novel_time":novels_time,
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

            # 作成された小説のIDを取得
            novel_id = novel.id

            # display_novel ページにリダイレクト
            return redirect('display_novel', novel_id=novel_id)

        content = {
            "novels": Novel.objects.all(),
            'generated_novel': generated_novel,
            'title':title_novel,
            "images":novel_images,
            "novel_id": novel_id,
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

def display_novel(request, novel_id):
    novel = Novel.objects.get(id=novel_id)

    if request.method == 'POST':
        form = NovelEditForm(request.POST, instance=novel)
        if form.is_valid():
            form.save()
    else:
        form = NovelEditForm(instance=novel)

    return render(request, 'story_app/display_novel.html', {'novel': novel, 'form': form})

def like(request, novel_id):
    try:
        novel = Novel.objects.get(pk=novel_id)
        novel.like += 1
        novel.save()
    except Novel.DoesNotExist:
         raise Http404("Novel does not exist")
    
    context = {
        "novel": novel,
    }
    
    return render(request, "story_app/detail.html", context)


def genre_page(request, genre):
    # ジャンルに基づいて小説をフィルタリング
    novels = Novel.objects.filter(genre=genre)

    content={
        'novels': novels, 'genre': genre}
 

    return render(request, 'story_app/genre_page.html',content )


def time_page(request):
    return render(request,'story_app/time_page.html',{'novel_time':Novel.objects.all().order_by('-created_at')})