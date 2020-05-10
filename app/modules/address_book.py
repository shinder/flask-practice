from flask import Flask, request, render_template, session, jsonify
import json
import math
import modules.mongo_connection

def ab_list(page=1):
    (db, connection) = modules.mongo_connection.getDB('test')
    output = {
        'page_name': 'ab-list',
        'totalRows': 0,   # 總筆數
        'perPage': 3,     # 每一頁最多幾筆
        'totalPages': 0,  # 總頁數
        'page': page,     # 用戶要查看的頁數
        'rows': [],       # 當頁的資料
    }
    output['totalRows']  = db.address_book.count_documents({})
    output['totalPages'] = math.ceil(output['totalRows']/output['perPage'])
    output['page'] = 1 if page < 1 else page
    if output['page'] > output['totalPages']:
        output['page'] = output['totalPages']
    if output['totalRows']==0:
        output['rows'] = []
    else:
        cursor = db.address_book.find({},
                        sort=[('_id', -1)],
                        skip=(output['page']-1) * output['perPage'],
                        limit=output['perPage']
                    )
        for doc in cursor:
            doc['_id'] = str(doc['_id'])
            output['rows'].append(doc)
    return render_template('address-book/list.html', **output)






 