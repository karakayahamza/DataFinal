import os
import pandas as pd
from flask import Flask, render_template
import json
from publications import Publications
from wordcloud import WordCloud

app = Flask(__name__)


@app.route('/')
def getData():
    publications = Publications()

    publications.getData()

    project_dir = os.path.dirname(os.path.abspath(__file__))

    file_path = os.path.join(project_dir, 'data.json')

    with open(file_path, 'r') as file:
        data = json.load(file)

        publications = []
        for item in data:
            publication = {
                'authors': item['authors'],
                'publication_info': item['publication_info'],
                'title': item['title'],
                'url': item['url']
            }
            publications.append(publication)

    #Histogram
    df = pd.DataFrame.from_dict(count_publications_by_date(publications), orient='index', columns=['Count'])
    df = df.sort_index()
    years = df.index.tolist()
    years_as_integers = [int(year) for year in years]
    counts = df['Count'].tolist()

    #PieGraph
    pieGraph = pie_chart(publications)
    pieLabels = pieGraph.keys()
    pieVal = pieGraph.values()
    pieValues = [int(year) for year in pieVal]
    liste = list(pieLabels)


    #CLOUD Image
    cloudData = cloud(publications)
    return render_template('template.html', pieLabels=liste, pieValues=pieValues, cloudData=cloudData,
                           years=years_as_integers, counts=counts)


def pie_chart(data):
    authors_except_b = []
    for item in data:
        authors = item['authors'].split(', ')
        for author in authors:
            if author != 'B Canbula':
                authors_except_b.append(author)

    author_frequencies = {}
    for author in authors_except_b:
        if author in author_frequencies:
            author_frequencies[author] += 1
        else:
            author_frequencies[author] = 1

    return author_frequencies


def cloud(publications):
    titles = [pub['title'] for pub in publications]

    preprocessed_titles = []
    for title in titles:
        processed_title = ''.join(ch.lower() for ch in title if ch.isalnum() or ch.isspace())
        words = processed_title.split()
        preprocessed_titles.extend(words)

    word_frequencies = {}
    for word in preprocessed_titles:
        word_frequencies[word] = word_frequencies.get(word, 0) + 1

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_frequencies)

    wordcloud_image = "static/wordcloud.png"
    wordcloud.to_file(wordcloud_image)

    return wordcloud_image


def count_publications_by_date(publications):
    publication_count = {}
    for publication in publications:
        publication_info = publication['publication_info']
        date = publication_info.split(',')[-1].strip().rstrip('.')

        if date in publication_count:
            publication_count[date] += 1
        else:
            publication_count[date] = 1
    return publication_count


if __name__ == '__main__':
    app.run()
