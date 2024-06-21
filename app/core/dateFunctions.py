
import datetime
from pprint import pprint


class DateFunctions:

    @staticmethod
    async def return_current_timestamp():
        # Get the current time
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d_%H:%M:%S_%f")

    @staticmethod
    async def add_current_timestamp(item: dict, date_column_name=''):
        try:
            # Get the current time
            now = datetime.datetime.now()
            suffix = await DateFunctions.add_suffix(now)

            # Format the time using strftime and the desired format string
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S:%f")

            column_name = date_column_name if len(date_column_name) > 0 else 'date_created'

            # add update properties
            item[column_name] = {
                'timestamp': timestamp,
                'timestamp_id': now.strftime("%Y%m%d%H%M%S%f"),
                'date': timestamp[:-3],
                'formatted_date_short': now.strftime(f"%d{suffix} %b %Y"),
                'formatted_date_long': now.strftime(f"%d{suffix} %B %Y"),
                'formatted_date_time': now.strftime("%I:%M %p"),
                'time_of_the_day': await DateFunctions.time_of_day(now),
                'day': now.day,
                'day_suffix': suffix,
                'day_name_short': now.strftime("%a"),
                'day_name_long': now.strftime("%A"),
                'hour': now.hour,
                'hour_formatted': now.strftime("%I:%p"),
                'minute': now.minute,
                'month_number': now.month,
                'month_short': now.strftime("%b"),
                'month_long': now.strftime("%B"),
                'Year': now.year,
                'week_number': now.isocalendar()[1]
            }

            return item
        except Exception as e:
            return {}

    @staticmethod
    async def add_payback_timestamp(item: dict, payback_date, date_column_name=''):
        try:
            from datetime import datetime

            # Format the payback date using strftime and the desired format string
            try:
                payback_date = DateFunctions.convert_date_time_from_form(payback_date)
            except Exception as e:
                pass

            try:
                timestamp = payback_date.strftime("%Y-%m-%d %H:%M:%S:%f")
            except Exception as e:
                timestamp = DateFunctions.convert_date_time_from_form(payback_date)

            column_name = date_column_name if len(date_column_name) > 0 else 'payback_date'

            # add payback properties
            item[column_name] = {
                'timestamp': timestamp,
                'timestamp_id': payback_date.strftime("%Y%m%d%H%M%S%f"),
                'date': timestamp[:-3],
                'formatted_date_short': payback_date.strftime(f"%dth %b %Y"),
                'formatted_date_long': payback_date.strftime(f"%dth %B %Y"),
                'formatted_date_time': payback_date.strftime("%I:%M %p"),
                'time_of_the_day': await DateFunctions.time_of_day(payback_date),
                'day': payback_date.day,
                'day_suffix': payback_date.strftime("%S"),
                'day_name_short': payback_date.strftime("%a"),
                'day_name_long': payback_date.strftime("%A"),
                'hour': payback_date.hour,
                'hour_formatted': payback_date.strftime("%I:%p"),
                'minute': payback_date.minute,
                'month_number': payback_date.month,
                'month_short': payback_date.strftime("%b"),
                'month_long': payback_date.strftime("%B"),
                'Year': payback_date.year,
                'week_number': payback_date.isocalendar()[1]
            }

            return item
        except Exception as e:
            return item

    @staticmethod
    async def time_elapsed(date_string):
        try:
            now = datetime.datetime.now()
            date = datetime.datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S:%f')
            delta = now - date
            seconds = delta.total_seconds()

            if seconds < 0:
                return 'in the future'

            time_units = [(60, 'second'), (60, 'minute'), (24, 'hour'), (30, 'day'), (12, 'month'), (10, 'year'),
                          (10, 'decade')]
            result_units = ['second', 'minute', 'hour', 'day', 'month', 'year', 'decade', 'century']

            for i, (unit, unit_name) in enumerate(time_units):
                if seconds < unit:
                    count = int(seconds)
                    unit_name = unit_name if count == 1 else unit_name + 's'
                    return f'{count} {unit_name} ago'
                seconds /= unit

            count = int(seconds)
            unit_name = result_units[len(time_units)]
            unit_name = unit_name if count == 1 else unit_name + 's'
            return f'{count} {unit_name} ago'
        except Exception as e:
            return ""

    @staticmethod
    def str_to_bool(date):
        try:
            # If the string is 'false' or '0', return False
            if date and date.lower() in ('false', '0'):
                return False
            # Otherwise, return the original string
            else:
                return date
        except Exception as e:
            return date

    @staticmethod
    def in_date_range(date_created, start_date=False, end_date=False):
        try:
            from datetime import datetime

            start_date = DateFunctions.str_to_bool(start_date)
            end_date = DateFunctions.str_to_bool(end_date)

            # Remove the space and the microseconds from the date string
            date_created = datetime.strptime(date_created, "%Y-%m-%d %H:%M:%S:%f").date()

            if not start_date and not end_date:
                return True

            if start_date and not end_date:
                # Remove the space and the microseconds from the start_date string
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                return date_created >= start_date

            if end_date and not start_date:
                # Remove the space and the microseconds from the end_date string
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                return date_created <= end_date

            if start_date and end_date:
                # Remove the space and the microseconds from the start_date and end_date strings
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                return start_date <= date_created <= end_date

            return False
        except Exception as e:
            return False

    @staticmethod
    def convert_date_time_from_form(manual_date_created):
        from datetime import datetime, timedelta
        try:
            converted_date = datetime.strptime(manual_date_created, '%Y-%m-%d')
            start_date = datetime.now()
            return converted_date.replace(hour=start_date.hour, minute=start_date.minute, second=start_date.second,
                                          microsecond=start_date.microsecond)
        except Exception as e:
            return manual_date_created

    @staticmethod
    async def add_last_updated_timestamp(item: dict):
        return await DateFunctions.add_current_timestamp(item, 'last_updated')

    @staticmethod
    async def add_suffix(date):
        try:
            day = date.strftime("%d")
            if day in ["01", "21", "31"]:
                suffix = "st"
            elif day in ["02", "22"]:
                suffix = "nd"
            elif day in ["03", "23"]:
                suffix = "rd"
            else:
                suffix = "th"
            return suffix
        except Exception as e:
            return ""

    @staticmethod
    async def time_of_day(time):
        try:
            hour = time.hour
            if 6 <= hour < 12:
                return "morning"
            elif 12 <= hour < 17:
                return "afternoon"
            elif 17 <= hour < 21:
                return "evening"
            else:
                return "night"
        except Exception as e:
            return ""
