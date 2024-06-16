import streamlit as st
from dotenv import load_dotenv
load_dotenv()


import google.generativeai as genai

from  youtube_transcript_api import YouTubeTranscriptApi
import os


genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt="""You are a Good Youtube Video Summarizer .You will summarize the Entire video by Taking the transcript text and summarizing the entire Video and Providing the Import summary in points within 300 words\n
You should Provide the topics seprateley and clear understanding of what is in the script



Your Transcript will be Provided Below 


Transcript:{transcript}
"""



##### GEtting transcript from Youtube Video 
def extract_treanscript(link):

    try:
        video_id=link.split("=")[1]
        trasncript=YouTubeTranscriptApi.get_transcript(video_id=video_id)
       


        trasncript_text=""

        for i in trasncript:
            trasncript_text+=" ".join(i["text"])

      
        return trasncript_text

    except Exception as e:

        raise e
    


###Getting the Sumamry 
def genrate_content(transcript,prompt):

    model=genai.GenerativeModel(model_name="gemini-pro")
 
    prompt.format(transcript=transcript)
   

    response=model.generate_content(prompt)
    return response.text




def main():

    st.set_page_config("YouTube Video Summarizer with Transcript")

    st.title("YouTube Video Summarizer with Transcript \U0001F4F9")

    text_input=st.text_input("Enter the Url od Youtube Video")

    if text_input:
        video_id=text_input.split("=")[1]

        image_url=f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

        st.image(image_url, caption='YouTube Video Thumbnail', use_column_width=True)

    if st.button("get detailed Summary"):

        transcript=extract_treanscript(text_input)

        response=genrate_content(transcript,prompt)

        st.markdown('##Detailed Notes:')


        st.write(response)




if __name__=='__main__':

    main()




