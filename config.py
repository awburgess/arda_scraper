ARDA_ESRI_REST_ENDPOINT = 'http://maps.nazarene.org/arcgis/rest/services/ARDA/InfoGroupChurches/MapServer/0/query?f=json&where=&returnGeometry=true&spatialRel=esriSpatialRelIntersects&geometry={{%22xmin%22:{xmin},%22ymin%22:{ymin},%22xmax%22:{xmax},%22ymax%22:{ymax},%22spatialReference%22:{{%22wkid%22:4326,%22latestWkid%22:4326}}}}&geometryType=esriGeometryEnvelope&inSR=4326&outFields=COMPANY_NA,ADDRESS,CITY,STATE,ZIP_CODE,DENOM_DESC&outSR=4326'

COUNTIES_PATH = 'data/tl_2017_us_county.shp'
STATE_FIPS_XWALK = 'data/fips_state_xwalk.csv'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36'