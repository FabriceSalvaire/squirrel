####################################################################################################
#
# Babel - An Electronic Document Management System
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import matplotlib.pyplot as plt

from ..Math.Binning import Binning1D
from ..Math.Histogram import Histogram
from ..Math.Interval import Interval

####################################################################################################

def console_database_statistics(application, args):

    document_database = application.document_database
    document_table = document_database.document_table

    number_of_documents = document_table.query().count()
    print('Number of documents: {:_}'.format(number_of_documents))

    print('Distribution of the number of pages:')
    fine_histogram = Histogram(Binning1D(Interval(1, 500), 1))
    coarse_histogram = Histogram(Binning1D(Interval(1, 10_000), 100))
    for document in document_table.query():
        fine_histogram.fill(document.number_of_pages)
        coarse_histogram.fill(document.number_of_pages)
    # Fixme:
    # plt.plot(*page_histogram.to_graph()[:2])
    # plt.show()
    fine_histogram.normalise(scale=100)
    coarse_histogram.normalise(scale=100)
    for interval in (
            Interval(1, 10),
            Interval(11, 50),
            Interval(51, 100),
            Interval(101, 250),
            Interval(251, 500),
            Interval(500, 1000),
            Interval(1000, 10_000), # coarse_histogram.binning.sup
    ):
        if interval.inf >= 500:
            histogram = coarse_histogram
        else:
            histogram = fine_histogram
        sum, _ = histogram.integral(interval_x=interval)
        print('{0:5.1f} % for [{1.inf:_}, {1.sup:_}] pages'.format(sum, interval))
