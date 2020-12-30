from transformers import GPT2Tokenizer, GPT2LMHeadModel, pipeline
import re
import json
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

translator = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-ru")
translator_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-ru")

model = GPT2LMHeadModel.from_pretrained('gpt2-tuned_with_wishes')
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model.to('cuda')
translator.to('cuda')

replay_point = True

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


start = r'Happy New Year!'
congratulations = {}

for i in tqdm(range(500)):
    text = pipeline('text-generation', model=model, tokenizer=tokenizer, device=0)(r'Happy New Year!',
                                                                                   max_length=150)[0]
    congratulation = ' '.join(split_into_sentences(text['generated_text'])[1:-1])
    translation = pipeline('translation_en_to_ru', model=translator, tokenizer=translator_tokenizer, device=0)(congratulation)
    congratulations[i] = translation

with open('congratulations/congratulations_4.txt', 'w', encoding='utf8') as outfile:
    json.dump(congratulations, outfile, ensure_ascii=False)