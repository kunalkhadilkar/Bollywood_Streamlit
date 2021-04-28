import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import pandas as pd
import nltk
from PIL import Image
nltk.download('punkt')

st.title("Fair is Actually Unfair: Uncovering Gender and Racial Bias in Movies")
st.header("A crowdsourcing effort to collect incidents of gender bias, colorism and misogyny in movies all over the world.")

st.sidebar.title("Bias Analysis")
st.sidebar.markdown("Choose between different options")
option = st.sidebar.selectbox("Choose:",   ('','Calculate Gender Bias', 'Write a movie Review'),format_func=lambda x: 'Select an option' if x == '' else x)

if option=='':
	st.subheader('Try out live demo of by transcripts and getting a gender bias score')
	st.subheader('Did you come across bias in a movie you recently watched? Submit a review.')
	st.write('Research by Kunal Khadilkar, Ashique KhudaBukhsh, Tom Mitchell')
	st.write('Read our paper [here](https://arxiv.org/abs/2102.09103).')

def calculate_MPR(file_name):
	corpus_string = ""
	with open(file_name,'r',encoding="ISO-8859-1") as f:
		for line in f:
			if "-->" not in line:
				corpus_string += line.strip("\n") + " "
		#st.write(corpus_string)
	word_tokenizer = nltk.word_tokenize(corpus_string)
	word_tokenizer = [word.lower() for word in word_tokenizer]
	he_count = word_tokenizer.count('he')
	him_count = word_tokenizer.count('him')
	she_count = word_tokenizer.count('she')
	her_count = word_tokenizer.count('her')
	MPR = (he_count+him_count)/(he_count+him_count+she_count+her_count)
	st.write('Male Pronoun Ratio is: ',MPR)


if option=='Calculate Gender Bias':
	st.header('Calculate Male Pronoun Ratio')
	st.write('Male Pronoun Ratio (MPR) can be calculated for any movie transcript. Mathematically it can be expressed as:')
	st.latex(r'''MPR = \frac{\text{(Occurences of 'he') + (Occurences of 'him')}}{\text{(Occurences of 'he') + (Occurences of 'him') + (Occurences of 'she') + (Occurences of 'her')}}''')
	st.write('A MPR of 0.5 suggests equal gendered pronoun usage. MPR > 0.5 indicates higher use of male pronouns than female pronouns in the movie dialogs.')
	expander_2 = st.beta_expander("Try out a live demo")
	with expander_2:
		radio_option = st.radio("Try it out",('Upload a movie subtitle file', 'Calculate MPR for sample movies'))
		if radio_option=='Upload a movie subtitle file':
			uploaded_file = st.file_uploader("Upload Files",type=['.txt','.srt'])
			if uploaded_file is not None:
				st.write("Uploaded successfully")
				calculate_MPR(str(uploaded_file.name))
		else:
			movie_option = st.selectbox("Choose a movie:",   ('','Housefull', 'Spectre','American Sniper','Kal Ho Na Ho','Student Of The Year','P.S. I Love You'),format_func=lambda x: 'Select an option' if x == '' else x)
			if movie_option=='Housefull':
				calculate_MPR('Housefull.srt')
			if movie_option=='Spectre':
				calculate_MPR('Spectre.srt')
			if movie_option=='American Sniper':
				calculate_MPR('American Sniper.srt')
			if movie_option=='Kal Ho Na Ho':
				calculate_MPR('KalHoNaaHo.srt')
			if movie_option=='Student Of The Year':
				calculate_MPR('Student_of_the_year.srt')
			if movie_option=='P.S. I Love You':
				calculate_MPR('PSILoveYou.srt')

	expander_1 = st.beta_expander("Large Scale MPR Research and Insights")
	with expander_1:
		st.write('In the past, the MPR for books and movies was in the high 60s and 70s. We can see that books have achieved gender pronoun parity in recent years, but movies are still lagging behind. This shows the difference between the two mediums of books and movies, when it comes to gendered pronoun usage.')
		image = Image.open('MPR_Extended.png')
		st.image(image,caption='MPR over the years')

elif option=='Write a movie Review':
	st.header('Share your reviews regarding why the movie was biased?')
	st.subheader('Explain your answers:')
	movie_name = st.text_input("Enter movie name")
	bias_reason = st.text_input("Why do you think the movie is biased? Were there occupational stereotypes? Was colorism portrayed in movies? Were there any objectionable dialogs?")
	bias_rating = st.text_input("Give a rating between 0 to 5, where 0 indicates least biased and 5 indicates highly biased")
	if st.button('Submit Review'):
		if len(movie_name)>0 and len(bias_rating)>0 and len(bias_reason)>0:
			df = pd.read_csv('anon_reviews.csv')
			df = df.append({'Movie Name':movie_name,'Bias Reason':bias_reason,'Bias Rating':bias_rating},ignore_index=True)
			df.to_csv('anon_reviews.csv',index=False)

	df = pd.read_csv('anon_reviews.csv')
	st.write('Here are some other movies people have reviewed:')
	if len(df)>0:
		for index,row in df.iterrows():
			st.text("-----------------------------------------------------------")
			st.text("Movie Name: "+str(row['Movie Name']) + "\nBias Reason: "+str(row['Bias Reason']) + "\nBias Rating: "+str(row['Bias Rating']))
