import csv
import threading
import tkinter
from tkinter import *
from tkinter import filedialog, messagebox, ttk

import gtts
import librosa
from gtts import gTTS
import numpy as np
import soundfile as sf
from pydub import AudioSegment


class TtsToIvr:
    def __init__(self, master):
        self.csv_window = None
        self.csv_flag = None
        self.master = master
        self.master.title("TTS to IVR APP")
        self.master.iconbitmap('E:/PythonProject/IVR_TTS/pythonProject/pyAPP/chat.ico')
        self.master.geometry("800x300")

        self.TTS_ENGINE = [
            ("google - TTS", "Google")
        ]
        self.LANGUAGES = {

            'en':'English'
        }

        self.ACCENTS = {

            'United States':'us'

        }
        try:
            self.LANGUAGES = gtts.lang.tts_langs()
        except Exception as e:
            print('Exception getting Languages ', e)

        try:
            self.ACCENTS = gtts.lang.tts_langs()
        except Exception as e:
            print('Exception getting Accents ', e)

        self.tts_engine = StringVar()
        self.tts_lang = StringVar()

        self.to_mono = BooleanVar()
        # samp = BooleanVar()
        self.compression = StringVar()
        self.bit_rate = IntVar()
        var1 = BooleanVar()
        var2 = BooleanVar()

        self.csv_path_file = ''
        self.prompts_list = {}
        self.dest_path = ''
        self.progress_var = DoubleVar()

        self.tts_field_label = Label(self.master, text="Enter Prompt Content ").grid(row=1, column=0, padx=10, pady=10)
        self.tts_field = Entry(self.master, width=80)
        self.tts_field.grid(row=1, column=1, padx=10, pady=10)

        self.cancel_op = BooleanVar()
        self.cancel_op.set(False)

        self.dropdowns()
        self.createButtons()
        self.labels()

    def createButtons(self):

        load_csv_button = Button(self.master, text="Load a CSV FIle", command=lambda: self.open_csv())
        load_csv_button.grid(row=7, column=1)

        load_destination_button = Button(self.master, text="O/P Folder", padx=10, pady=5,
                                         command=lambda: self.set_destination())
        load_destination_button.grid(row=5, column=1)

        generate_button = Button(self.master, text="Generate", padx=10, pady=5,
                                 command=lambda: threading.Thread(
                                     target=self.text_to_speech(
                                         language=self.tts_lang.get())).start()
                                 )
        generate_button.grid(row=2, column=1)

    def labels(self):
        # Text on column 1
        frame1 = LabelFrame(self.master, padx=5, pady=5)
        frame1.grid(row=0, column=1, padx=10, pady=10)
        # Label
        myLabel1 = Label(frame1, text="|||||||||||||||||<< TTS To IVR Audio >>|||||||||||||||||")
        myLabel1.pack()

        sel_engine_text = Label(self.master, text="Choose TTS Engine :")
        sel_engine_text.grid(row=3, column=0)

        sel_language_text = Label(self.master, text="Choose Language :")
        sel_language_text.grid(row=4, column=0)

        load_csv_text = Label(self.master, text="Load a List with CSV :")
        load_csv_text.grid(row=7, column=0)

        curr_dest_text = Label(self.master, text="Output Folder:")
        curr_dest_text.grid(row=5, column=0)

    def dropdowns(self):

        self.tts_engine.set(self.TTS_ENGINE[0][1])
        temp_tts_engines = []

        self.tts_lang.set(self.LANGUAGES['en'])
        temp_tts_langs = {

        }

        for text, engine in self.TTS_ENGINE:
            print("text - ", text, "engine-", engine)
            temp_tts_engines.append(engine)

        # for key in self.LANGUAGES:
        #     print("text - ", key, "language-", self.LANGUAGES[key])
        #     temp_tts_langs[key] = self.LANGUAGES[key]

        tts_engine_dropdown = OptionMenu(self.master, self.tts_engine, *temp_tts_engines).grid(row=3, column=1)

        tts_language_dropdown = OptionMenu(self.master, self.tts_lang, *self.LANGUAGES.values()).grid(row=4, column=1)

    def open_csv(self):
        print("Open CSV")
        self.csv_flag = 'y'
        self.master.filename = filedialog.askopenfilename(initialdir="", title="openCSVFile",
                                                          filetypes=(("csv fies", "*.csv"),))
        self.csv_path_file = self.master.filename
        print("csv path: ", self.csv_path_file)
        if self.csv_path_file != '':
            # self.read_csv(self.csv_path_file)
            threading.Thread(target=self.csv_read_window()).start()
        else:
            print('csv path empty')
            messagebox.showinfo("csv path empty", "csv path empty")

    def read_csv(self, csv_path_file):
        print("Read CSV")

        with open(csv_path_file, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)
            # Iterate through each row in the CSV file
            for row in csv_reader:
                key = row[0].rstrip()
                value = row[1].rstrip()
                self.prompts_list[key] = value

        temp = len(self.prompts_list)

        frame4 = LabelFrame(self.csv_window, padx=5, pady=5)
        frame4.grid(row=4, column=3, padx=10, pady=10)

        file_label = Label(frame4, text="Current File :")
        file_label.grid(row=0, column=1)

        curr_file_label = Label(frame4, text="")
        curr_file_label.grid(row=0, column=2)

        for key, value in self.prompts_list.items():
            print('self.cancel_op', self.cancel_op.get())
            if self.cancel_op.get():
                print("Canceling Operation.")
                break
            else:
                print(f"Key: {key}, Value: {value}")
                file_name = key
                input_text = value
                threading.Thread(
                    target=self.text_to_speech(input_text, file_name, language=self.tts_lang.get())).start()
                curr_file_label.config(text=f"{key}")
                threading.Thread(target=self.update_progress(100 / temp)).start()

        print('self.cancel_op', self.cancel_op.get())
        if self.cancel_op is True:
            messagebox.showinfo("operation Canceled", "Converted Files saved in destination DIR")
        else:
            messagebox.showinfo("operation complete", "Files saved in destination DIR")
            self.prompts_list.clear()
            threading.Thread(target=self.update_progress(-1 * self.progress_var.get())).start()

    def set_destination(self):
        print("getting Destination Folder")
        # shutil.move("audio.mp3", "path/to_your/file_name.mp3")
        self.master.filename = filedialog.askdirectory(initialdir="", title="setDestination Folder")
        self.dest_path = self.master.filename
        print("Destination - ", self.dest_path)

    def csv_read_window(self):
        self.csv_window = tkinter.Toplevel(self.master)
        self.csv_window.title("processing")
        self.csv_window.iconbitmap('E:/PythonProject/IVR_TTS/pythonProject/pyAPP/chat.ico')
        self.csv_window.geometry("500x250")
        self.csv_window.wm_attributes("-topmost", 1)

        # Label

        mylabel2 = Label(self.csv_window, text="                            ", padx=10, pady=10)
        mylabel2.grid(row=0, column=2)

        frame2 = LabelFrame(self.csv_window, padx=5, pady=5)
        frame2.grid(row=1, column=3)

        csv_read_text = Label(frame2, text="Progress :")
        csv_read_text.grid(row=0, column=1)

        progress_bar = ttk.Progressbar(frame2, variable=self.progress_var, maximum=100, orient='horizontal',
                                       mode='determinate', length=280)
        progress_bar.grid(row=0, column=2)

        mylabel3 = Label(self.csv_window, text="                            ", padx=10, pady=10)
        mylabel3.grid(row=2, column=2)

        frame3 = LabelFrame(self.csv_window, padx=5, pady=5)
        frame3.grid(row=3, column=3)

        start_button = Button(frame3, text="Start",
                              command=lambda: threading.Thread(target=self.read_csv(self.csv_path_file)).start()
                              )
        start_button.grid(row=0, column=1)
        # start_button.pack()

        cancel_button = Button(frame3, text="Cancel", command=lambda: self.cancel_operation)
        cancel_button.grid(row=0, column=2)
        # cancel_button.pack()

    # def read_csv_thread(self):
    #     print('Starting read Csv thread')
    #     threading.Thread(target=self.read_csv(self.csv_path_file)).start()
    def update_progress(self, increment):
        print('increment-', increment)
        self.progress_var.set(self.progress_var.get() + increment)
        self.csv_window.update_idletasks()

    def cancel_operation(self):
        self.cancel_op.set(True)
        print('self.cancel_op.get()', self.cancel_op.get())
        # self.csv_window.destroy()

    def text_to_speech(self, tts_content='', output_file='ttsAudio.wav', language='en'):
        print(" Text - To - Speech - Module")
        flag = 'n'
        lang_flag = False
        try:
            for key in self.LANGUAGES:
                if self.LANGUAGES[key] == self.tts_lang.get():
                    language = key
                    lang_flag = True
        except:
            print('Error')
        if lang_flag == False:
            language = 'en'

        if tts_content == "":
            flag = 'y'
            tts_content = self.tts_field.get()

        if tts_content == "":
            messagebox.showerror("Error",
                                 "TexT Field Empty  , Check Logs for more "
                                 "Information")
        else:
            print("tts_content - ", tts_content)
            print("language - ", language)
            print("output_file - ", output_file)

            try:
                tts = gTTS(text=tts_content, lang=language, slow=False)
            except Exception as e:
                print("Exception - gTTS-", e)
                messagebox.showerror("gTTS Error", "gTTS has Failed , Check Logs for more Information")

            try:
                tts.save(output_file)
            except:
                print("Exception - gTTS")

            # try:
            self.convert_to_ivr_audio(output_file, "mono", 8000, "mu-law", output_file)

            if flag == 'y':
                messagebox.showinfo("operation complete", "Files saved in destination DIR")

    def convert_to_ivr_audio(self, _file, channel, target_sample_rate, compression, op_file_name, processor='librosa'):
        print('file_name : ', _file)
        print('Audio Processor : ', processor)
        print('Channel : ', channel)
        print('target_sample_rate :', target_sample_rate)
        print('compression :', compression)
        print('op_file_name :', op_file_name)

        if self.dest_path != '':
            op_file_name = self.dest_path + '/' + op_file_name
            print('op_file_name :', op_file_name)

        if processor == 'librosa':
            print('using - librosa')
            try:

                audio_signal_og, sampling_rate_og = librosa.load(_file, dtype=np.float32)
                print("audio_signal_og", audio_signal_og)
                print("audio_signal_og", sampling_rate_og)
                # Step 3: Resample to 8 kHz
                audio_resampled = librosa.resample(audio_signal_og, orig_sr=sampling_rate_og,
                                                   target_sr=target_sample_rate)
                print('Audio Resampled - ')

                if len(audio_resampled.shape) > 1:
                    print('--applying mono--')
                    audio_mono = librosa.to_mono(audio_resampled).astype(dtype=np.float32)
                else:
                    print('--already mono--')
                    audio_mono = audio_resampled



                sf.write(op_file_name, audio_mono, target_sample_rate, 'PCM_16')

                # audio_8bit = AudioSegment.from_wav(op_file_name)
                #
                # # Set the desired bitrate (64 kbps in this case)
                # target_bitrate = "64k"
                # audio_8bit.export(op_file_name, format="wav", bitrate=target_bitrate)
                print('write complete')
            except Exception as e:
                print("Error Converting Audio - ", e)
                messagebox.showerror("Error",
                                     "Exception In Audio Processing, Check Logs for more "
                                     "Information")


if __name__ == "__main__":
    root = tkinter.Tk()
    app = TtsToIvr(root)
    root.mainloop()
