#!/usr/bin/env python3
#coding: utf-8

import speech_recognition as sr



import re
import string
import os
import subprocess
import fileinput
import pandas as pd
import numpy as np

from sklearn.neural_network import MLPClassifier

mlp_relatives = MLPClassifier(hidden_layer_sizes=(5,5), max_iter=500)

mlp_QU = MLPClassifier(hidden_layer_sizes=(100,100), max_iter=1000)





class Error(Exception):
    """Base class for other exceptions"""
    pass
class ValueTooSmallError(Error):
    pass
class ValueTooLargeError(Error):
    pass
class NotADirectoryError(Error):
    pass
class InvalidName(Error):
    pass
class InvalidName2(Error):
    pass
class InvalidName3(Error):
    pass
class InvalidName4(Error):
    pass
class FileOverriden(Error):
    pass


output_path = os.path.join(os.getcwd(), '')


while True:
    try:
        output_path = input('Where would you like to save the output? Enter a directory: ')
        if not os.path.isdir(output_path):
            raise FileNotFoundError
        break
    except FileNotFoundError:
        print('Not a directory. Try again.')

while True:
    try:
        name_question = input('How would you like to name the file? ')
        if re.match('((\s)*(\S)*(\s)*)*[.](\s)*(\S)*(\s)*', name_question):
            raise InvalidName
        elif re.match('^$', name_question):
            raise InvalidName2
            break
        elif re.match('((\S)*(\s)+(\S)*)+', name_question):
            raise InvalidName3
            break
        elif re.match('(\S)*[^a-zA-Z\d_](\S)*', name_question):
            raise InvalidName4
            break
        elif os.path.isfile('{0}{1}.TextGrid'.format(output_path, name_question)):
            user_warning = input('Warning! File already exists. Do you want to override it? [y] or [n]')
            if user_warning == 'y':
                print('File overriden.')
                break
            elif user_warning == 'n':
                print('Type name again.')
            else:
                user_answer = input('Answer [y] or [n].')
                while True:
                    if user_answer == 'y':
                        print('File overriden')
                        break
                    elif user_answer == 'n':
                        print('Type name again')
                        break
                    else:
                        print('Answer [y] or [n].')
        else:
            break
    except InvalidName:
        print('Enter a name without extension and spaces.')
    except InvalidName2:
        print('File name can\'t be null. Enter any name.')
    except InvalidName3:
        print('File name can\'t contain any spaces.')
    except InvalidName4:
        print('File name can\'t contain any non-alphanumeric characters save for underscores.')



output_path_2 = 'idTG$ = "{0}{1}.TextGrid"'.format(output_path,name_question)

audio_path_2 = 'file$ = "%s"' %name_question

full_path = '{0}{1}.TextGrid'.format(output_path, name_question)



r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)



# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    first_option = ("1. Google Speech Recognition thinks you said: " + r.recognize_google(audio))
    print(first_option)
    first_label = r.recognize_google(audio)
except sr.UnknownValueError:
    print("1. Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))


# recognize speech using Houndify
HOUNDIFY_CLIENT_ID = "jtPz2pl5Sf8kP3fjyBXoSw=="  # Houndify client IDs are Base64-encoded strings
HOUNDIFY_CLIENT_KEY = "ZX7MST4J3robF8Vl8KwuVAW3rj3Vjk9R4wq8EibG9ajYXM0Ts5CopgQXOfiZU9RwjQK5DP5M4Kg80qb_K2gU_g=="  # Houndify client keys are Base64-encoded strings
try:
    second_option = ("2. Houndify thinks you said: " + r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY))
    print(second_option)
    second_label = r.recognize_houndify(audio, client_id=HOUNDIFY_CLIENT_ID, client_key=HOUNDIFY_CLIENT_KEY)
except sr.UnknownValueError:
    print("2. Houndify could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Houndify service; {0}".format(e))



# recognize speech using Wit.ai
WIT_AI_KEY = "Q225NDYFNNOUWLX43ZPXDV6JYWZI57NT"  # Wit.ai keys are 32-character uppercase alphanumeric strings
try:
    third_option = ("3. Wit.ai thinks you said: " + r.recognize_wit(audio, key=WIT_AI_KEY))
    print(third_option)
    third_label = r.recognize_wit(audio, key=WIT_AI_KEY)
