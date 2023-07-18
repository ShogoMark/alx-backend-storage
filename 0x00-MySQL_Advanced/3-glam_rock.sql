-- SQL script that lists all bands with Glam rock as their style
-- ranked by their year of longevity

SELECT band_name, (COALESCE(split, 2022) - formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock'
ORDER BY lifespan DESC;
