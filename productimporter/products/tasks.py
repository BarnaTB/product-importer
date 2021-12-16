from productimporter import celery_app as app


@app.task
def load_data(file):
    pass