except sr.UnknownValueError:
    print("3. Wit.ai could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Wit.ai service; {0}".format(e))



# recognize speech using Sphinx
try:
    fourth_option = ("4. Sphinx thinks you said: " + r.recognize_sphinx(audio))
    print(fourth_option)
    fourth_label = r.recognize_sphinx(audio)
except sr.UnknownValueError:
    print("4. Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))





while True:
    try:
        question_1 = input('Which transcription do you prefer? Tell me the number: ')
        if question_1 == '1':
            result = first_label
            break
        elif question_1 == '2':
            result = second_label
            break
        elif question_1 == '3':
            result = third_label
            break
        elif question_1 == '4':
            result = fourth_label
            break
        else:
            print('Number out of range. Try again.')
    except NameError:
        print('Pick a non-null label.')

# write audio to a WAV file
with open("{0}.wav".format(name_question), "wb") as f:
    f.write(audio.get_wav_data())
    
    path_to_file = '{0}{1}.wav'.format(output_path, name_question)
    
    output_path_2 = 'idTG$ = "{0}{1}.TextGrid"'.format(output_path,name_question)
    
    audio_path_2 = 'file$ = "{0}"'.format(path_to_file)
    
    full_path = '{0}{1}.TextGrid'.format(output_path, name_question)

for line in fileinput.input('intervals_modified.praat', inplace=True):
    print (line.rstrip().replace('#add file here:', '%s' %audio_path_2))

for line in fileinput.input('intervals_modified.praat', inplace=True):
    print (line.rstrip().replace('#add TG here:', '%s' %output_path_2))

for line in fileinput.input('intervals_modified.praat', inplace=True):
    print (line.rstrip().replace('#add outpath here:', '%s' %output_path))

for line in fileinput.input('intervals_modified.praat', inplace=True):
    print (line.rstrip().replace('#add label here:', '%s' %result))

os.system ('/Applications/Praat.app/Contents/MacOS/Praat --run intervals_modified.praat')

#we now clean up the praat script and revert it to the original
for line in fileinput.input('intervals_modified.praat', inplace=True):
    print (line.rstrip().replace('{}'.format(audio_path_2), '#add file here:'))


#we now clean up the praat script and revert it to the original
for line in fileinput.input('intervals_modified.praat', inplace=True):
    print (line.rstrip().replace('{}'.format(output_path_2), '#add TG here:'))


#we now clean up the praat script and revert it to the original
for line in fileinput.input('intervals_modified.praat', inplace=True):
    print (line.rstrip().replace('{}'.format(output_path), '#add outpath here:'))


#we now clean up the praat script and revert it to the original
for line in fileinput.input('intervals_modified.praat', inplace=True):
    print (line.rstrip().replace('{}'.format(result), '#add label here:'))


audio_path_3 = 'name$ = "%s"' %name_question

output_path_3 = 'dir$ = "%s"' %output_path

grid_path = 'text$ = "%s"' %name_question

for line in fileinput.input('duration_silence.praat', inplace=True):
    print (line.rstrip().replace('#add name here:', '%s' %audio_path_3))

for line in fileinput.input('duration_silence.praat', inplace=True):
    print (line.rstrip().replace('#add grid here:', '%s' %grid_path))

for line in fileinput.input('duration_silence.praat', inplace=True):
    print (line.rstrip().replace('#add dir here:', '%s' %output_path_3))


os.system ('/Applications/Praat.app/Contents/MacOS/Praat --run duration_silence.praat')

#we now clean up the praat script and revert it to the original
for line in fileinput.input('duration_silence.praat', inplace=True):
    print (line.rstrip().replace('{}'.format(audio_path_3), '#add name here:'))


#we now clean up the praat script and revert it to the original
for line in fileinput.input('duration_silence.praat', inplace=True):
    print (line.rstrip().replace('{}'.format(grid_path), '#add grid here:'))


#we now clean up the praat script and revert it to the original
for line in fileinput.input('duration_silence.praat', inplace=True):
    print (line.rstrip().replace('{}'.format(output_path_3), '#add dir here:'))


xxx_path = '%sxxx.txt' %output_path


if re.findall(r'(\bwho\b|\bwhich\b)', result):
    
    data_rel = pd.DataFrame()

    data_rel['Type'] = ['NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC']
    data_rel['Duration_before'] = [110.42,35.778,66.593,51.377,np.nan,57.215,318.858,370.123,25.094,126.69,50.299,83,308.649,25.497,np.nan,73.173,108.322,np.nan,31.287,175.417,np.nan,np.nan,185.237,31.571,97.252,40.334,92.065,np.nan,np.nan,114.115,233.994,236.786,57.499,np.nan,111.81,79.501,np.nan,51.272,210.858,116.172,111.705,89.675,124.239,157.43,np.nan,205.506,68.629,164.257,87.708,159.511,61.293,41.431,98.157,np.nan,56.795,170.514,48.353,80.803,51.842,17.117,119.475,np.nan,np.nan,262.212,81.743,13.49,np.nan,np.nan,25.096,49.273,67.539,21.383,137.349,np.nan,np.nan,np.nan,np.nan,30.583,np.nan,27.148,np.nan,33.065,56.324,33.663,149.886,np.nan,np.nan,np.nan,34.131,np.nan,np.nan,np.nan,55.373,np.nan,np.nan,np.nan,np.nan,np.nan,109.49,np.nan,np.nan,91.466,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,77.655,91.351,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,93.779,41.636,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    data_rel['Duration_after'] = [50.995,90.953,118.322,np.nan,np.nan,111.069,84.879,277.815,np.nan,316.111,104.684,76.526,235.319,388.513,382.696,np.nan,95.095,89.909,99.699,78.749,50.903,91.481,126.331,np.nan,np.nan,141.555,np.nan,177.094,348.352,80.411,125.432,42.112,77.724,155.387,450.534,77.806,377.457,49.722,185.349,84.49,np.nan,np.nan,492.771,100.261,np.nan,np.nan,96.556,np.nan,83.622,66.302,434.5,417.119,np.nan,110.04,120.635,438.826,461.495,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,17.734,np.nan,272.691,np.nan,np.nan,np.nan,np.nan,208.681,np.nan,np.nan,64.228,48.188,np.nan,np.nan,np.nan,np.nan,np.nan,56.623,70.337,np.nan,np.nan,np.nan,40.643,52.335,49.527,79.501,29.551,np.nan,53.188,46.452,24.658,120.34,60.179,81.016,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,83.651,np.nan,np.nan,np.nan,np.nan,69.572,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    
    data_rel_neural = pd.DataFrame()
    
    data_rel_neural['Type'] = ['NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','NRRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC','RRC']
    data_rel_neural['Duration_before'] = [110.42,35.778,66.593,51.377,0,57.215,318.858,370.123,25.094,126.69,50.299,83,308.649,25.497,0,73.173,108.322,0,31.287,175.417,0,0,185.237,31.571,97.252,40.334,92.065,0,0,114.115,233.994,236.786,57.499,0,111.81,79.501,0,51.272,210.858,116.172,111.705,89.675,124.239,157.43,0,205.506,68.629,164.257,87.708,159.511,61.293,41.431,98.157,0,56.795,170.514,48.353,80.803,51.842,17.117,119.475,0,0,262.212,81.743,13.49,0,0,25.096,49.273,67.539,21.383,137.349,0,0,0,0,30.583,0,27.148,0,33.065,56.324,33.663,149.886,0,0,0,34.131,0,0,0,55.373,0,0,0,0,0,109.49,0,0,91.466,0,0,0,0,0,0,77.655,91.351,0,0,0,0,0,0,0,0,0,0,0,0,0,0,93.779,41.636,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    data_rel_neural['Duration_after'] = [50.995,90.953,118.322,0,0,111.069,84.879,277.815,0,316.111,104.684,76.526,235.319,388.513,382.696,0,95.095,89.909,99.699,78.749,50.903,91.481,126.331,0,0,141.555,0,177.094,348.352,80.411,125.432,42.112,77.724,155.387,450.534,77.806,377.457,49.722,185.349,84.49,0,0,492.771,100.261,0,0,96.556,0,83.622,66.302,434.5,417.119,0,110.04,120.635,438.826,461.495,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,17.734,0,272.691,0,0,0,0,208.681,0,0,64.228,48.188,0,0,0,0,0,56.623,70.337,0,0,0,40.643,52.335,49.527,79.501,29.551,0,53.188,46.452,24.658,120.34,60.179,81.016,0,0,0,0,0,0,83.651,0,0,0,0,69.572,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    X_rel = data_rel_neural.drop('Type', axis=1)
    
    y_rel = data_rel_neural['Type']
    
    mlp_relatives.fit(X_rel, y_rel)

    heard_string_QU = pd.DataFrame()

    with open(xxx_path, 'r') as working_file:
        content = working_file.readlines()
    content = [x.rstrip('\n') for x in content]

    while True:
        if len(content) < 4:
            print('It is a restrictive relative clause.')
            os.remove(xxx_path)
            break
        else:
            content_bef = content[1:2]
            content_bef = [float(i) for i in content_bef]
            content_aft = content[2:3]
            content_aft = [float(i) for i in content_aft]
            break

    print(content_bef)

    print(content_aft)

    heard_string_rel = pd.DataFrame()

    heard_string_rel['Duration_before'] = content_bef

    heard_string_rel['Duration_after'] = content_aft

    neural_rel_prediction = mlp.relatives.predict(heard_string_rel)

    print(natural_rel_prediction)

    n_NRRC = data_rel['Type'][data_rel['Type'] == 'NRRC'].count()

    n_RRC = data_rel['Type'][data_rel['Type'] == 'RRC'].count()

    total_types = data_rel['Type'].count()

    P_NRRC = n_NRRC/total_types

    P_RRC = n_RRC/total_types

    data_rel_means = data_rel.groupby('Type').mean()

    data_rel_variance = data_rel.groupby('Type').var()

    NRRC_duration_before_mean = data_rel_means['Duration_before'][data_rel_variance.index == 'NRRC'].values[0]

    NRRC_duration_before_variance = data_rel_variance['Duration_before'][data_rel_variance.index == 'NRRC'].values[0]

    NRRC_duration_after_mean = data_rel_means['Duration_after'][data_rel_variance.index == 'NRRC'].values[0]

    NRRC_duration_after_variance = data_rel_variance['Duration_after'][data_rel_variance.index == 'NRRC'].values[0]

    RRC_duration_before_mean = data_rel_means['Duration_before'][data_rel_variance.index == 'RRC'].values[0]

    RRC_duration_before_variance = data_rel_variance['Duration_before'][data_rel_variance.index == 'RRC'].values[0]

    RRC_duration_after_mean = data_rel_means['Duration_after'][data_rel_variance.index == 'RRC'].values[0]

    RRC_duration_after_variance = data_rel_variance['Duration_after'][data_rel_variance.index == 'RRC'].values[0]

    def p_x_given_y(x, mean_y, variance_y):
    
        p = 1/(np.sqrt(2*np.pi*variance_y)) * np.exp((-(x-mean_y)**2)/(2*variance_y))
    
        return p


    results_NRRC = list(P_NRRC * \
          p_x_given_y(heard_string_rel['Duration_before'], NRRC_duration_before_mean, NRRC_duration_before_variance) *\
          p_x_given_y(heard_string_rel['Duration_after'], NRRC_duration_after_mean, NRRC_duration_after_variance))

    results_RRC = list(P_RRC * \
          p_x_given_y(heard_string_rel['Duration_before'], RRC_duration_before_mean, RRC_duration_before_variance) *\
          p_x_given_y(heard_string_rel['Duration_after'], RRC_duration_after_mean, RRC_duration_after_variance))

    os.remove(xxx_path)
    
    print(results_NRRC)

    print(results_RRC)
    
    for i, j in zip(results_NRRC, results_RRC):
        if i > j:
            print('It is a non-restrictive relative clause.')
        else:
            print('It is a restrictive relative clause.')
    
    while True:
        user_question = input('Would you like to see the results? Press [y] or [n]. ')
        if user_question == 'y':
            subprocess.call(['open', full_path])
            subprocess.check_call(['open', '-a', '/Applications/Praat.app/Contents/MacOS/Praat', name_question])
            break
        elif user_question == 'n':
            break
        else:
            print('Press either [y] or [n] to continue.')


    
else:
    data_QU = pd.DataFrame()

    data_QU['Type'] = ['quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted']
    data_QU['Duration_before'] = [128.288,71.676,128.501,133.501,97.301,67.574,75.418,84.565,85.688,180.058,70.807,58.472,35.299,68.272,143.232,82.155,137.947,66.197,84.954,118.447,57.088,118.337,125.433,58.203,79.939,89.999,87.192,171.016,82.035,51.399,103.479,76.01,65.951,67.192,141.914,135.103,197.737,81.429,123.075,129.804,93.599,78.218,62.559,94.258,87.604,60.133,63.727,51.152,61.975,84.782,91.638,62.29,61.077,49.154,63.18,56.586,40.059,29.191,54.7,34.985,63.382,52.619,55.688,51.975,105.506,81.848,95.994,59.954,38.622,66.99,69.46,85.665,37.006,59.928,87.574,101.256,71.082,48.008,51.481,76.346,75.403,136.525,59.206,46.107,110.448,68.218,57.739,44.236,54.835,57.035]
    data_QU['Duration_after'] = [481.917,281.718,353.259,410.84,777.946,54.555,319.516,183.381,361.612,435.353,98.292,109.13,559.573,59.293,127.992,201.824,114.34,62.627,51.182,71.93,72.619,63.285,112.229,79.984,66.085,91.758,86.017,470.092,52.56,58.308,471.528,60.561,458.789,44.685,105.8, np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,374.306,423.76,387.705,64.251,95.807,368.933,26.816,75.224,61.975,70.89,202.393,125.328,40.531,232.22,55.013,65.418,413.168,233.889,313.5,52.746,91.728,69.52,75.029,83.262,80.5,145.956,61.429,85.852,175.866,83.005,62.29,79.505,51.047,146.076,48.66,56.496,95.059, np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]
    
    data_QU_neural = pd.DataFrame()
    
    data_QU_neural['Type'] = ['quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','quoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted','unquoted']
    data_QU_neural['Duration_before'] = [128.288,71.676,128.501,133.501,97.301,67.574,75.418,84.565,85.688,180.058,70.807,58.472,35.299,68.272,143.232,82.155,137.947,66.197,84.954,118.447,57.088,118.337,125.433,58.203,79.939,89.999,87.192,171.016,82.035,51.399,103.479,76.01,65.951,67.192,141.914,135.103,197.737,81.429,123.075,129.804,93.599,78.218,62.559,94.258,87.604,60.133,63.727,51.152,61.975,84.782,91.638,62.29,61.077,49.154,63.18,56.586,40.059,29.191,54.7,34.985,63.382,52.619,55.688,51.975,105.506,81.848,95.994,59.954,38.622,66.99,69.46,85.665,37.006,59.928,87.574,101.256,71.082,48.008,51.481,76.346,75.403,136.525,59.206,46.107,110.448,68.218,57.739,44.236,54.835,57.035]
    data_QU_neural['Duration_after'] = [481.917,281.718,353.259,410.84,777.946,54.555,319.516,183.381,361.612,435.353,98.292,109.13,559.573,59.293,127.992,201.824,114.34,62.627,51.182,71.93,72.619,63.285,112.229,79.984,66.085,91.758,86.017,470.092,52.56,58.308,471.528,60.561,458.789,44.685,105.8, 0,0,0,0,0,0,0,0,0,0,374.306,423.76,387.705,64.251,95.807,368.933,26.816,75.224,61.975,70.89,202.393,125.328,40.531,232.22,55.013,65.418,413.168,233.889,313.5,52.746,91.728,69.52,75.029,83.262,80.5,145.956,61.429,85.852,175.866,83.005,62.29,79.505,51.047,146.076,48.66,56.496,95.059, 0,0,0,0,0,0,0,0]


    X_QU = data_QU_neural.drop('Type', axis=1)
    
    y_QU = data_QU_neural['Type']
    
    mlp_QU.fit(X_QU, y_QU)

    heard_string_QU = pd.DataFrame()

    with open(xxx_path, 'r') as working_file:
        content = working_file.readlines()
    content = [x.rstrip('\n') for x in content]

    if len(content) < 4:
        print('There is at least one quoted string in the utterance.')
        os.remove(xxx_path)
        
    else:
        content_bef = content[:-2]
        content_bef = [float(i) for i in content_bef]
        content_aft = content[-1:]
        content_aft = [float(i) for i in content_aft]
        content_aft_new = content_bef[1:] + content_aft





    heard_string_QU['Duration_before'] = content_bef

    heard_string_QU['Duration_after'] = content_aft_new

    neural_QU_prediction = mlp_QU.predict(heard_String_QU)

    print(neural_QU_prediction)

    n_quoted = data_QU['Type'][data_QU['Type'] == 'quoted'].count()

    n_unquoted = data_QU['Type'][data_QU['Type'] == 'unquoted'].count()

    total_types = data_QU['Type'].count()

    P_quoted = n_quoted/total_types

    P_unquoted = n_unquoted/total_types

    data_QU_means = data_QU.groupby('Type').mean()

    data_QU_variance = data_QU.groupby('Type').var()

    quoted_duration_before_mean = data_QU_means['Duration_before'][data_QU_variance.index == 'quoted'].values[0]

    quoted_duration_before_variance = data_QU_variance['Duration_before'][data_QU_variance.index == 'quoted'].values[0]

    quoted_duration_after_mean = data_QU_means['Duration_after'][data_QU_variance.index == 'quoted'].values[0]

    quoted_duration_after_variance = data_QU_variance['Duration_after'][data_QU_variance.index == 'quoted'].values[0]

    unquoted_duration_before_mean = data_QU_means['Duration_before'][data_QU_variance.index == 'unquoted'].values[0]

    unquoted_duration_before_variance = data_QU_variance['Duration_before'][data_QU_variance.index == 'unquoted'].values[0]

    unquoted_duration_after_mean = data_QU_means['Duration_after'][data_QU_variance.index == 'unquoted'].values[0]

    unquoted_duration_after_variance = data_QU_variance['Duration_after'][data_QU_variance.index == 'unquoted'].values[0]

    def p_x_given_y(x, mean_y, variance_y):
    
        p = 1/(np.sqrt(2*np.pi*variance_y)) * np.exp((-(x-mean_y)**2)/(2*variance_y))
    
        return p






    results_quoted = list(P_quoted * \
                        p_x_given_y(heard_string_QU['Duration_before'], quoted_duration_before_mean, quoted_duration_before_variance) *\
                        p_x_given_y(heard_string_QU['Duration_after'], quoted_duration_after_mean, quoted_duration_after_variance))

    results_unquoted = list(P_unquoted * \
                        p_x_given_y(heard_string_QU['Duration_before'], unquoted_duration_before_mean, unquoted_duration_before_variance) *\
                        p_x_given_y(heard_string_QU['Duration_after'], unquoted_duration_after_mean, unquoted_duration_after_variance))

    print(results_quoted)

    print(results_unquoted)

    final_outcome_quoted = []

    final_outcome_unquoted = []

    for i, j in zip(results_quoted, results_unquoted):
        if i > j:
            final_outcome_quoted.append(i)
        else:
            final_outcome_unquoted.append(j)

    if len(final_outcome_quoted) > len(final_outcome_unquoted):
        print('There is at least one quoted string in the utterance.')
    else:
        print('There is no quoted string in the utterance.')




    os.remove(xxx_path)


    while True:
        user_question = input('Would you like to see the results? Press [y] or [n]. ')
        if user_question == 'y':
            subprocess.call(['open', full_path])
            subprocess.check_call(['open', '-a', '/Applications/Praat.app/Contents/MacOS/Praat', name_question])
            break
        elif user_question == 'n':
            break
        else:
            print('Press either [y] or [n] to continue.')


