import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import syllables
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import chardet
nltk.download('punkt')
nltk.download('stopwords')

df = pd.read_excel('Input.xlsx')

def extract_text(link):
  text = ""
  p_texts = []
  # Send a GET request to the website
  try:
    response = requests.get(link)
    # Get the HTML content from the response
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find the first occurrence of the <h1> element with the specified class
    h1_element = soup.find('h1')
    if h1_element is not None:
      # Extract the text content of the element
      h1_text = h1_element.text
      # Print the extracted text
      #print(h1_text)
    else:
      h1_text = ""
    #div_tag = soup.select('div.td-post-content.tagdiv-type','div.tdb-block-inner.td-fix-index')
    div_tag = soup.select('.td-post-content.tagdiv-type,.tdb-block-inner.td-fix-index')
    if div_tag is not None:
      for p in div_tag:
        p_tags = p.find_all('p')
        #print(p_tags)
        if len(p_tags) != 0:
          p_texts = [p.text for p in p_tags]
    for i in p_texts:
      text = text + i + " "
    return h1_text,text
  except requests.exceptions.HTTPError as err:
    if err.response.status_code == 404:
      print("Error 404: Page not found")




# Specify the directory path where you want to create the folder
directory = 'text_files'

"""## **Extract text of the URL's and create text files in the folder**"""

for index, rows in df.iterrows():
  name = rows['URL_ID']
  url = str(rows['URL'])
  #print(name)
  head, text = extract_text(url)
  # # head,text = extract_text(url)
  if head != "" and text != "":
    file_name = f'{name}.txt'
    file_path = os.path.join(directory, file_name)
    #with open(file_path, 'rb') as file:
      #encoding = chardet.detect(file.read())['encoding']
    with open(file_path, 'w',encoding = "utf-8") as f:
      # Write the column values to the text file
      f.write(f'{head}\n')
      f.write(f'{text}\n')

"""## **Checking number of files and null files**"""

def count_files(folder_path):
    file_count = 0
    nul_count = 0
    only_head = 0
    for _, _, files in os.walk(folder_path):
        file_count += len(files)
    for txt in os.listdir(folder_path):
      if txt.endswith('.txt'):
        file_path = os.path.join(folder_path, txt)

        # Detect the encoding of the file
        with open(file_path, 'rb') as file:
            encoding = chardet.detect(file.read())['encoding']

        # Read the stop words from the file and add them to the set
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()
            words = content.split()
            num_words = len(words)
            if num_words < 20:
              only_head+=1
              print(file_path)
            if content == " ":
              nul_count+=1
    return file_count,nul_count,only_head

# Example usage
#directory = ''  # Replace with the text files folder path
num_files,nul,head = count_files(directory)
print("Number of files:", num_files)
print("Number of null files:", nul)
print("Number of files only w heading", head)



"""## **Removing Stopwords**"""


# Specify the directory path where the text files are located
#stop_words_directory = '/content/StopWords/'
# Create an empty set to store all stop words
stop_words = set()
# Loop through the files in the stop words folder
stop_words_folder = 'StopWords'
for filename in os.listdir(stop_words_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(stop_words_folder, filename)

        # Detect the encoding of the file
        with open(file_path, 'rb') as file:
            encoding = chardet.detect(file.read())['encoding']

        # Read the stop words from the file and add them to the set
        with open(file_path, 'r', encoding=encoding) as file:
            stop_words.update(word.strip() for word in file)

# Loop through the text files
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)

        # Detect the encoding of the file
        with open(file_path, 'rb') as file:
            encoding = chardet.detect(file.read())['encoding']

        # Read the file content
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()

        # Tokenize the content into words
        words = word_tokenize(content)

        # Remove stop words
        filtered_words = [word for word in words if word.lower() not in stop_words]

        # Join the filtered words back into a string
        filtered_content = ' '.join(filtered_words)

        # Write the filtered content back to the file
        with open(file_path, 'w', encoding=encoding) as file:
            file.write(filtered_content)

#!unzip /content/MasterDictionary-20230618T144932Z-001.zip

positive_file = r"MasterDictionary\positive-words.txt"
negative_file = r"MasterDictionary\negative-words.txt"
positive_words = set()
negative_words = set()
with open(positive_file, 'rb') as file:
  encoding = chardet.detect(file.read())['encoding']
with open(positive_file, 'r',encoding = encoding) as file:
    positive_words.update(word.strip() for word in file if word.strip() not in stop_words)
with open(negative_file, 'rb') as file:
  encoding = chardet.detect(file.read())['encoding']
with open(negative_file, 'r',encoding = encoding) as file:
    negative_words.update(word.strip() for word in file if word.strip() not in stop_words)

print(positive_words)
print(negative_words)

