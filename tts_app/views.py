from django.shortcuts import render
from django.http import JsonResponse
import boto3
from django.conf import settings
import os

def text_to_speech(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        polly = boto3.client('polly', 
                             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                             region_name=settings.AWS_REGION)
        response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')
        audio_stream = response['AudioStream'].read()
        
        # Save audio_stream to a file in the static directory
        audio_file_path = os.path.join('tts_app/static/tts_app', 'output.mp3')
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(audio_stream)
        
        # Render the template with the audio file path
        return render(request, 'tts_app/text_to_speech.html', {'audio_file': '/static/tts_app/output.mp3'})
    
    # Render the text-to-speech template for GET requests
    return render(request, 'tts_app/text_to_speech.html')
