def get_current_utc():
    import datetime
    from django.utils import timezone
    return timezone.now()


def get_filename(filename):
    return filename.upper()