# Loop through the text files
#directory = '/content/text_files'
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)

        # Detect the encoding of the file
        with open(file_path, 'rb') as file:
            encoding = chardet.detect(file.read())['encoding']

        # Read the file content
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()

        # Tokenize the content into words
        words = word_tokenize(content)

        # Remove stop words
        filtered_words = [word for word in words if word.lower() not in stop_words]

        # Join the filtered words back into a string
        filtered_content = ' '.join(filtered_words)

        # Write the filtered content back to the file
        with open(file_path, 'w', encoding=encoding) as file:
            file.write(filtered_content)

"""## **1. Extracting Derived variables**

"""

def calculate_polarity_subjectivity(pos,neg,total):
  polarity = (pos - neg)/ ((pos + neg) + 0.000001)
  subject =  (pos + neg)/ ((total) + 0.000001)
  return polarity,subject


def score(text):
    """Returns a score btw -1 and 1"""
    text = [e.lower() for e in text if e.isalnum()]
    #total = len(text)
    pos = len([e for e in text if e in positive_words])
    neg = len([e for e in text if e in negative_words])
    return pos, neg

"""## **2. Analysis of Readability & 4. Complex Words**"""

import re
def count_syllables(word):
    word = word.lower()
    if word.endswith(('es', 'ed')):
        word = word[:-2]
    syllables = re.findall(r'[aeiouy]+', word)
    return len(syllables)

def calculate_readability(text):
    # Tokenize the text into words
    words = nltk.word_tokenize(text)

    # Count the number of words and sentences
    num_words = len(words)
    num_sentences = len(nltk.sent_tokenize(text))
    num_syllables = sum(count_syllables(word) for word in words)
    if num_sentences > 0:
        # Calculate the average sentence length
        avg_sentence_length = num_words / num_sentences

        # Count the number of complex words (words with more than 2 syllables)
        complex_words = [word for word in words if len(word) > 2 and syllables.estimate(word) > 2]
        num_complex_words = len(complex_words)

        # Calculate the percentage of complex words
        percentage_complex_words = (num_complex_words / num_words) * 100

        # Calculate the Fog Index
        fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

        return avg_sentence_length, percentage_complex_words, fog_index,num_complex_words
    else:
        # Return default values or handle the case when there are no sentences
        return 0, 0, 0, 0

"""## **3. Average Number of Words Per Sentence**

"""

def calculate_average_words_per_sentence(file_path):
    with open(file_path, 'rb') as file:
        encoding = chardet.detect(file.read())['encoding']
    with open(file_path, 'r',encoding = encoding) as file:
        text = file.read()

    sentences = nltk.sent_tokenize(text)
    num_sentences = len(sentences)

    words = nltk.word_tokenize(text)
    num_words = len(words)
    if num_sentences > 0:
      average_words_per_sentence = num_words / num_sentences
      return average_words_per_sentence
    else:
      return 0

"""## **5. WORD COUNT**"""

import os
import string
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def count_cleaned_words(file_path):
  with open(file_path, 'rb') as file:
    encoding = chardet.detect(file.read())['encoding']

  with open(file_path, 'r', encoding = encoding) as file:
      text = file.read()

  # Remove punctuation
  text = text.translate(str.maketrans('', '', string.punctuation))

  # Tokenize the text into words
  words = text.split()

  # Remove stop words
  cleaned_words = [word for word in words if word.lower() not in stop_words]

  # Count the cleaned words
  num_cleaned_words = len(cleaned_words)

  return num_cleaned_words

# Path to the folder containing the text files
# text_files_folder = '/content/text_files'

# # Loop through all files in the folder
# for filename in os.listdir(text_files_folder):
#     if filename.endswith('.txt'):
#         file_path = os.path.join(text_files_folder, filename)
#         num_cleaned_words = count_cleaned_words(file_path)
#         print(f'File: {filename}')
#         print(f'Total Cleaned Words: {num_cleaned_words}')
#         print('---')

"""## **6. Syllable Count Per Word**

"""

def count_syllables(word):
    word = word.lower()
    if word.endswith(('es', 'ed')):
        word = word[:-2]
    syllables = re.findall(r'[aeiouy]+', word)
    return len(syllables)

def syllable(text):
  words = nltk.word_tokenize(text)
  # Count the number of words and sentences
  #num_words = len(words)
  #num_sentences = len(nltk.sent_tokenize(text))
  num_syllables = sum(count_syllables(word) for word in words)
  return num_syllables

"""## **7. Personal Pronouns**"""

import os
import re

def count_personal_pronouns(file_path):
  with open(file_path, 'rb') as file:
    encoding = chardet.detect(file.read())['encoding']
  with open(file_path, 'r',encoding = encoding) as file:
    text = file.read()

  # Define the personal pronouns regex pattern
  pattern = r'\b(I|we|my|ours|us)\b'

  # Find all matches of personal pronouns in the text
  matches = re.findall(pattern, text, flags=re.IGNORECASE)

  # Count the personal pronouns
  num_personal_pronouns = len(matches)

  return num_personal_pronouns

# # Path to the folder containing the text files
# text_files_folder = '/content/text_files'

