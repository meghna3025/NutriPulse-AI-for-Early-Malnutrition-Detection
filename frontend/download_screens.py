import requests

urls = {
    "landing.html": "https://contribution.usercontent.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2RhMmE5ZWYxNGQ0NTQxYTA4MDJlODg4MWUwYTEyMGIxEgsSBxC63ZrB8A4YAZIBIwoKcHJvamVjdF9pZBIVQhM0MjM0MDg3MjEyNTExMTUzNTE5&filename=&opi=89354086",
    "form.html": "https://contribution.usercontent.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2UwM2Q4NTE5MDBkMTQ2MTJhZjgwOTliZWU3OTgxYWQ3EgsSBxC63ZrB8A4YAZIBIwoKcHJvamVjdF9pZBIVQhM0MjM0MDg3MjEyNTExMTUzNTE5&filename=&opi=89354086",
    "dashboard.html": "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2IwYjhmZDIwY2Y4MTQ2YTc4YWI4ZDkzMzJiZDkyMjIwEgsSBxC63ZrB8A4YAZIBIwoKcHJvamVjdF9pZBIVQhM0MjM0MDg3MjEyNTExMTUzNTE5&filename=&opi=89354086"
}

for filename, url in urls.items():
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filename, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
