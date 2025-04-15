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

With the planning done, I finally started on the coding portion. My programming was done in parts, as outlined below. Black text indicates a step, grey text indicates a search query, green text indicates an implemented plan for the step, yellow text indicates an approach that was considered or implemented but later abandoned, red text indicates an approach that could've been taken but was discarded before implementation, and blue text indicates personal reminders / notes. 

![image](https://github.com/user-attachments/assets/12716e9a-e4b2-4c5b-bb35-b5ce4071c560)

The first task was getting a package for reading images. I chose cv2, due to its compatability with a wide variety of image formats including PNG, JPG, TIF, and many more. Images were grayscaled on read-in and then thresholded with an Adaptive Gaussian filter (good for images w/ different light levels) before being fed into an Optical Character Recognition (OCR) algorithm, allowing for text extraction from the images. 

OCR was first attempted with the EasyOCR package, which yielded lackluster results. This approach was considered first due to it being lightweight and requiring no local system installs. Tesseract was the second approach to this and performed quite well. Interestingly, it extracted text more accurately without the adaptive thresholding. 

Once text could be extracted from images, I worked on getting text from PDF's, employing the use of the PyMuPDF library. It was simple and easy to use.

The choice of NLP classifier wasn't as difficult as I thought it would be. I ended up going with a BERT model, as I'd seen its performance before and knew it had a zero-shot model that could be implemented and run locally without local system installs. I was able to provide three labels (bank statement, drivers license, and invoice) and pass in a file, recieving an output with probabilities for each label. To my surprise, this approach worked quite well and was relatively fast. If this failed, I was prepared to use a few-shot learning approach by attaching a Linear layer to a pretrained BERT model and running some of the given examples through it (keeping a few unseen for testing purposes). 

Once this was done, I implemented text extraction from Microsoft Word documents, as well as Microsoft Excel and CSV files. This went rather smoothly; I used docx2txt for DOCX, and the ever reliable pandas package for XLSX and CSV. 

Despite tests with curl running smoothly, I wanted the `pytest` command to properly test the new classifier system, and thus wrote a test function that ran through each file in the files/ folder and verified that the classifier output the correct document type. 

Though it didn't make it into the final submission, I did also investigate data generation as a side goal. Even though the zero-shot classification worked for the given documents (as well as the test documents produced for the new filetypes), I thought it would be worthwhile to attempt data generation for future plans of developing a dedicated, fine-tuned model of our own. This is what I found:
* GPT-2 tended to select 2-3 lines of text from a given input and repeat it 10-30 times as an output.
* Phi-2 tended to output almost identical versions of the input and also randomly injected bits of the prompt into the output.
* HuggingFace models such as llama3 and Mistral required permission to access (on the HuggingFace website), then an authkey (to access via API). I was able to pass these barriers, but ultimately couldn't use either model due to a stated connection error. Many fixes were tried, and none worked.

Unfortunately, I ended up running out of time before rediscovering Ollama, which allowed for models to be downloaded off their website and run locally through a local system install of Ollama. I believe that this would've been a viable solution for data generation, with the added bonus of being extremely easy to work with. Some time might've been needed for proper prompt construction and experimentation with creativity / randomness variables such as temperature and top_k. 

## How to Run

Due to the local system install for Tesseract, I needed a way to package this dependency with my code to prevent clients from needing this install (and any future ones) locally. As such, I chose to use Docker. Though I'd never worked with it before directly, I was familiar with its capability. 

Once this repo is downloaded on a local machine, the app can be run either through Terminal (or adjacent applications) or through Docker Desktop (the below instructions are for Windows version).

### Building

Building can be done by navigating to the directory containing the Dockerfile and running the command: `docker compose up --build`. The build should take about 3-5 minutes, and will automatically start the app when it's done. 

### Testing & Curling (Terminal)

Testing and curling is simple once the container is running. To do either, open a new terminal, navigate to the directory containing the Dockerfile and run the command: `docker compose exec app bash`. This will open a bash prompt where you can test the application by typing `pytest`, or send request using the following command format: `curl -X POST -F 'file=@files/drivers_license_1.jpg' http://127.0.0.1:5000/classify_file`. 

### Testing & Curling (Docker Desktop)

Once the container is running, click on the container in your 'Containers' page, then click on the 'Exec' tab and type the same commands as in the previous section. 

## Improvements / Further Work

* Implement the Ollama LLM model for data generation, do prompt engineering, and experiment with parameters to facilitate generation of a wider variety of data. This would allow for training of our own models, as well as allow for new document types to be introduced and trained for regardless of dataset sizes. Would further allow for more rigorous testing of the current zero-shot classifier implementation. 
* Test the effectiveness of the zero-shot model against a fully trained model (using generated data).
* Reduce bulk of preprocessor.py. Much of the code in preprocessor.py simply performs text extraction given a certain file extension. This code could be condensed by creating a dictionary that maps each file extension to a callable text extraction method and then calls a one liner that does the extraction. This would make adding new text extraction methods for new file types easier (write method, add to dictionary) and would reduce the clutter of the current if -> elif -> else implementation.
* Create a frontend for the app. Currently the app defaults to a 404 (as there is no homepage). It would be convenient if you could drag and drop or upload files to a website (even if its localhost) and get the results displayed neatly.
* Set up CI/CD pipeline via GitHub, or through other methods to facilitate easier building, testing, and deployment.



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
