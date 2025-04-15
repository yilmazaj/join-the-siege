# Heron Coding Challenge - Report

## Planning Phase

Before coding, I planned out my idea for what the final version of this project would look like. I analyzed the existing codebase first then addressed the questions from Part 1 and 2 as seen below in the Overview sections. 

My analysis of the initial codebase yielded the following notes: 

![image](https://github.com/user-attachments/assets/95bda93e-333f-4c36-bada-c4f2c7f036f0)

Though simple, I thought it important to understand what I was working with before beginning, as I'd actually not used Flask before this task. 

Following this, I addressed Part 1:

![image](https://github.com/user-attachments/assets/2d799e19-7dee-4825-82ac-e6f9c3cbecd3)

This outlined two main issues with the current system:
* New document types necessitate new `if doc_type in filename:` statements
* Classifier depends on consistent naming conventions w/ Document type in filename w/ specific spelling

The way in which these issued could be addressed was largely by modifying the classifier. For this, I had two ideas given the *extension* types. The first was an NLP based classifier, which would necessitate that all files be converted to text format, suited for the PDF files. The second was an Image Rec based classifier, which would necessitate that all files be converted to img format, suited for thg PNG files. The processes by which both would be utilized are detailed in the snippet above.

Overall, I ended up going with the NLP based classifier for a few reasons:
* Documents may not have similar formats, which could lead to difficulties when doing Image Rec (no concrete patterns to pick up on)
* Documents of different types may have similar formats, which could lead to misclassification
* Building our own model would require synthetic data generation in image format, which I thought would be more difficult precision-wise and more expensive than text generation
* Zero-shot was likely not possible due to the specificity of the data and labels we were trying to classify (how many models have been trained to recognize the difference between bank statements and invoices?)
* Few-shot has the same issues as building our own model (data generation infidelity)

With these questions explored, I moved on to Part 2:

![image](https://github.com/user-attachments/assets/83999f82-767b-43ad-858a-680a454d068c)

When I first set out to tackle this problem, I'd not yet considered zero-shot classifiers, and thus had plans on how to build a robust classifier of my own using synthetic data. I planned to use an LLM to generate said data. Prediction thresholding was another idea I had, though this was forgone as it wasn't an issue for any of the examples I used in testing. In a true production environment however, this might be a decent idea. Lastly, for ease of deployment, saving the model parameters and packaging them with the project file was an idea I had to avoid the need to retrain models client-side. 

This was the general architecture at the end of the planning phase: 

![image](https://github.com/user-attachments/assets/2a177aa0-a3de-4d6a-b3d0-ee52239326b9)

## Work Phase



# Heron Coding Challenge - File Classifier

## Overview

At Heron, we’re using AI to automate document processing workflows in financial services and beyond. Each day, we handle over 100,000 documents that need to be quickly identified and categorised before we can kick off the automations.

This repository provides a basic endpoint for classifying files by their filenames. However, the current classifier has limitations when it comes to handling poorly named files, processing larger volumes, and adapting to new industries effectively.

**Your task**: improve this classifier by adding features and optimisations to handle (1) poorly named files, (2) scaling to new industries, and (3) processing larger volumes of documents.

This is a real-world challenge that allows you to demonstrate your approach to building innovative and scalable AI solutions. We’re excited to see what you come up with! Feel free to take it in any direction you like, but we suggest:


### Part 1: Enhancing the Classifier

- What are the limitations in the current classifier that's stopping it from scaling?
- How might you extend the classifier with additional technologies, capabilities, or features?


### Part 2: Productionising the Classifier 

- How can you ensure the classifier is robust and reliable in a production environment?
- How can you deploy the classifier to make it accessible to other services and users?

We encourage you to be creative! Feel free to use any libraries, tools, services, models or frameworks of your choice

### Possible Ideas / Suggestions
- Train a classifier to categorize files based on the text content of a file
- Generate synthetic data to train the classifier on documents from different industries
- Detect file type and handle other file formats (e.g., Word, Excel)
- Set up a CI/CD pipeline for automatic testing and deployment
- Refactor the codebase to make it more maintainable and scalable

## Marking Criteria
- **Functionality**: Does the classifier work as expected?
- **Scalability**: Can the classifier scale to new industries and higher volumes?
- **Maintainability**: Is the codebase well-structured and easy to maintain?
- **Creativity**: Are there any innovative or creative solutions to the problem?
- **Testing**: Are there tests to validate the service's functionality?
- **Deployment**: Is the classifier ready for deployment in a production environment?


## Getting Started
1. Clone the repository:
    ```shell
    git clone <repository_url>
    cd heron_classifier
    ```

2. Install dependencies:
    ```shell
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. Run the Flask app:
    ```shell
    python -m src.app
    ```

4. Test the classifier using a tool like curl:
    ```shell
    curl -X POST -F 'file=@path_to_pdf.pdf' http://127.0.0.1:5000/classify_file
    ```

5. Run tests:
   ```shell
    pytest
    ```

## Submission

Please aim to spend 3 hours on this challenge.

Once completed, submit your solution by sharing a link to your forked repository. Please also provide a brief write-up of your ideas, approach, and any instructions needed to run your solution. 
