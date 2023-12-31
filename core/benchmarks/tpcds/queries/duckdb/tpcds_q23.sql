
WITH frequent_ss_items AS
  (SELECT itemdesc,
          i_item_sk item_sk,
          d_date solddate,
          count(*) cnt
   FROM store_sales,
        date_dim,
     (SELECT SUBSTRING(i_item_desc, 1, 30) itemdesc, * FROM item) sq1
   WHERE ss_sold_date_sk = d_date_sk
     AND ss_item_sk = i_item_sk
     AND d_year IN (1999,
                    1999+1,
                    1999+2,
                    1999+3)
   GROUP BY itemdesc,
            i_item_sk,
            d_date
   HAVING count(*) >4),
      max_store_sales AS
  (SELECT max(csales) tpcds_cmax
   FROM
     (SELECT c_customer_sk,
             sum(ss_quantity*ss_sales_price) csales
      FROM store_sales,
           customer,
           date_dim
      WHERE ss_customer_sk = c_customer_sk
        AND ss_sold_date_sk = d_date_sk
        AND d_year IN (1999,
                       1999+1,
                       1999+2,
                       1999+3)
      GROUP BY c_customer_sk) sq2),
      best_ss_customer AS
  (SELECT c_customer_sk,
          sum(ss_quantity*ss_sales_price) ssales
   FROM store_sales,
        customer,
        max_store_sales
   WHERE ss_customer_sk = c_customer_sk
   GROUP BY c_customer_sk
   HAVING sum(ss_quantity*ss_sales_price) > (95/100.0) * max(tpcds_cmax))
SELECT sum(sales)
FROM
  (SELECT cs_quantity*cs_list_price sales
   FROM catalog_sales,
        date_dim,
        frequent_ss_items,
        best_ss_customer
   WHERE d_year = 1999
     AND d_moy = 1
     AND cs_sold_date_sk = d_date_sk
     AND cs_item_sk = item_sk
     AND cs_bill_customer_sk = c_customer_sk
   UNION ALL SELECT ws_quantity*ws_list_price sales
   FROM web_sales,
        date_dim,
        frequent_ss_items,
        best_ss_customer
   WHERE d_year = 1999
     AND d_moy = 1
     AND ws_sold_date_sk = d_date_sk
     AND ws_item_sk = item_sk
     AND ws_bill_customer_sk = c_customer_sk) sq3
LIMIT 100;
WITH frequent_ss_items AS
  (SELECT itemdesc,
          i_item_sk item_sk,
          d_date solddate,
          count(*) cnt
   FROM store_sales,
        date_dim,
     (SELECT SUBSTRING(i_item_desc, 1, 30) itemdesc,
             *
      FROM item) sq1
   WHERE ss_sold_date_sk = d_date_sk
     AND ss_item_sk = i_item_sk
     AND d_year IN (1999,
                    1999+1,
                    1999+2,
                    1999+3)
   GROUP BY itemdesc,
            i_item_sk,
            d_date
   HAVING count(*) >4),
     max_store_sales AS
  (SELECT max(csales) tpcds_cmax
   FROM
     (SELECT c_customer_sk,
             sum(ss_quantity*ss_sales_price) csales
      FROM store_sales,
           customer,
           date_dim
      WHERE ss_customer_sk = c_customer_sk
        AND ss_sold_date_sk = d_date_sk
        AND d_year IN (1999,
                       1999+1,
                       1999+2,
                       1999+3)
      GROUP BY c_customer_sk) sq2),
     best_ss_customer AS
  (SELECT c_customer_sk,
          sum(ss_quantity*ss_sales_price) ssales
   FROM store_sales,
        customer,
        max_store_sales
   WHERE ss_customer_sk = c_customer_sk
   GROUP BY c_customer_sk
   HAVING sum(ss_quantity*ss_sales_price) > (95/100.0) * max(tpcds_cmax))
SELECT c_last_name,
       c_first_name,
       sales
FROM
  (SELECT c_last_name,
          c_first_name,
          sum(cs_quantity*cs_list_price) sales
   FROM catalog_sales,
        customer,
        date_dim,
        frequent_ss_items,
        best_ss_customer
   WHERE d_year = 1999
     AND d_moy = 1
     AND cs_sold_date_sk = d_date_sk
     AND cs_item_sk = item_sk
     AND cs_bill_customer_sk = best_ss_customer.c_customer_sk
     AND cs_bill_customer_sk = customer.c_customer_sk
   GROUP BY c_last_name,
            c_first_name
   UNION ALL SELECT c_last_name,
                    c_first_name,
                    sum(ws_quantity*ws_list_price) sales
   FROM web_sales,
        customer,
        date_dim,
        frequent_ss_items,
        best_ss_customer
   WHERE d_year = 1999
     AND d_moy = 1
     AND ws_sold_date_sk = d_date_sk
     AND ws_item_sk = item_sk
     AND ws_bill_customer_sk = best_ss_customer.c_customer_sk
     AND ws_bill_customer_sk = customer.c_customer_sk
   GROUP BY c_last_name,
            c_first_name) sq3
ORDER BY c_last_name,
         c_first_name,
         sales
LIMIT 100;


