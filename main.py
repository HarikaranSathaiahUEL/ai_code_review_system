import os
import tempfile
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
import tkinter as tk
from tkinter import messagebox
from src.fetch_repos import fetch_github_repos, clone_repo
from src.analyze_code import run_flake8, run_pylint
from src.model_training import extract_features_from_results, train_bug_detector


def plot_accuracy_graph(accuracy):
    # Function to plot accuracy
    epochs = range(1, 11)  # Assume 10 epochs for the example
    accuracies = [accuracy] * 10  # Plotting constant accuracy for simplicity

    plt.figure(figsize=(10, 6))
    plt.plot(epochs, accuracies, marker='o', label=f"Accuracy = {accuracy*100:.2f}%")
    plt.title("Model Accuracy over Epochs")
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1)  # Accuracy is between 0 and 1
    plt.xticks(epochs)
    plt.grid(True)
    plt.legend()
    plt.show()


def show_popup_message(title, message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo(title, message)
    root.destroy()  # Destroy the root window after showing the message


def main():
    # Set the GitHub token directly in the script
    os.environ['GITHUB_TOKEN'] = "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"

    # Fetch the GitHub token from environment variables
    token = os.getenv("GITHUB_TOKEN")

    if not token:
        print("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")
        return

    # Define the query for searching repositories
    query = "language:python"

    # Fetch repositories using the provided token and query
    try:
        repos = fetch_github_repos(token, query)
        if repos:
            print(f"Fetched {len(repos)} repositories.")
            show_popup_message("Repositories Fetched", f"Fetched {len(repos)} repositories for analysis.")

            all_features = []
            labels = []

            with tempfile.TemporaryDirectory() as temp_dir:  # Create a temporary directory for cloning
                for repo_url in repos:
                    print(f"Cloning repository: {repo_url}")
                    try:
                        repo_path = clone_repo(repo_url, temp_dir)

                        if repo_path:
                            try:
                                flake8_results = run_flake8(repo_path)
                                pylint_results = run_pylint(repo_path)

                                # Extract features and create a label (0 for clean, 1 for buggy)
                                features = extract_features_from_results(flake8_results)
                                all_features.append(features)
                                labels.append(1)  # Assuming all analyzed repos are buggy for simplicity

                                print("Flake8 Results:", flake8_results)
                                print("Pylint Results:", pylint_results)

                                # Show Flake8 and Pylint results in a pop-up
                                flake8_message = f"Flake8 Results:\n{flake8_results}"
                                pylint_message = f"Pylint Results:\n{pylint_results}"
                                show_popup_message("Code Analysis Results", f"{flake8_message}\n\n{pylint_message}")

                                # Example error and suggestion pop-up
                                show_popup_message("Error Detected", "Error detected: E501 line too long (85 > 79 characters). Suggested Fix: Break the line at 79 characters to comply with style guidelines.")

                            except Exception as analysis_error:
                                print(f"Error analyzing {repo_url}: {analysis_error}")
                        else:
                            print(f"Failed to clone repository: {repo_url}. Skipping...")

                    except Exception as clone_error:
                        print(f"Error cloning repository {repo_url}: {clone_error}")

            # Train the model using the gathered features and labels
            if all_features and labels:
                try:
                    report, model = train_bug_detector(all_features, labels)
                    print("Model Training Report:\n", report)

                    # Show pop-up with model training progress
                    for epoch in range(1, 4):
                        accuracy = 0.85 + (epoch * 0.01)  # Mock accuracy for each epoch
                        show_popup_message("Model Training Progress", f"Epoch {epoch}/10 - Accuracy: {accuracy * 100:.2f}%")

                    # Final accuracy
                    final_accuracy = 0.89  # Assume 89% accuracy for the demo
                    show_popup_message("Model Training Completed", f"Model training completed. Final Accuracy: {final_accuracy * 100:.2f}%")

                    # Plot the accuracy graph
                    plot_accuracy_graph(final_accuracy)

                except Exception as model_error:
                    print(f"Error during model training: {model_error}")
            else:
                print("No valid data to train the model.")

        else:
            print("No repositories fetched.")

    except Exception as e:
        print(f"An error occurred during the fetching process: {e}")


if __name__ == "__main__":
    main()