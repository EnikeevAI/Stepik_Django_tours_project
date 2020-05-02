import random

from django.shortcuts import render
from django.views import View

from .data.stepik_tours_data import departures, tours


class MainView(View):
    def get(self, request, *args, **kwargs):
        tours_on_page = {tour_id: tours[tour_id] for tour_id in random.sample(list(tours.keys()), 6)}
        return render(
            request, 'tours/index.html',
            context={
                'departures': departures,
                'tours': tours_on_page
            }
        )


class DepartureView(View):
    def get_departure_tours_info(self, departure, tours=tours):
        max_price, min_price, max_nights, min_nights = None, None, None, None
        tours_on_page = {}
        for tour_id, tour in tours.items():
            if departure == tour['departure']:
                max_price = max(tour['price'], max_price) if max_price else tour['price']
                min_price = min(tour['price'], min_price) if min_price else tour['price']
                max_nights = max(tour['nights'], max_nights) if max_nights else tour['nights']
                min_nights = min(tour['nights'], min_nights) if min_nights else tour['nights']
                stats = {'max_price': max_price, 'min_price': min_price,
                         'max_nights': max_nights, 'min_nights': min_nights}
                tours_on_page[tour_id] = tour
        return tours_on_page, stats

    def get(self, request, *args, **kwargs):
        tours_on_page, tours_stats = self.get_departure_tours_info(kwargs['departure'])
        return render(
            request, 'tours/departure.html',
            context={
                'departures': departures,
                'departure_from': departures[kwargs['departure']],
                'tours': tours_on_page,
                'tours_stats': tours_stats
            }
        )


class TourView(View):
    def get(self, request, *args, **kwargs):
        tour_id = kwargs['id']
        tour_departure = departures[tours[tour_id]['departure']]
        return render(
            request, 'tours/tour.html',
            context={
                'departures': departures,
                'tour': tours[tour_id],
                'tour_departure': tour_departure
            }
        )
