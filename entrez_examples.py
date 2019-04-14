import re
from collections import Counter
import plotly.plotly as py
import plotly.tools as tls
import matplotlib.pyplot as plt

# They might be some issues here so...
try:
    from Bio import Entrez
except:
    print("Run: {} to install Bio module.".format("pip install biopython"))


# Based on https://biopython.org/DIST/docs/api/Bio.Entrez-module.html

class BioScraper(object):

    def __init__(self, email):
        self.email = email
        self.all_databases = []
        self.histogram = {}

    def get_data(self, biodatabase, bioterm):
        """
        Gets data from Emrez database

        :param biodatabase: Emrez database
        :param bioterm: Given term

        :return: histogram
        """

        Entrez.email = self.email

        # Get all databases
        handle = Entrez.einfo()
        self.all_databases = handle.read()


        # Get articles from pubmed db containing biopython term
        handle = Entrez.esearch(db=biodatabase, term=bioterm)
        records = Entrez.read(handle)

        # All records related to the term
        recordsIds = records['IdList']

        found_year = None
        years_statistics = []

        for recordId in recordsIds:
            article = Entrez.efetch(db=biodatabase, id=recordId, rettype="gb", retmode="text")
            data = article.read()

            # Find year
            for d in data.split():
                year = re.match(r'.*([1-3][0-9]{3})', d)
                if year and len(year.string) == 4:
                    found_year = year.string
                    years_statistics.append(found_year)
                    break

        self.histogram = Counter(years_statistics)

        return years_statistics

    def plot_histogram(self, years_statistics, outputfile):
        """
        Plots histogram at the basis of given data list and stores it into file.

        :param years_statistics: Statistics for years
        :param outputfile: Output filename
        """

        plt.hist(years_statistics)
        plt.title("Statistics for years")
        plt.xlabel("Value")
        plt.ylabel("Frequency")

        fig = plt.gcf()
        plotly_fig = tls.mpl_to_plotly( fig )
        py.iplot(plotly_fig, filename=outputfile)

if __name__ == "__main__":

    b = BioScraper("Marcin@example.com")
    histogram_data = b.get_data('pubmed', 'biopython')
    b.plot_histogram(histogram_data, 'output.png')