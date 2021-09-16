-- name: get_places
-- Fetch all places from bigQuery.
SELECT * FROM oceana_twitter.twitter_place
LIMIT :limit
OFFSET :offset
