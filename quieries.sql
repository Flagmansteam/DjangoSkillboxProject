select "shopapp_product"."id", "shopapp_product"."name", "shopapp_product"."description", "shopapp_product"."price", "shopapp_product"."discount
", "shopapp_product"."created_at", "shopapp_product"."created_by", "shopapp_product"."archived", "shopapp_product"."preview" from "shopapp_product" WHER
E NOT "shopapp_product"."archived" ORDER BY "shopapp_product"."name" ASC, "shopapp_product"."price" ASC;


select "shopapp_product"."id", "shopapp_product"."name", "shopapp_product"."description", "shopapp_product"."price", "shopapp_product"."discount
", "shopapp_product"."created_at", "shopapp_product"."created_by", "shopapp_product"."archived", "shopapp_product"."preview" from "shopapp_product" WHER
E "shopapp_product"."id" = 1 LIMIT 21;

select "shopapp_productimage"."id", "shopapp_productimage"."product_id", "shopapp_productimage"."image", "shopapp_productimage"."description" FR
OM "shopapp_productimage" WHERE "shopapp_productimage"."product_id" = 1;

SELECT ("shopapp_order_products"."order_id") AS "_prefetch_related_val_order_id", "shopapp_product"."id", "shopapp_product"."name", "shopapp_pro
duct"."description", "shopapp_product"."price", "shopapp_product"."discount", "shopapp_product"."created_at", "shopapp_product"."created_by", "shopapp_p
roduct"."archived", "shopapp_product"."preview" FROM "shopapp_product" INNER JOIN "shopapp_order_products" ON ("shopapp_product"."id" = "shopapp_order_p
roducts"."product_id") WHERE "shopapp_order_products"."order_id" IN (1, 2, 3, 4) ORDER BY "shopapp_product"."name" ASC, "shopapp_product"."price" ASC;

SELECT "django_session"."session_key", "django_session"."session_data", "django_session"."expire_date" FROM "django_session" WHERE ("django_sess
ion"."expire_date" > '2023-09-03 14:26:25.871426' AND "django_session"."session_key" = '9wtrd8infskrkvu7vza7cgghdxu9zchj') LIMIT 21; args=('2023-09-03 1
4:26:25.871426', '9wtrd8infskrkvu7vza7cgghdxu9zchj');

SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."firs
t_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined" FROM "auth_user" WHERE
 "auth_user"."id" = 1 LIMIT 21; 

SELECT "shopapp_order"."id", "shopapp_order"."delivery_adress", "shopapp_order"."promocode", "shopapp_order"."created_at", "shopapp_order"."user
_id", "shopapp_order"."description", "shopapp_order"."receipt", "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_supe
ruser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active",
 "auth_user"."date_joined" FROM "shopapp_order" INNER JOIN "auth_user" ON ("shopapp_order"."user_id" = "auth_user"."id");

 SELECT ("shopapp_order_products"."order_id") AS "_prefetch_related_val_order_id", "shopapp_product"."id", "shopapp_product"."name", "shopapp_pro
duct"."description", "shopapp_product"."price", "shopapp_product"."discount", "shopapp_product"."created_at", "shopapp_product"."created_by", "shopapp_p
roduct"."archived", "shopapp_product"."preview" FROM "shopapp_product" INNER JOIN "shopapp_order_products" ON ("shopapp_product"."id" = "shopapp_order_p
roducts"."product_id") WHERE "shopapp_order_products"."order_id" IN (1, 2, 3, 4) ORDER BY "shopapp_product"."name" ASC, "shopapp_product"."price" ASC;
