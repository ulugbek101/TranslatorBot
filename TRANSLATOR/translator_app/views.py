from django.shortcuts import render
from googletrans import Translator


def index(request):
    if request.method == 'POST':
        translator = Translator()
        word = request.POST.get('word')
        from_lang = translator.detect(text=word.lower()).__getattribute__("lang")
        to_lang = request.POST.get("to_lang")
        translated_word = translator.translate(src=from_lang, dest=to_lang, text=word).text
        context = {
            "word": translated_word
        }
        print(translated_word)
        return render(request, "translator_app/index.html", context)
    return render(request, "translator_app/index.html")
