from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def extract_features_from_results(flake8_results):
    features = {
        'line_too_long': flake8_results.count('E501'),
        'blank_line_whitespace': flake8_results.count('W293'),
        'syntax_error': flake8_results.count('F0001'),
        'parse_error': flake8_results.count('F0010'),
        # Add more features based on other error/warning types
    }
    return list(features.values())

def train_bug_detector(features, labels):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    return classification_report(y_test, predictions), model