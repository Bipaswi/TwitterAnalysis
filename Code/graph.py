%matplotlib inline
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas
from parse import parse_data
from analyse import analyse_entities
from os import path

#d = path.dirname("../Data/digifest16.csv")

# Read the whole text.
#text = open(path.join(d, 'constitution.txt')).read()
#data = parse_data("../Data/digifest16.csv")
#hashtags = analyse_entities(data, 'hashtags', 'text')
#print(hashtags.max())
# Generate a word cloud image
wordcloud = WordCloud().generate(str(hashtags))

# Display the generated image:
# the matplotlib way:
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
pylab.rcParams['figure.figsize'] = 14, 10



# take relative word frequencies into account, lower max_font_size
wordcloud = WordCloud(stopwords=STOPWORDS,
                          background_color='white',
                          width=1800,
                          height=1400).generate(str(hashtags))
plt.figure()
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig('./hashtag_cloud.png', dpi=300)
plt.show()

