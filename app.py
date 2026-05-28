from flask import Flask, render_template, request
import os

app = Flask(__name__)


def search_files(folder_path, keyword):
    results = []

    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            path = os.path.join(folder_path, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                    count = content.count(keyword.lower())
                    if count > 0:
                        results.append((file, count))
            except OSError:
                continue

    results.sort(key=lambda x: x[1], reverse=True)
    return results


@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    error = None
    folder = ''
    keyword = ''

    if request.method == 'POST':
        folder = request.form.get('folder', '').strip()
        keyword = request.form.get('keyword', '').strip()

        if not folder or not keyword:
            error = 'Please enter both a folder path and a keyword.'
        elif not os.path.isdir(folder):
            error = f'The folder does not exist: {folder}'
        else:
            results = search_files(folder, keyword)
            if not results:
                error = 'No matches found.'

    return render_template('index.html', results=results, error=error, folder=folder, keyword=keyword)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
