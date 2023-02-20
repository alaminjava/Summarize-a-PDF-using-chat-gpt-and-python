import openai
import PyPDF2
import time

# Set up OpenAI API key
openai.api_key = "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"

# Read the PDF file and create a text file without images
pdf_file = open('example_short.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)
text = ""

for page_num in range(pdf_reader.numPages):
    page = pdf_reader.getPage(page_num)
    text += page.extractText()

# Remove images from the text
text_without_images = ""

for word in text.split():
    if word.startswith("Image") or word.startswith("IMAGE"):
        continue
    text_without_images += word + " "

# Slice words into chunks of text
text_chunks = []
chunk_size = 500

for i in range(0, len(text_without_images), chunk_size):
    text_chunks.append(text_without_images[i:i+chunk_size])


# Summarize the chunks
summary = ""
for chunk in text_chunks:
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=chunk + "\nSummarize the above text in one sentence.",
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5
    )
    summary += response.choices[0].text.strip() + " "


# Merge all the chunks
merged_text = ""
for chunk in text_chunks:
    merged_text += chunk + " "

# Write a new summary of the merged chunks
merged_summary = openai.Completion.create(
    engine="text-davinci-002",
    prompt=merged_text + "\nSummarize the above text in one paragraph.",
    max_tokens=200,
    n=1,
    stop=None,
    temperature=0.5
).choices[0].text.strip()


# Write key notes from the summary
key_notes = openai.Completion.create(
    engine="text-davinci-002",
    prompt=merged_summary + "\nList the key points from the above text.",
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.5
).choices[0].text.strip()

# Write a step-by-step guide from the notes
steps = openai.Completion.create(
    engine="text-davinci-002",
    prompt=key_notes + "\nWrite a step-by-step guide based on the above key points.",
    max_tokens=300,
    n=1,
    stop=None,
    temperature=0.5
).choices[0].text.strip()

# Summarize the notes into the bare essentials of the book
bare_essentials = openai.Completion.create(
    engine="text-davinci-002",
    prompt=key_notes + "\nSummarize the key points into the bare essentials of the book.",
    max_tokens=100,
    n=1,
    stop=None,
    temperature=0.5
).choices[0].text.strip()

# Write a blog post from the notes
blog_post = openai.Completion.create(
    engine="text-davinci-002",
    prompt=key_notes + "\nWrite a blog post based on the above key points.",
    max_tokens=1000,
    n=1,
    stop=None,
    temperature=0.5
).choices[0].text.strip()

# Create mid-journey prompts from the notes for illustrations
mid_journey_prompts = openai.Completion.create(
    engine="davinci",
    prompt=key_notes + "\nCreate mid-journey prompts from the above key points.",
    max_tokens=300,
    n=1,
    stop=None,
    temperature=0.5
).choices[0].text.strip()


print("------------summary-----------")
print(summary)
print("------------merged_summary-----------")
print(merged_summary)
print("------------key_notes-----------")
print(key_notes)
print("------------blog_post-----------")
print(blog_post)
print("------------mid_journey_prompts-----------")
print(mid_journey_prompts)
