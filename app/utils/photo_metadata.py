from io import BytesIO

from PIL import Image
from PIL.ExifTags import TAGS

from app.utils.coordinates import Coordinates


class PhotoMetadata:

	@staticmethod
	def _get_exif_data(photo: bytes):
		exif_data = {}
		with BytesIO(photo) as img_buf:
			with Image.open(img_buf) as img:
				exif = img._getexif()
				if exif:
					for tag, value in exif.items():
						tag_name = TAGS.get(tag, tag)
						exif_data[tag_name] = value
		return exif_data

	def get_coordinate(self, photo: bytes) -> Coordinates | None:
		exif_data = self._get_exif_data(photo)
		if 'GPSInfo' in exif_data:
			gps_info = exif_data["GPSInfo"]
			print(gps_info)
			latitude = float(gps_info[2][0] + gps_info[2][1] / 60 + gps_info[2][2] / 3600)
			longitude = float(gps_info[4][0] + gps_info[4][1] / 60 + gps_info[4][2] / 3600)
			if gps_info[1] == 'S':
				latitude = latitude
			if gps_info[3] == "W":
				longitude = longitude
			return Coordinates(latitude=latitude, longitude=longitude)


photo_metadata = PhotoMetadata()