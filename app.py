import os
import pandas as pd
from flask import Flask, render_template
import json
from matplotlib import pyplot as plt
from publications import Publications

app = Flask(__name__)


@app.route('/')
def getData():
    publications = Publications()

    publications.getData()

    project_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the file path
    file_path = os.path.join(project_dir, 'data.json')

    # Read data from JSON file
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


    print(publications)

    df = pd.DataFrame.from_dict(count_publications_by_date(publications), orient='index', columns=['Count'])

    # Sort DataFrame by index (year)
    df = df.sort_index()

    # Create the histogram using Pandas plot
    ax = df.plot(kind='bar', legend=False, rot=45)
    ax.set_xlabel('Year')
    ax.set_ylabel('Count')
    ax.set_title('Publication Count by Year')

    # Save the plot as an image
    plot_path = 'static/histogram.png'
    plt.tight_layout()
    plt.savefig(plot_path)

    pieGraph = pie_chart(publications)
    # Pass the image path to the HTML template
    return render_template('template.html', histogram_path=plot_path, pie_chart=pieGraph)


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

    labels = list(author_frequencies.keys())
    values = list(author_frequencies.values())

    plt.figure(figsize=(8, 8))  # Şeklin boyutunu belirle (isteğe bağlı)
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.axis('equal')
    plt.title('Authors (excluding B Canbula)')

    chart_path = 'static/pie_chart.png'
    plt.savefig(chart_path)
    plt.close()

    return chart_path


def count_publications_by_date(publications):
    publication_count = {}
    for publication in publications:
        publication_info = publication['publication_info']
        date = publication_info.split(',')[-1].strip()

        if date in publication_count:
            publication_count[date] += 1
        else:
            publication_count[date] = 1
    return publication_count


if __name__ == '__main__':
    app.run()
