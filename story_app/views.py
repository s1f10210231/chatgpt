from django.shortcuts import render, redirect
import openai
import requests
from .models import Novel,NovelImage
from collections import defaultdict
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.base import ContentFile
from .forms import NovelEditForm


openai.api_key = '4b98eCipWEd7272fuiZlnZtjLaatiCWm2di3cdVoXxHskiyxuYdCr7-WS94fu0gbbmg5QheHOQVinJiZnwGCTgw'
openai.api_base = 'https://api.openai.iniad.org/api/v1'

# Create your views here.

def generate_novel(genre,where,when,who,how,key):
    if genre == "ホラー":
        message=[{"role": "system", "content": f"あなたは1500文字の{genre}専門とする天才的な日本のショートショート作家です。制約条件を絶対に守り命令文に従ってください"},
                    {"role": "user", "content": f'''
                    #制約条件
                    ・ターゲット読者: 10代以上
                    ・読者を怖がらせてください。
                    ・名前はあなたが決めてください。
                    ・現実にありそうな内容。
                    ・小説は日本語
                    ・時間設定は {when} 。
                    ・シーンは1つだけにすること
                    ・タイトルを表示しない。
                    ・起承転結
                    ・展開を大袈裟にする。
                    ・ジャンルは{genre}。
                    ・場面設定は{where}。
                    ・{how}のような展開にすること。
                    ・次回予告はしないでください
                    ・必ずバッドエンドにしてください。
                    ・読者を鬱にさせてください。
                    ・キーワード：[{key}]
                    #命令文
                    以上の制約条件を絶対に守り、ショートショート小説を書いてください。
                    #出力
                    --本文--
                    '''},

                    ]
    elif genre == "ファンタジー":
        message=[{"role": "system", "content": f"あなたは1500文字の{genre}専門とする天才的な日本のショートショート作家です。制約条件を絶対に守り命令文に従ってください"},
                    {"role": "user", "content": f'''
                    #制約条件
                    ・ターゲット読者: 10代以上
                    ・内容：非現実的
                    ・世界観：{who}
                    ・名前はあなたが決めてください。
                    ・言語：日本語
                    ・時間設定：{when} 。
                    ・タイトルを表示しない。
                    ・展開を大袈裟にする。
                    ・ジャンル：{genre}。
                    ・シーンは1つだけにすること
                    ・シーン：{where}
                    ・展開：{how}。
                    ・次回予告はしないでください
                    ・キーワード：[{key}]
                    #命令文
                    以上の制約条件を絶対に守り、ショートショート小説を書いてください。
                    #出力文
                    --本文--
                    '''},
                    ]
    elif genre == "ラブコメ":
        message=[{"role": "system", "content": f"あなたは1500文字の{genre}専門とする天才的な日本のショートショート作家です。制約条件を絶対に守り命令文に従ってください"},
                    {"role": "user", "content": f'''
                    #制約条件
                    ・ターゲット読者: 10代以上
                    ・ヒーローとヒロインそれぞれ作成してください。 
                    ・ヒーローとヒロインの会話を物語形式で楽しませてください。
                    ・ヒーローとヒロインの口調は今風にしてください
                    ・シーンは1つだけにすること
                    ・主人公の設定は{who}とすること。
                    ・名前はあなたが決めてください。
                    ・言語は日本語
                    ・時間設定は {when} 。
                    ・タイトルを表示しない。
                    ・起承転結
                    ・展開を大袈裟にする。
                    ・ジャンルは{genre}。
                    ・場面設定は{where}。
                    ・{how}のような内容にすること。
                    ・必ずオチをつける。
                    ・キュンとする
                    ・前向きになるような内容
                    ・非現実的な内容
                    ・キーワード：[{key}]

                    #命令文
                    以上の制約条件を絶対に守り、ショートショート小説を書いてください。
                    #出力
                    --本文--
                    '''},
                    ]
    elif genre == "ミステリー":
        message=[{"role": "system", "content": f"あなたは1500文字の{genre}専門とする天才的な日本のショートショート作家です。制約条件を絶対に守り命令文に従ってください"},
                    {"role": "user", "content": f'''
                    #制約条件
                    ・主人公の設定：探偵
                    ・登場人物は六人以上
                    ・進行役：{who}
                    ・犯人候補の手順：三人から推理して一人に絞る。
                    ・犯人を追い詰める。
                    ・読者も一緒に推理できる内容。
                    ・名前はあなたが決めてください。
                    ・ターゲット読者: 10代以上
                    ・言語：日本語
                    ・時間設定は {when} 。
                    ・タイトルを表示しない。
                    ・起承転結
                    ・展開を大袈裟にする。
                    ・ジャンルは{genre}。
                    ・場面設定は{where}。
                    ・展開：{how}
                    ・誰が真犯人かは最後に書いてください。
                    ・犯罪の動機を書いてください。
                    ・推理パートでどうやって犯罪したかを明記してください。
                    ・次回予告はしないでください
                    ・キーワード：[{key}]
                    #命令文
                    以上の制約条件を絶対に守り、ショートショート小説を書いてください。
                    #出力
                    --本文--
                    '''},
                    ]
    elif genre == "SF":
        message=[{"role": "system", "content": f"あなたは1500文字の{genre}専門とする天才的な日本のショートショート作家です。制約条件を絶対に守り命令文に従ってください"},
                    {"role": "user", "content": f'''
                    #制約条件
                    ・ターゲット読者: 10代後半以上
                    ・内容：科学的根拠に基づいた空想
                    ・世界観：{who}
                    ・名前はあなたが決めてください。
                    ・言語：日本語
                    ・時間設定：{when} 。
                    ・タイトルを表示しない。
                    ・展開を大袈裟にする。
                    ・ジャンル：{genre}。
                    ・シーンは1つだけにすること
                    ・シーン：{where}
                    ・展開：{how}。
                    ・次回予告はしないでください
                    ・キーワード：[{key}]
                    #命令文
                    以上の制約条件を絶対に守り、ショートショート小説を書いてください。
                    #出力
                    --本文--
                    '''},
                    ]
    else:
        message=[{"role": "system", "content": f"あなたは1500文字の{genre}専門とする天才的な日本のショートショート作家です。制約条件を絶対に守り命令文に従ってください"},
                    {"role": "user", "content": f'''
                    #制約条件
                    ・ターゲット読者: 10代以上
                    ・主人公の設定は{who}とすること。
                    ・名前はあなたが決めてください。
                    ・小説は日本語
                    ・時間設定は {when} 。
                    ・タイトルを表示しない。
                    ・起承転結
                    ・展開を大袈裟にする。
                    ・ジャンルは{genre}。
                    ・場面設定は{where}。
                    ・{how}のような展開にすること。
                    ・お話は一つだけだが、次回を期待させる。
                    ・次回予告はしないでください
                    ・キーワード：[{key}]

                    #命令文
                    以上の制約条件を絶対に守り、ショートショート小説を書いてください。
                    #出力
                    --本文--
                    '''},
                    ]

    response = openai.ChatCompletion.create(model = 'gpt-3.5-turbo', messages=message, max_tokens=3000)
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
                key = request.POST.get('keyword', '')

        elif form_type == 'autoInput':
                # 組み合わせ選択フォームからのデータを取得
                genre = request.POST.get('genre','')  # リストとして取得されるので getlist を使用
                who = request.POST.get('whose', '')
                where = request.POST.get('where', '')
                when = request.POST.get('when', '')
                how = request.POST.get('how', '')
                key = request.POST.get('key', '')
        else:
                # ユーザー手動入力フォーム以外の場合、適切な初期値を設定
                genre = ''
                who = ''
                where = ''
                when = ''
                how = ''
                key = ''
        genre_text = "\n".join(genre)
        who_text = "\n".join(who)
        where_text = "\n".join(where)
        when_text = "\n".join(when)
        how_text = "\n".join(how)
        key_text = "\n".join(key)

        generated_novel = generate_novel(genre_text,where_text,when_text,who_text,how_text,key_text)
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
    context = {
        "novel": Novel.objects.get(pk=novel_id),
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
        if request.user in novel.liked_by.all():
            novel.like -= 1
            novel.save()
            request.user.liked_novels.remove(novel)
        else:
            novel.like += 1
            novel.save()
            request.user.liked_novels.add(novel)
    except Novel.DoesNotExist:
        raise Http404("Novel does not exist")
    context = {
        "novel": novel,
    }
    return render(request, "story_app/detail.html", context)


def genre_page(request, genre):
    # ジャンルに基づいて小説をフィルタリング
    novels = Novel.objects.filter(genre=genre)
    content={'novels': novels, 'genre': genre}
    return render(request, 'story_app/genre_page.html',content )


def time_page(request):
    return render(request,'story_app/time_page.html',{'novel_time':Novel.objects.all().order_by('-created_at')})


def rank(request):
    novels = Novel.objects.all().order_by('-like')  # お気に入りの数が多い順にソート
    return render(request, 'story_app/rank.html', {'novels': novels})