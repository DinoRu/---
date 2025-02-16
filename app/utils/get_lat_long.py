from exif import Image


async def get_coordinates_from_photo(photo_url: str):
    """
    	Download Image from URL and extract coordinates.
    """
    import aiohttp

    async with aiohttp.ClientSession() as session:
        async with session.get(photo_url) as resp:
            if resp.status == 200:
                photo_bytes = await resp.read()

                img = Image(photo_bytes)
                if img.has_exif:
                    if img.gps_latitude and img.gps_longitude:
                        latitude = convert_to_decimal(img.gps_latitude, img.gps_latitude_ref)
                        longitude = convert_to_decimal(img.gps_longitude, img.gps_longitude_ref)
                        return latitude, longitude
    return None, None

def convert_to_decimal(gps_data, ref):
    """
   		Convert data to decimal.
    """
    d, m, s = gps_data
    decimal = d + (m / 60.0) + (s / 3600.0)
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal