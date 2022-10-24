QUERY_WISHES_RESERVED_BY_ME = """
    SELECT 
      wl.id
    , wl.name AS wish_name
    , wl.image_link
    , wl.product_link
    , u.name AS username
    , u.birthdate 
    FROM wish_histories wh 
        JOIN wishlists wl ON wl.id = wh.wish_id	
                        AND wh.tg_id_who_chose = {tg_id}
        JOIN users u ON u.id = wl.user_id 
    WHERE CONVERT_TZ(NOW(),'+00:00','+03:00') BETWEEN wh.start_datetime AND IFNULL(wh.end_datetime , STR_TO_DATE('01-01-2099', '%d-%m-%Y'))
"""