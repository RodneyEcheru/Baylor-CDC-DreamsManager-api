
from pprint import pprint
import re
from app.core.form import Form
from app.core.database import Database


class Pagination:
    @staticmethod
    async def pagination_details(page_number, page_size, total_records, url) -> dict:

        page_number = int(page_number)
        page_size = int(page_size)
        total_records = int(total_records)

        # Calculate total pages
        total_pages = (total_records + page_size - 1) // page_size if total_records > 0 else 0

        # Calculate skip value
        skip = (page_number - 1) * page_size

        # Calculate range of displayed entries
        start_entry = skip + 1
        end_entry = min(skip + page_size, total_records)

        # Create pagination links
        pagination_links = []
        max_links = 5
        middle_link = max_links // 2 + 1
        for i in range(max(1, page_number - middle_link + 1), min(total_pages + 1, page_number + middle_link)):
            link = {
                'page_number': i,
                'active_status': ' gridjs-currentPage' if i == page_number else '',
                'text': str(i),
                'url': f'{url}/{i}/{page_size}'
            }
            pagination_links.append(link)

        # Pagination details dictionary
        entries = f"""
        Showing {format(start_entry, ',')} to {format(end_entry, ',')} of {format(total_records, ',')} entries
        """
        pagination_details = {
            'showing_entries': entries,
            'first_page_link': f'{url}/1/{page_size}',
            'last_page_link': f'{url}/{total_pages}/{page_size}',
            'previous_page_link': f'{url}/{page_number - 1}/{page_size}' if page_number > 1 else '#!',
            'next_page_link': f'{url}/{page_number + 1}/{page_size}' if page_number < total_pages else '#!',
            'page_number': page_number,
            'page_size': page_size,
            'pagination_links': pagination_links,
            'total_pages': format(total_pages, ','),
            'total_records': format(total_records, ','),
        }

        return pagination_details

    @staticmethod
    async def paginated_items(page_number, page_size, collection, query_list_of_dictionaries=None, exclude_list_of_dictionaries=None) -> dict:
        page_number = int(page_number)
        page_size = int(page_size)
        items = await Database.fetch_many_items_paginated(
            collection,
            page_number,
            page_size,
            query_list_of_dictionaries,
            exclude_list_of_dictionaries
        )
        return items

    @staticmethod
    async def paginated_results(page_number, page_size, collection, url, query_list_of_dictionaries=None, exclude_list_of_dictionaries=None) -> dict:

        paginated_results = await Pagination.paginated_items(
            page_number,
            page_size,
            collection,
            query_list_of_dictionaries,
            exclude_list_of_dictionaries
        )

        paginated_results_count = await Database.count_items(collection, query_list_of_dictionaries, exclude_list_of_dictionaries)

        pagination_details = await Pagination.pagination_details(
            page_number, page_size, paginated_results_count, url
        )
        return {
            'results': paginated_results,
            'pagination_details': pagination_details,
            'total_count': paginated_results_count,
        }
