API_URL = 'https://SDMDataAccess.sc.egov.usda.gov/Tabular/post.rest?format=json'

VALUES_TEMPLATE = '''(geometry::STGeomFromText('{wkt}', 4326).MakeValid(), '{uuid}')'''

QUERY_TEMPLATE = '''
DROP TABLE IF EXISTS #temp_pasturemap_paddock;

CREATE TABLE #temp_pasturemap_paddock (
    id          INT NOT NULL IDENTITY PRIMARY KEY,
    coordinates GEOMETRY NOT NULL,
    paddock_uuid UNIQUEIDENTIFIER UNIQUE NOT NULL,
);

INSERT INTO #temp_pasturemap_paddock (coordinates, paddock_uuid) VALUES 
{values};

SELECT
       #temp_pasturemap_paddock.paddock_uuid,
       #temp_pasturemap_paddock.coordinates.STIntersection(mupolygon.mupolygongeo) AS intersection,
       component.rsprod_l AS forage_low,
       component.rsprod_r AS forage_regular,
       component.rsprod_h AS forage_high
FROM #temp_pasturemap_paddock
OUTER APPLY SDA_Get_Mupolygonkey_from_intersection_with_WktWgs84(#temp_pasturemap_paddock.coordinates.STAsText()) matching_polygon
JOIN mupolygon ON mupolygon.mupolygonkey = matching_polygon.mupolygonkey
JOIN component ON component.mukey = mupolygon.mukey
WHERE #temp_pasturemap_paddock.coordinates.STIsValid() = 1

UNION ALL 

SELECT 
    #temp_pasturemap_paddock.paddock_uuid,
    #temp_pasturemap_paddock.coordinates AS intersection,
    NULL AS forage_low,
    NULL AS forage_regular,
    NULL AS forage_high
FROM #temp_pasturemap_paddock
WHERE #temp_pasturemap_paddock.coordinates.STIsValid() = 0;
'''
