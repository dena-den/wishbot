QUERY_WISHES_RESERVED_BY_ME = """
    SELECT 
      wl.id
    , wl.name AS wish_name
    , wl.product_link
    , u.name AS username
    , u.birthdate 
    FROM wish_histories wh 
        JOIN wishlists wl ON wl.id = wh.wish_id	
                        AND wh.tg_id_who_chose = {tg_id}
        JOIN users u ON u.id = wl.user_id 
    WHERE wh.end_datetime IS NULL
"""


QUERY_HOW_MANY_WISHES_ARE_RESERVED = """
  SELECT COUNT(1) AS `count`
  FROM wish_histories wh 
    JOIN wishlists w ON w.id = wh.wish_id 
    				AND w.user_id = {friend_user_id}
    				AND wh.end_datetime IS NULL
  WHERE wh.tg_id_who_chose = {my_tg_id}
"""


QUERY_UPSERT_HASH = """
  REPLACE INTO keyboard_hash (tg_id, hash)
  VALUES ({tg_id}, Null)
"""