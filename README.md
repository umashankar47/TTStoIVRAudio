Text-to-Speech Converter for IVR Audio Testing
This Python program, built with Tkinter, provides a simple GUI for converting text into speech using Google Text-to-Speech (gTTS). It then converts the generated speech into an audio format that is compatible with Interactive Voice Response (IVR) systems, making it easier to test and verify audio files used in IVR applications.

Features
Text to Speech Conversion: Enter any text, and the program converts it into speech using Google Text-to-Speech (gTTS).
IVR Compatible Audio: The generated speech is automatically saved in an audio format supported by IVR systems.
Batch Processing via CSV: Load a CSV file containing prompt names and content. The program will create a folder and save each generated audio file with the corresponding prompt name.
User-Friendly Interface: Built with Tkinter, the program offers a simple and intuitive GUI for easy interaction.
Quick Audio Testing: Ideal for testing and verifying audio files during IVR development and deployment.

Requirements
Python 3.x
Tkinter (usually included with Python installations)
gTTS (Google Text-to-Speech)
csv (for CSV file handling)


Usage
Convert Text to Speech
Enter the text you wish to convert into speech in the provided text box.
Click the "Convert" button to generate the audio file.
The program will save the audio file in the specified directory, ready for use in IVR systems.
Batch Processing with CSV
Prepare a CSV file with two columns: prompt_name and content.
Load the CSV file into the program.
The program will create a folder named after the CSV file and save all the generated audio files with the corresponding prompt names.

![image](https://github.com/umashankar47/TTStoIVRAudio/assets/159722680/693af828-51ea-43aa-a1f4-9acec35e97dd)


Eg. - 

![image](https://github.com/umashankar47/TTStoIVRAudio/assets/159722680/1fceb1e7-a549-41eb-92ec-d3e27542fd14)




 

