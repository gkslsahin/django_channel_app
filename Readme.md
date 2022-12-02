# Django Channel App
This project provides channels and sub-channels under it via rest api. The project consists of 3 models. Channel which is the main channel, Subchannel below it and Content showing the content.
Under a channel, there can be a subchannel or a direct content. 

# calculate rate managment command
calculate_rate.py
This command calculates the rate values of the channels and writes them to the csv file in order.
- run `python3 namage.py calculate_rate`

# endpoint
## Get all data

```
GET /api/channels
```
`curl --request GET --url http://localhost:8000/api/channels`

## Response

```
{
	"tvshows": [
		{
			"id": 1,
			"title": "tvshows",
			"image": "tvshows_icon"
		},
		{
			"id": 1,
			"channel": 1,
			"title": "vikins",
			"image": "viking.image.path",
			"info_sub_channel": "tv series about vikins"
		},
		{
			"id": 1,
			"channel": null,
			"sub_channel": 1,
			"name": "season 1 first episode",
			"image": "image.vikins.e1",
			"language": "tr,sp,en",
			"content_info": "this episiode about lorem ipsum1",
			"file": "vikins1e1.mp4",
			"rate": 7
		},
		{
			"id": 2,
			"channel": null,
			"sub_channel": 1,
			"name": "season 1 second episode",
			"image": "image.vikins.e2",
			"language": "tr,sp,en",
			"content_info": "this episiode about lorem ipsum2",
			"file": "vikins1e1.mp4",
			"rate": 4
		},
		{
			"id": 3,
			"channel": 1,
			"sub_channel": null,
			"name": "Oscar Awards 2022",
			"image": "image.oscar",
			"language": "en",
			"content_info": "2022 oscar awards ceremony",
			"file": "oscar.mp4",
			"rate": 10
		}
	]
}
```