# # Loop through all files in the folder
# for filename in os.listdir(text_files_folder):
#     if filename.endswith('.txt'):
#         file_path = os.path.join(text_files_folder, filename)
#         num_personal_pronouns = count_personal_pronouns(file_path)
#         print(f'File: {filename}')
#         print(f'Personal Pronouns Count: {num_personal_pronouns}')
#         print('---')

"""## **8. Average Word length**"""

def calculate_average_word_length(file_path):

    # Detect the encoding of the file
    with open(file_path, 'rb') as file:
        encoding = chardet.detect(file.read())['encoding']
    with open(file_path, 'r',encoding = encoding) as file:
        text = file.read()

    # Split the text into words
    words = text.split()

    # Calculate the total number of characters in each word
    total_characters = sum(len(word) for word in words)

    # Calculate the total number of words
    num_words = len(words)
    if num_words > 0:
      # Calculate the average word length
      average_word_length = total_characters / num_words
      return average_word_length
    else:
      return 0

# Path to the folder containing the text files
# text_files_folder = '/content/text_files'

# # Loop through all files in the folder
# for filename in os.listdir(text_files_folder):
#     if filename.endswith('.txt'):
#         file_path = os.path.join(text_files_folder, filename)
#         average_word_length = calculate_average_word_length(file_path)
#         print(f'File: {filename}')
#         print(f'Average Word Length: {average_word_length:.2f}')
#         print('---')

data = []
for filename in os.listdir(directory):
      if filename.endswith('.txt'):
          file_path = os.path.join(directory, filename)
          with open(file_path, 'rb') as file:
            encoding = chardet.detect(file.read())['encoding']
          with open(file_path, 'r', encoding=encoding) as file:
              text = file.read()
              tokens = word_tokenize(text)
              pos,neg = score(tokens)
              total = len(text)
              # positive_count = sum(1 for token in tokens if token.lower() in positive_words)
              # negative_count = sum(1 for token in tokens if token.lower() in negative_words)
              polarity, subjectivity = calculate_polarity_subjectivity(pos,neg,total)
              avg_sentence_length,percentage_complex_words,fog_index,complex_words = calculate_readability(text)
              avg_word_per_sentence = calculate_average_words_per_sentence(file_path)
              average_word_length = calculate_average_word_length(file_path)
              word_count = count_cleaned_words(file_path)
              num_syllable = syllable(text)
              personal_pronouns = count_personal_pronouns(file_path)
              new_file = filename.replace('.txt', "")
              avg_word_len = calculate_average_word_length(file_path)
              print(f'File: {filename}')
              print(f'Positive Count: {pos}')
              print(f'Negative Count: {neg}')
              print(f'Polarity: {polarity}')
              print(f'Subjectivity: {subjectivity}')
              print(f'Avg Sentence Length: {avg_sentence_length}')
              print(f'Percentage Complex Words: {percentage_complex_words}')
              print(f'Fog Index: {fog_index}')
              print(f'Avg Words Per Sentence: {avg_word_per_sentence}')
              print(f'Average Word Length: {average_word_length:.2f}')
              print(f'Complex Word Count: {complex_words}')
              print(f'Word Count: {word_count}')
              print(f'Syllables per word: {num_syllable}')
              print(f'Personal Pronouns: {word_count}')
              print(f'Average Word Length: {average_word_length:.2f}')
              print('---')

              data.append({
                'URL_ID': new_file,
                #'AVERAGE NUMBER OF WORDS PER SENTENCE': avg_word_per_sentence,
                'POSITIVE SCORE': pos,
                'NEGATIVE SCORE': neg,
                'POLARITY SCORE': polarity,
                'SUBJECTIVITY SCORE':subjectivity,
                'AVG SENTENCE LENGTH': avg_sentence_length,
                'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
                'FOG INDEX': fog_index,
                'AVG NUMBER OF WORDS PER SENTENCE':avg_word_per_sentence,
                #'':average_word_length,
                'COMPLEX WORD COUNT': complex_words,
                'WORD COUNT':word_count,
                'SYLLABLE PER WORD': num_syllable,
                'PERSONAL PRONOUNS': word_count,
                'AVG WORD LENGTH':average_word_length
        })
df_new = pd.DataFrame(data)

df_new = pd.DataFrame(data)

print(df_new)

df_new.info()

excel_file = pd.read_excel('Output Data Structure.xlsx')
print(excel_file.info())

"""## **MERGING THE DATAFRAMES**"""

excel_file = excel_file.drop(['POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE',
       'SUBJECTIVITY SCORE', 'AVG SENTENCE LENGTH',
       'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
       'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
       'SYLLABLE PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'],axis =1)

df_new['URL_ID'] = df_new['URL_ID'].astype('int64')
merged_df = pd.merge(df_new, excel_file, on='URL_ID',how = 'left')
print(merged_df)

merged_df.to_csv('final.csv')

print(merged_df.info())

