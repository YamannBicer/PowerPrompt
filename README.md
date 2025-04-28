# PowerPrompt

PowerPrompt utilizes AI's electrical consumption to balance electricity demand and supply.

PowerPrompt's web platform displays the AI generated images and videos. 
Those images and videos are generated with pregenerated prompts when electricty demand is low and electiricty prices are negative.
The platform also allows users to upload their own prompts and generate images and videos.


run in terminal: 
uvicorn backend.main:app --reload

then:
streamlit run frontend/app.py

