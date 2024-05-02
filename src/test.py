import cloudinary.api
import cloudinary

cloudinary.config(
    cloud_name="dzygv07en",
    api_key="316176596399777",
    api_secret="yfINC_0-evVT33Du_TkIbug5bkw"
)
result = cloudinary.api.resource_by_asset_id("3689c293c7dc306190708c463328aa67")