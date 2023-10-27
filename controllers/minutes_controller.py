from app import connect
from flask import make_response
from models.minute_model import Minutes
from bson import ObjectId
from pydantic import ValidationError
from os import environ
from docx import Document
from bson.json_util import dumps
from bson.objectid import ObjectId
import openai
import json

class minutes_controller():

    def transcribe_audio(self, audio_file_path):
        with open(audio_file_path, 'rb') as audio_file:
            transcription = openai.Audio.transcribe("whisper-1", audio_file)
        return transcription['text']

    def abstract_summary_extraction(self, transcription):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        return response['choices'][0]['message']['content']


    def key_points_extraction(self, transcription):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a proficient AI with a specialty in distilling information into key points. Based on the following text, identify and list the main points that were discussed or brought up. These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        return response['choices'][0]['message']['content']


    def action_item_extraction(self, transcription):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI expert in analyzing conversations and extracting action items. Please review the text and identify any tasks, assignments, or actions that were agreed upon or mentioned as needing to be done. These could be tasks assigned to specific individuals, or general actions that the group has decided to take. Please list these action items clearly and concisely."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        return response['choices'][0]['message']['content']
    def sentiment_analysis(self, transcription):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "As an AI with expertise in language and emotion analysis, your task is to analyze the sentiment of the following text. Please consider the overall tone of the discussion, the emotion conveyed by the language used, and the context in which words and phrases are used. Indicate whether the sentiment is generally positive, negative, or neutral, and provide brief explanations for your analysis where possible."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ]
        )
        return response['choices'][0]['message']['content']

    def meeting_minutes(self, transcription):
        abstract_summary = self.abstract_summary_extraction(transcription)
        key_points = self.key_points_extraction(transcription)
        action_items = self.action_item_extraction(transcription)
        sentiment = self.sentiment_analysis(transcription)
        return {
            'abstract_summary': abstract_summary,
            'key_points': key_points,
            'action_items': action_items,
            'sentiment': sentiment
        }

    def save_as_docx(self, minutes, filename):
        doc = Document()
        for key, value in minutes.items():
            # Replace underscores with spaces and capitalize each word for the heading
            heading = ' '.join(word.capitalize() for word in key.split('_'))
            doc.add_heading(heading, level=1)
            doc.add_paragraph(value)
            # Add a line break between sections
            doc.add_paragraph()
        doc.save(filename)

    def getall(self):
        minutes = connect.minutes
        try:
            minutes = minutes.find()
            return make_response({"success":"true","data":json.loads(dumps(list(minutes)))},200)
        except:
            return make_response({"success":"true","message":"server error"},400)
    
    def getminutesbyid(self, id):
        try:
            minutes = connect.minutes.find({"_id":ObjectId(id)})
            return make_response({"success":"true","message":"users retrieved successfully","data":json.loads(dumps(list(minutes)))},200)
        except Exception:
            return make_response({"success":"false","message":"server error"},500)
        
    def generateminutesbyaudio(self,request):
        f = request.files["audio"]
        path="samples/"+f.filename
        f.save(path)
        transcription = self.transcribe_audio(path)
        data = self.meeting_minutes(transcription)
        return make_response({"success":"true","message":"successfully generated minutes","data":data},200)
    
    def generateminutesbytranscript(self,transcription):
        data = self.meeting_minutes(transcription)
        return make_response({"success":"true","message":"successfully generated minutes","data":data},200)
    
    def saveminutes(self,request):
        #get the collections
        minutes = connect.minutes
        users = connect.users

        #check minutes format
        try:
            data = request.json
            Minutes(**data)
        except ValidationError as e:
            return make_response({"success":"false","message":",".join([msg["msg"] for msg in e.errors()])},200)
        #add minutes with the user id
        #add the minute with the user id
        try:
            user = users.find_one({"email":request.user["email"]})
            minute_id = minutes.insert_one(request.json)
            #return the response
            return make_response({"success":"true","message":"successfully saved minutes"},200)
        except:
            return make_response({"success":"false","message":"server error"},500)
    