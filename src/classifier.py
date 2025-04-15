from werkzeug.datastructures import FileStorage
from transformers import pipeline

from src.preprocessor import do_preprocessing



def classify_file(file: FileStorage, possible_labels):
    preprocessed_data = do_preprocessing(file)

    classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
    result = classifier(preprocessed_data, possible_labels)

    return f"Predicted filetype: {result['labels'][0]}, prediction score: {round(result['scores'][0], 4)}"

