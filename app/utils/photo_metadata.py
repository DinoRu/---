from io import BytesIO

import requests
from PIL import Image
from PIL.ExifTags import TAGS
from app.utils.coordinates import Coordinates


class PhotoMetadata:
	@staticmethod
	def _get_exif_data(photo: bytes) -> dict:
		"""Extract EXIF data from the photo."""
		try:
			with BytesIO(photo) as img_buf:
				with Image.open(img_buf) as img:
					exif = img._getexif()
					if exif:
						return {TAGS.get(tag, tag): value for tag, value in exif.items()}
		except Exception as e:
			print(f"Error extracting EXIF data: {e}")
		return {}

	@staticmethod
	def _convert_to_degrees(value: tuple) -> float:
		"""Convert GPS coordinates from degrees, minutes, seconds to decimal format."""
		degrees, minutes, seconds = value
		return degrees + (minutes / 60) + (seconds / 3600)

	def get_coordinate(self, photo: bytes) -> Coordinates | None:
		"""Get the GPS coordinates from the photo's EXIF data."""
		exif_data = self._get_exif_data(photo)
		gps_info = exif_data.get("GPSInfo")

		if gps_info:
			try:
				latitude = self._convert_to_degrees(gps_info[2])
				longitude = self._convert_to_degrees(gps_info[4])

				# Adjust for hemisphere
				if gps_info[1] == 'S':
					latitude = -latitude
				if gps_info[3] == 'W':
					longitude = -longitude

				return Coordinates(latitude=latitude, longitude=longitude)
			except (IndexError, KeyError, TypeError) as e:
				print(f"Error parsing GPS coordinates: {e}")

		print("No GPS information found in photo.")
		return None

	def get_coordinate_from_url(self, url: str) -> Coordinates | None:
		""" Download image from URL and get GPS coordinates."""
		try:
			response = requests.get(url)
			response.raise_for_status()
			return self.get_coordinate(response.content)
		except requests.RequestException as e:
			print(f"Error fetching image from URL: {e}")
		return None





photo_metadata = PhotoMetadata()
